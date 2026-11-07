SOD_CONFLICTS = {
    "CREATE_PAYMENT": ["APPROVE_PAYMENT"],
    "APPROVE_PAYMENT": ["CREATE_PAYMENT"],

    "CREATE_USER": ["APPROVE_USER"],
    "APPROVE_USER": ["CREATE_USER"],
}

from app.models import Employee
from app.models import UserRole
from app.models import RolePermission


def check_sod_violation(
    employee,
    requested_action: str
) -> bool:

    conflicting_actions = SOD_CONFLICTS.get(
        requested_action,
        []
    )

    existing_actions = []

    for user_role in employee.user_roles:
        role = user_role.role

        for role_permission in role.role_permissions:
            permission = role_permission.permission

            existing_actions.append(
                permission.action
            )

    return any(
        action in existing_actions
        for action in conflicting_actions
    )