from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from app.models.mixins import AuditMixin, OwnershipMixin
import uuid

class Department(Base, AuditMixin, OwnershipMixin):
    __tablename__ = "departments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Relationships
    employees: Mapped[list["Employee"]] = relationship("Employee", back_populates="department", cascade="all, delete-orphan")
    resources: Mapped[list["Resource"]] = relationship("Resource", back_populates="department", cascade="all, delete-orphan")