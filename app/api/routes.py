import json
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import analyst_identity
from app.db.session import get_db
from app.models.entities import AuditEvent, Case, Customer, Transaction
from app.schemas.cases import CaseDetail, CaseOut, InvestigateRequest, InvestigationResponse, ReviewRequest
from app.services.audit import write_audit
from app.services.investigation import InvestigationService, UnsafePromptError

router = APIRouter(prefix="/api/v1")
service = InvestigationService()


@router.get("/cases", response_model=list[CaseOut])
def list_cases(db: Session = Depends(get_db), actor: str = Depends(analyst_identity)):
    return db.query(Case).order_by(Case.created_at.desc()).all()


@router.get("/cases/{case_ref}", response_model=CaseDetail)
def get_case(case_ref: str, db: Session = Depends(get_db), actor: str = Depends(analyst_identity)):
    case = db.query(Case).filter(Case.case_ref == case_ref).first()
    if not case:
        raise HTTPException(404, "Case not found")
    customer = db.query(Customer).filter(Customer.customer_ref == case.customer_ref).first()
    txs = db.query(Transaction).filter(Transaction.customer_ref == case.customer_ref).order_by(Transaction.occurred_at).all()
    return {
        "case_ref": case.case_ref, "customer_ref": case.customer_ref, "status": case.status,
        "disposition": case.disposition, "customer_name": customer.full_name,
        "customer_country": customer.country, "customer_risk_rating": customer.risk_rating,
        "transactions": txs,
    }


@router.post("/cases/{case_ref}/investigate", response_model=InvestigationResponse)
def investigate(case_ref: str, body: InvestigateRequest, db: Session = Depends(get_db), actor: str = Depends(analyst_identity)):
    try:
        return service.investigate(db, case_ref, body.analyst_question, body.jurisdiction, actor)
    except LookupError as e:
        raise HTTPException(404, str(e))
    except UnsafePromptError as e:
        raise HTTPException(400, str(e))


@router.post("/cases/{case_ref}/review")
def review(case_ref: str, body: ReviewRequest, db: Session = Depends(get_db), actor: str = Depends(analyst_identity)):
    case = db.query(Case).filter(Case.case_ref == case_ref).first()
    if not case:
        raise HTTPException(404, "Case not found")
    case.disposition = body.decision
    case.disposition_reason = body.reason
    case.status = "REVIEWED"
    db.commit()
    correlation_id = str(uuid.uuid4())
    write_audit(db, event_type="CASE_REVIEWED", actor=actor, correlation_id=correlation_id,
                case_ref=case_ref, details={"decision": body.decision, "reason": body.reason})
    return {"case_ref": case_ref, "status": case.status, "decision": body.decision, "correlation_id": correlation_id}


@router.get("/audit")
def audit(case_id: str | None = Query(default=None), db: Session = Depends(get_db), actor: str = Depends(analyst_identity)):
    q = db.query(AuditEvent)
    if case_id:
        q = q.filter(AuditEvent.case_ref == case_id)
    events = q.order_by(AuditEvent.created_at.desc()).limit(100).all()
    return [{"event_type": e.event_type, "case_ref": e.case_ref, "actor": e.actor,
             "correlation_id": e.correlation_id, "details": json.loads(e.details_json), "created_at": e.created_at} for e in events]
