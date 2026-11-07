from sqlalchemy import String, Text, Boolean, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from app.models.mixins import AuditMixin, OwnershipMixin
from app.models.enums import SensitivityLevel, ResourceType, EnvironmentType
import uuid

class Resource(Base, AuditMixin, OwnershipMixin):
    __tablename__ = "resources"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    resource_type: Mapped[ResourceType] = mapped_column(Enum(ResourceType), nullable=False)
    resource_identifier: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    sensitivity_level: Mapped[SensitivityLevel] = mapped_column(Enum(SensitivityLevel), nullable=False)
    environment: Mapped[EnvironmentType] = mapped_column(Enum(EnvironmentType), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    owner_department_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    business_owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True)
    technical_owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True)

    # Relationships
    department: Mapped["Department"] = relationship("Department", back_populates="resources")
    business_owner: Mapped["Employee"] = relationship("Employee", foreign_keys=[business_owner_id])
    technical_owner: Mapped["Employee"] = relationship("Employee", foreign_keys=[technical_owner_id])
    access_requests: Mapped[list["AccessRequest"]] = relationship("AccessRequest", back_populates="resource")
    access_grants: Mapped[list["AccessGrant"]] = relationship("AccessGrant", back_populates="resource")
    audit_logs: Mapped[list["AuditLog"]] = relationship("AuditLog", back_populates="resource")