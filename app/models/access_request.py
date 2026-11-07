from sqlalchemy import String, Text, Enum, ForeignKey, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from app.models.mixins import AuditMixin
from app.models.enums import AccessRequestStatus, RequestType
import uuid
from datetime import datetime

class AccessRequest(Base, AuditMixin):
    __tablename__ = "access_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    resource_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resources.id"), nullable=False)
    requested_action: Mapped[str] = mapped_column(String(50), nullable=False)
    request_type: Mapped[RequestType] = mapped_column(Enum(RequestType), nullable=False)
    business_justification: Mapped[str] = mapped_column(Text, nullable=False)
    approval_manager_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True)
    status: Mapped[AccessRequestStatus] = mapped_column(Enum(AccessRequestStatus), nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    ai_recommendation: Mapped[str] = mapped_column(Text, nullable=True)
    approved_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    rejected_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Relationships
    employee: Mapped["Employee"] = relationship("Employee", back_populates="access_requests", foreign_keys=[employee_id])
    resource: Mapped["Resource"] = relationship("Resource", back_populates="access_requests")
    approval_manager: Mapped["Employee"] = relationship("Employee", foreign_keys=[approval_manager_id])