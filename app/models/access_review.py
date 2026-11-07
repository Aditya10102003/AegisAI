import uuid
from datetime import datetime

from sqlalchemy import (
    Enum,
    ForeignKey,
    DateTime,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base
from app.models.enums import (
    ReviewStatus,
    DecisionType,
)


class AccessReview(Base):
    __tablename__ = "access_reviews"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    access_grant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("access_grants.id"),
        nullable=False,
    )

    reviewer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("employees.id"),
        nullable=False,
    )

    status: Mapped[ReviewStatus] = mapped_column(
        Enum(ReviewStatus),
        nullable=False,
    )

    decision: Mapped[DecisionType] = mapped_column(
        Enum(DecisionType),
        nullable=True,
    )

    comments: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    due_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    completed_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
    )

    access_grant = relationship(
        "AccessGrant"
    )

    reviewer = relationship(
        "Employee"
    )