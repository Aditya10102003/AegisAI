from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import AccessGrant
from app.models import AuditLog
from app.models.enums import DecisionType
from app.services.sod import check_sod_violation
from app.models.enums import (
    GrantType,
    AccessGrantStatus,
    ReviewStatus,
)
from app.core.database import get_db
from app.services.risk_scoring import calculate_risk_score
from app.services.risk_scoring import (
    calculate_risk_score,
    get_risk_level,
)

from app.models import (
    AccessRequest,
    Employee,
    Resource,
)
from app.models.enums import (
    AccessRequestStatus,
)

from app.models.enums import (
    RequestType,
)

router = APIRouter()


@router.get("/access-requests")
def get_access_requests(
    db: Session = Depends(get_db)
):
    requests = db.query(AccessRequest).all()

    return [
        {
            "id": str(req.id),
            "status": req.status.value,
        }
        for req in requests
    ]


@router.post("/access-requests")
def create_access_request(
    employee_id: str,
    resource_name: str,
    action: str,
    justification: str,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_id)
        .first()
    )

    if not employee:
        return {"error": "Employee not found"}

    resource = (
        db.query(Resource)
        .filter(Resource.name == resource_name)
        .first()
    )

    if not resource:
        return {"error": "Resource not found"}
    risk_score = calculate_risk_score(
        resource,
        action,
    )
    risk_level = get_risk_level(
       risk_score
    )
    request = AccessRequest(
        employee_id=employee.id,
        resource_id=resource.id,
        requested_action=action,
        request_type=RequestType.NEW,
        business_justification=justification,
        status=AccessRequestStatus.PENDING,
        risk_score=risk_score,
    )

    db.add(request)
    db.commit()
    db.refresh(request)

    return {
        "request_id": str(request.id),
        "status": request.status.value,
        "resource": resource.name,
        "risk_score": request.risk_score,
        "risk_level": risk_level,
    }
@router.post("/access-requests/{request_id}/approve")
def approve_access_request(
    request_id: str,
    db: Session = Depends(get_db)
):
    access_request = (
        db.query(AccessRequest)
        .filter(AccessRequest.id == request_id)
        .first()
    )

    if not access_request:
        return {
            "error": "Request not found"
        }
    employee = (
        db.query(Employee)
        .filter(Employee.id == access_request.employee_id)
        .first()
    )

    if check_sod_violation(
        employee,
        access_request.requested_action
    ):
        return {
            "error": "Segregation of Duties violation detected"
        }

    if access_request.risk_score >= 70:

        access_request.status = (
            AccessRequestStatus.MANAGER_APPROVED
        )

        db.commit()

        return {
            "message": "Security approval required",
            "status": access_request.status.value,
        }

    access_request.status = (
        AccessRequestStatus.APPROVED
    )


    audit_log = AuditLog(
        employee_id=access_request.employee_id,
        resource_id=access_request.resource_id,
        action="APPROVE_ACCESS_REQUEST",
        requested_action=access_request.requested_action,
        decision=DecisionType.ALLOWED,
        reason="Access request approved",
    )

    grant = AccessGrant(
        employee_id=access_request.employee_id,
        resource_id=access_request.resource_id,
        granted_action=access_request.requested_action,
        grant_type=GrantType.MANUAL,
        granted_by=access_request.employee_id,  # temporary for MVP
        status=AccessGrantStatus.ACTIVE,
        review_status=ReviewStatus.PENDING,
    )

    db.add(grant)
    db.add(audit_log)
    db.commit()

    return {
        "request_id": str(access_request.id),
        "status": access_request.status.value,
        "grant_created": True,
    }

@router.post(
    "/access-requests/{request_id}/security-approve"
)
def security_approve_request(
    request_id: str,
    db: Session = Depends(get_db)
):
    access_request = (
        db.query(AccessRequest)
        .filter(
            AccessRequest.id == request_id
        )
        .first()
    )

    if not access_request:
        return {
            "error": "Request not found"
        }

    if (
        access_request.status
        != AccessRequestStatus.MANAGER_APPROVED
    ):
        return {
            "error": (
                "Manager approval required first"
            )
        }

    access_request.status = (
        AccessRequestStatus.APPROVED
    )

    grant = AccessGrant(
        employee_id=access_request.employee_id,
        resource_id=access_request.resource_id,
        granted_action=access_request.requested_action,
        grant_type=GrantType.MANUAL,
        granted_by=access_request.employee_id,
        status=AccessGrantStatus.ACTIVE,
        review_status=ReviewStatus.PENDING,
    )

    db.add(grant)
    db.commit()

    return {
        "status": "Approved",
        "grant_created": True,
    }

@router.post("/access-requests/{request_id}/reject")
def reject_access_request(
    request_id: str,
    db: Session = Depends(get_db)
):
    access_request = (
        db.query(AccessRequest)
        .filter(AccessRequest.id == request_id)
        .first()
    )

    if not access_request:
        return {
            "error": "Request not found"
        }

    access_request.status = AccessRequestStatus.REJECTED

    audit_log = AuditLog(
        employee_id=access_request.employee_id,
        resource_id=access_request.resource_id,
        action="REJECT_ACCESS_REQUEST",
        requested_action=access_request.requested_action,
        decision=DecisionType.DENIED,
        reason="Access request rejected",
    )
    db.add(audit_log)
    db.commit()

    return {
        "request_id": str(access_request.id),
        "status": access_request.status.value,
    }