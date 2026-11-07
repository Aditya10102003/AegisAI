from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import AuditLog

router = APIRouter()


@router.get("/audit-logs")
def get_audit_logs(
    db: Session = Depends(get_db)
):
    logs = db.query(AuditLog).all()

    return [
        {
            "id": str(log.id),
            "action": log.action,
            "requested_action": log.requested_action,
            "decision": log.decision.value,
            "reason": log.reason,
            "timestamp": log.timestamp,
        }
        for log in logs
    ]