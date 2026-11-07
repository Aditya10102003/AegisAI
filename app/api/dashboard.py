from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models import (
    Employee,
    Resource,
    AccessRequest,
    AccessGrant,
    AccessReview,
)

from app.models.enums import (
    AccessRequestStatus,
    AccessGrantStatus,
    ReviewStatus,
)

router = APIRouter()


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db)
):
    return {
        "employees":
            db.query(Employee).count(),

        "resources":
            db.query(Resource).count(),

        "pending_requests":
            db.query(AccessRequest)
            .filter(
                AccessRequest.status
                == AccessRequestStatus.PENDING
            )
            .count(),

        "active_grants":
            db.query(AccessGrant)
            .filter(
                AccessGrant.status
                == AccessGrantStatus.ACTIVE
            )
            .count(),

        "pending_reviews":
            db.query(AccessReview)
            .filter(
                AccessReview.status
                == ReviewStatus.PENDING
            )
            .count(),
    }