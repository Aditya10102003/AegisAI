from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Role

router = APIRouter()


@router.get("/roles")
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()

    return [
        {
            "id": str(role.id),
            "name": role.name,
            "description": role.description,
        }
        for role in roles
    ]