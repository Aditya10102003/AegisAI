from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from app.models.mixins import AuditMixin
from app.models.enums import EmploymentStatus, EmploymentType
import uuid

class Employee(Base, AuditMixin):
    __tablename__ = "employees"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    department_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)
    manager_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True)
    job_title: Mapped[str] = mapped_column(String(100), nullable=True)
    location: Mapped[str] = mapped_column(String(100), nullable=True)
    employment_type: Mapped[EmploymentType] = mapped_column(Enum(EmploymentType), nullable=False)
    employment_status: Mapped[EmploymentStatus] = mapped_column(Enum(EmploymentStatus), nullable=False)

    # Relationships
    department: Mapped["Department"] = relationship("Department", back_populates="employees")
    manager: Mapped["Employee"] = relationship("Employee", remote_side="Employee.id", back_populates="subordinates")
    subordinates: Mapped[list["Employee"]] = relationship("Employee", back_populates="manager", cascade="all, delete-orphan")

    # RBAC Relationships
    user_roles: Mapped[list["UserRole"]] = relationship(
        "UserRole",
        back_populates="employee"
    )

    # Future Relationships
    access_requests: Mapped[list["AccessRequest"]] = relationship(
        "AccessRequest",
        foreign_keys="AccessRequest.employee_id",
        back_populates="employee"
    )

    access_grants: Mapped[list["AccessGrant"]] = relationship(
        "AccessGrant",
        foreign_keys="AccessGrant.employee_id",
        back_populates="employee"
    )

    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="employee"
    )