from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Resource

router = APIRouter()


@router.get("/resources")
def get_resources(
    db: Session = Depends(get_db)
):
    resources = db.query(Resource).all()

    return [
        {
            "id": str(resource.id),
            "name": resource.name,
            "resource_type": resource.resource_type.value,
            "sensitivity_level": resource.sensitivity_level.value,
            "environment": resource.environment.value,
            "active": resource.is_active,
        }
        for resource in resources
    ]