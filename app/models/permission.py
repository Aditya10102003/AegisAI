from sqlalchemy import String, Text, UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from app.models.enums import ResourceType
import uuid

class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    resource_type: Mapped[ResourceType] = mapped_column(Enum(ResourceType), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Relationships
    role_permissions: Mapped[list["RolePermission"]] = relationship(
        "RolePermission", back_populates="permission", cascade="all, delete-orphan"
    )

    # Uniqueness constraint
    __table_args__ = (
        UniqueConstraint("name", "action", "resource_type", name="uq_permission_name_action_resource_type"),
    )