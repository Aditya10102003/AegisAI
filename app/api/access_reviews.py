from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import AccessReview

from datetime import datetime, timedelta

from app.models import (
    AccessReview,
    AccessGrant,
    Employee,
)

from app.models.enums import (
    ReviewStatus,
)
from datetime import datetime
from app.models.enums import (
    ReviewStatus,
    DecisionType,
)
from app.models import AccessGrant
from app.models.enums import AccessGrantStatus
router = APIRouter()


@router.get("/access-reviews")
def get_access_reviews(
    db: Session = Depends(get_db)
):
    reviews = db.query(
        AccessReview
    ).all()

    return [
        {
            "id": str(review.id),
            "status": review.status.value,
            "due_date": review.due_date,
            "decision": (
                review.decision.value
                if review.decision
                else None
            ),
        }
        for review in reviews
    ]

@router.post("/access-reviews")
def create_access_review(
    access_grant_id: str,
    reviewer_employee_id: str,
    db: Session = Depends(get_db)
):
    grant = (
        db.query(AccessGrant)
        .filter(
            AccessGrant.id == access_grant_id
        )
        .first()
    )

    if not grant:
        return {
            "error": "Grant not found"
        }

    reviewer = (
        db.query(Employee)
        .filter(
            Employee.employee_id
            == reviewer_employee_id
        )
        .first()
    )

    if not reviewer:
        return {
            "error": "Reviewer not found"
        }

    review = AccessReview(
        access_grant_id=grant.id,
        reviewer_id=reviewer.id,
        status=ReviewStatus.PENDING,
        due_date=datetime.utcnow() + timedelta(days=90),
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return {
        "review_id": str(review.id),
        "status": review.status.value,
    }

@router.post("/access-reviews/{review_id}/certify")
def certify_access_review(
    review_id: str,
    comments: str = "",
    db: Session = Depends(get_db)
):
    review = (
        db.query(AccessReview)
        .filter(
            AccessReview.id == review_id
        )
        .first()
    )

    if not review:
        return {
            "error": "Review not found"
        }

    review.status = ReviewStatus.COMPLETED
    review.decision = DecisionType.ALLOWED
    review.comments = comments
    review.completed_at = datetime.utcnow()

    db.commit()

    return {
        "review_id": str(review.id),
        "status": review.status.value,
        "decision": review.decision.value,
    }

@router.post("/access-reviews/{review_id}/revoke")
def revoke_review_access(
    review_id: str,
    comments: str = "",
    db: Session = Depends(get_db)
):
    review = (
        db.query(AccessReview)
        .filter(
            AccessReview.id == review_id
        )
        .first()
    )

    if not review:
        return {
            "error": "Review not found"
        }

    grant = (
        db.query(AccessGrant)
        .filter(
            AccessGrant.id
            == review.access_grant_id
        )
        .first()
    )

    if grant:
        grant.status = AccessGrantStatus.REVOKED

    review.status = ReviewStatus.COMPLETED
    review.decision = DecisionType.DENIED
    review.comments = comments
    review.completed_at = datetime.utcnow()

    db.commit()

    return {
        "review_id": str(review.id),
        "status": review.status.value,
        "decision": review.decision.value,
        "grant_revoked": True,
    }