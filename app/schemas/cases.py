from datetime import datetime
from pydantic import BaseModel, Field


class TransactionOut(BaseModel):
    tx_ref: str
    amount: float
    currency: str
    beneficiary: str
    beneficiary_country: str
    is_new_beneficiary: bool
    occurred_at: datetime


class CaseOut(BaseModel):
    case_ref: str
    customer_ref: str
    status: str
    disposition: str | None = None


class CaseDetail(CaseOut):
    customer_name: str
    customer_country: str
    customer_risk_rating: str
    transactions: list[TransactionOut]


class InvestigateRequest(BaseModel):
    analyst_question: str = Field(min_length=5, max_length=2000)
    jurisdiction: str = Field(default="US", min_length=2, max_length=8)


class EvidenceCitation(BaseModel):
    document_id: str
    section: str
    title: str


class InvestigationResponse(BaseModel):
    case_ref: str
    correlation_id: str
    risk_score: float
    risk_level: str
    indicators: list[str]
    summary: str
    recommended_action: str
    citations: list[EvidenceCitation]
    model_provider: str
    model_id: str
    human_review_required: bool = True


class ReviewRequest(BaseModel):
    decision: str = Field(pattern="^(ESCALATE|CLOSE|REQUEST_INFORMATION)$")
    reason: str = Field(min_length=10, max_length=2000)
