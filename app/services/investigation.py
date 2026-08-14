import json
import uuid
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.models.entities import Case, Customer, Transaction, Investigation
from app.rag.retriever import LocalPolicyRetriever
from app.security.controls import detect_prompt_injection, redact_pii
from app.services.audit import write_audit
from app.services.models import BedrockProvider, GenerationRequest, LocalDeterministicProvider
from app.services.risk import RiskEngine


class UnsafePromptError(ValueError):
    pass


class InvestigationService:
    def __init__(self):
        self.settings = get_settings()
        self.risk_engine = RiskEngine()
        self.retriever = LocalPolicyRetriever()
        self.provider = (
            BedrockProvider(self.settings.aws_region, self.settings.bedrock_model_id)
            if self.settings.model_provider.lower() == "bedrock"
            else LocalDeterministicProvider()
        )

    def investigate(self, db: Session, case_ref: str, question: str, jurisdiction: str, actor: str) -> dict:
        if detect_prompt_injection(question):
            correlation_id = str(uuid.uuid4())
            write_audit(db, event_type="PROMPT_BLOCKED", actor=actor, correlation_id=correlation_id,
                        case_ref=case_ref, details={"reason": "prompt_injection_indicator"})
            raise UnsafePromptError("Request blocked by prompt-safety controls")

        case = db.query(Case).filter(Case.case_ref == case_ref).first()
        if not case:
            raise LookupError("Case not found")
        customer = db.query(Customer).filter(Customer.customer_ref == case.customer_ref).first()
        txs = db.query(Transaction).filter(Transaction.customer_ref == case.customer_ref).all()
        tx_dicts = [{
            "tx_ref": t.tx_ref, "amount": t.amount, "beneficiary_country": t.beneficiary_country,
            "is_new_beneficiary": t.is_new_beneficiary,
        } for t in txs]
        risk = self.risk_engine.evaluate(tx_dicts, customer.risk_rating)
        query = f"{question} {' '.join(risk.indicators)}"
        docs = self.retriever.search(query, jurisdiction=jurisdiction, k=3)
        evidence = [{"document_id": d.document_id, "title": d.title, "section": d.section, "text": redact_pii(d.text)} for d in docs]
        request = GenerationRequest(case_ref, redact_pii(question), risk.level, risk.score, risk.indicators, evidence)
        generated = self.provider.generate(request)
        correlation_id = str(uuid.uuid4())
        payload = {
            "case_ref": case_ref,
            "correlation_id": correlation_id,
            "risk_score": risk.score,
            "risk_level": risk.level,
            "indicators": risk.indicators,
            "summary": generated.summary,
            "recommended_action": generated.recommended_action,
            "citations": [{k: e[k] for k in ("document_id", "section", "title")} for e in evidence],
            "model_provider": generated.provider,
            "model_id": generated.model_id,
            "human_review_required": True,
        }
        db.add(Investigation(case_ref=case_ref, provider=generated.provider, model_id=generated.model_id,
                             risk_score=risk.score, risk_level=risk.level, summary_json=json.dumps(payload)))
        db.commit()
        write_audit(db, event_type="INVESTIGATION_GENERATED", actor=actor, correlation_id=correlation_id,
                    case_ref=case_ref, details={"provider": generated.provider, "model_id": generated.model_id,
                                                "sources": [e["document_id"] for e in evidence]})
        return payload
