from sqlalchemy import String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from app.models.mixins import AuditMixin
from app.models.enums import GrantType, AccessGrantStatus, ReviewStatus
import uuid
from datetime import datetime

class AccessGrant(Base, AuditMixin):
    __tablename__ = "access_grants"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    resource_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resources.id"), nullable=False)
    granted_action: Mapped[str] = mapped_column(String(50), nullable=False)
    grant_type: Mapped[GrantType] = mapped_column(Enum(GrantType), nullable=False)
    granted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    status: Mapped[AccessGrantStatus] = mapped_column(Enum(AccessGrantStatus), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    review_status: Mapped[ReviewStatus] = mapped_column(Enum(ReviewStatus), nullable=False)
    last_reviewed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    next_review_due_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    reviewed_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True)

    # Relationships
    employee: Mapped["Employee"] = relationship("Employee", back_populates="access_grants", foreign_keys=[employee_id])
    resource: Mapped["Resource"] = relationship("Resource", back_populates="access_grants")
    grantor: Mapped["Employee"] = relationship("Employee", foreign_keys=[granted_by])
    reviewer: Mapped["Employee"] = relationship("Employee", foreign_keys=[reviewed_by])