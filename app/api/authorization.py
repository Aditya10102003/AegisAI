from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.authorization import can_access

router = APIRouter()


@router.post("/authorize")
def authorize(
    employee_id: str,
    action: str,
    db: Session = Depends(get_db)
):
    result = can_access(
        db=db,
        employee_id=employee_id,
        action=action
    )

    return {
        "employee_id": employee_id,
        "action": action,
        "authorized": result
    }