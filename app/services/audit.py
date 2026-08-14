import json
from sqlalchemy.orm import Session
from app.models.entities import AuditEvent


def write_audit(db: Session, *, event_type: str, actor: str, correlation_id: str, details: dict, case_ref: str | None = None) -> None:
    db.add(AuditEvent(
        event_type=event_type,
        case_ref=case_ref,
        actor=actor,
        correlation_id=correlation_id,
        details_json=json.dumps(details, default=str),
    ))
    db.commit()
