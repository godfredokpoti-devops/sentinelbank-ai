import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
import boto3


@dataclass
class GenerationRequest:
    case_ref: str
    question: str
    risk_level: str
    risk_score: float
    indicators: list[str]
    evidence: list[dict]


@dataclass
class GenerationResult:
    provider: str
    model_id: str
    summary: str
    recommended_action: str


class ModelProvider(ABC):
    @abstractmethod
    def generate(self, request: GenerationRequest) -> GenerationResult: ...


class LocalDeterministicProvider(ModelProvider):
    def generate(self, request: GenerationRequest) -> GenerationResult:
        evidence_titles = ", ".join(f"{e['document_id']} §{e['section']}" for e in request.evidence) or "no retrieved policy"
        indicator_text = "; ".join(request.indicators)
        summary = (
            f"Case {request.case_ref} is assessed at {request.risk_level} risk ({request.risk_score:.0f}/100) "
            f"based on configured transaction indicators. Material observations: {indicator_text}. "
            f"Policy context reviewed: {evidence_titles}. The analysis is advisory and requires analyst validation."
        )
        action = "Escalate for enhanced analyst review." if request.risk_level == "HIGH" else (
            "Perform targeted analyst review before disposition." if request.risk_level == "MEDIUM" else "Continue standard review and document disposition."
        )
        return GenerationResult("local", "deterministic-evidence-v1", summary, action)


class BedrockProvider(ModelProvider):
    def __init__(self, region: str, model_id: str):
        self.client = boto3.client("bedrock-runtime", region_name=region)
        self.model_id = model_id

    def generate(self, request: GenerationRequest) -> GenerationResult:
        prompt = {
            "role": "bank-risk-investigation-copilot",
            "rules": [
                "Use only supplied evidence.",
                "Do not make final banking decisions.",
                "Do not invent policies, transactions, or customer facts.",
                "State uncertainty when evidence is insufficient.",
            ],
            "case": request.__dict__,
            "output": {"summary": "string", "recommended_action": "string"},
        }
        response = self.client.converse(
            modelId=self.model_id,
            messages=[{"role": "user", "content": [{"text": json.dumps(prompt)}]}],
            inferenceConfig={"temperature": 0.1, "maxTokens": 700},
        )
        text = response["output"]["message"]["content"][0]["text"]
        try:
            parsed = json.loads(text)
            summary = parsed["summary"]
            action = parsed["recommended_action"]
        except Exception:
            summary = text
            action = "Analyst review required."
        return GenerationResult("bedrock", self.model_id, summary, action)
