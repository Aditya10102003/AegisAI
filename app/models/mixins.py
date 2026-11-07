from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID

class AuditMixin:
    """Mixin to add created_at and updated_at fields for auditability."""
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class OwnershipMixin:
    """Mixin to add created_by and updated_by fields for ownership tracking."""
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)