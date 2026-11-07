from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import AccessGrant, Employee, Resource
from app.models.enums import AccessGrantStatus
from app.models import AuditLog
from app.models.enums import DecisionType
router = APIRouter()


@router.get("/access-grants")
def get_access_grants(
    db: Session = Depends(get_db)
):
    grants = db.query(AccessGrant).all()

    response = []

    for grant in grants:
        employee = (
            db.query(Employee)
            .filter(Employee.id == grant.employee_id)
            .first()
        )

        resource = (
            db.query(Resource)
            .filter(Resource.id == grant.resource_id)
            .first()
        )

        response.append(
            {
                "grant_id": str(grant.id),
                "employee_id": employee.employee_id if employee else None,
                "resource": resource.name if resource else None,
                "action": grant.granted_action,
                "status": grant.status.value,
                "grant_type": grant.grant_type.value,
            }
        )

    return response

@router.post("/access-grants/{grant_id}/revoke")
def revoke_access_grant(
    grant_id: str,
    db: Session = Depends(get_db)
):
    grant = (
        db.query(AccessGrant)
        .filter(AccessGrant.id == grant_id)
        .first()
    )

    if not grant:
        return {
            "error": "Grant not found"
        }

    grant.status = AccessGrantStatus.REVOKED

    audit_log = AuditLog(
        employee_id=grant.employee_id,
        resource_id=grant.resource_id,
        action="REVOKE_ACCESS",
        requested_action=grant.granted_action,
        decision=DecisionType.DENIED,
        reason="Access revoked",
    )
    db.add(audit_log)

    db.commit()

    return {
        "grant_id": str(grant.id),
        "status": grant.status.value,
    }
