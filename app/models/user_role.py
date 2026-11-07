import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

class UserRole(Base):
    __tablename__ = "user_roles"

    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"), primary_key=True)
    role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True)

    # Relationships
    employee: Mapped["Employee"] = relationship("Employee", back_populates="user_roles")
    role: Mapped["Role"] = relationship("Role", back_populates="user_roles")