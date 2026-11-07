
from sqlalchemy.orm import Session

from app.models import Employee, UserRole, RolePermission, Permission
from app.models.enums import EmploymentStatus


def can_access(
    db: Session,
    employee_id: str,
    action: str,
) -> bool:
    """Check whether an active employee has a role granting the action."""

    # 1. Find the employee.
    employee = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_id)
        .first()
    )

    if employee is None:
        return False

    # 2. Deny access to inactive employees.
    if employee.employment_status != EmploymentStatus.ACTIVE:
        return False

    # 3. Find the employee's roles.
    role_ids = (
        db.query(UserRole.role_id)
        .filter(UserRole.employee_id == employee.id)
        .all()
    )

    if not role_ids:
        return False

    role_id_values = [row[0] for row in role_ids]

    # 4. Check whether any assigned role grants the action.
    permission = (
        db.query(Permission.id)
        .join(
            RolePermission,
            RolePermission.permission_id == Permission.id,
        )
        .filter(
            RolePermission.role_id.in_(role_id_values),
            Permission.action.ilike(action),
        )
        .first()
    )

    return permission is not None
