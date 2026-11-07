from sqlalchemy import String, Text, Enum, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from app.models.enums import DecisionType
import uuid
from datetime import datetime

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    resource_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resources.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    requested_action: Mapped[str] = mapped_column(String(50), nullable=True)
    decision: Mapped[DecisionType] = mapped_column(Enum(DecisionType), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=True)
    location: Mapped[str] = mapped_column(String(100), nullable=True)
    user_agent: Mapped[str] = mapped_column(String(255), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    employee: Mapped["Employee"] = relationship("Employee", back_populates="audit_logs")
    resource: Mapped["Resource"] = relationship("Resource", back_populates="audit_logs")