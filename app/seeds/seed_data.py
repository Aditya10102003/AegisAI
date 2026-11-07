import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            ".."
        )
    )
)
from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from app.models import (
    Department,
    Employee,
    Role,
    Permission,
    UserRole,
    RolePermission,
)

from app.models.enums import (
    EmploymentType,
    EmploymentStatus,
    ResourceType,
    SensitivityLevel,
    EnvironmentType,
)
from app.models import Resource


def seed_data():
    db: Session = SessionLocal()

    try:
        print("Seeding database...")

        # =====================
        # Departments
        # =====================

        departments = {}

        for dept_name in [
            "Finance",
            "HR",
            "IT",
            "Security",
        ]:
            department = (
                db.query(Department)
                .filter(Department.name == dept_name)
                .first()
            )

            if not department:
                department = Department(
                    name=dept_name
                )
                db.add(department)
                db.flush()

            departments[dept_name] = department

        # =====================
        # Roles
        # =====================

        roles = {}

        for role_name in [
            "Employee",
            "Manager",
            "Admin",
            "Security Analyst",
        ]:
            role = (
                db.query(Role)
                .filter(Role.name == role_name)
                .first()
            )

            if not role:
                role = Role(
                    name=role_name
                )
                db.add(role)
                db.flush()

            roles[role_name] = role

        # =====================
        # Permissions
        # =====================

        permissions = {}

        permission_data = [
            {
                "name": "Read Resource",
                "action": "READ",
                "resource_type": ResourceType.APPLICATION,
            },
            {
                "name": "Write Resource",
                "action": "WRITE",
                "resource_type": ResourceType.APPLICATION,
            },
            {
                "name": "Approve Access",
                "action": "APPROVE",
                "resource_type": ResourceType.APPLICATION,
            },
            {
                "name": "Admin Access",
                "action": "ADMIN",
                "resource_type": ResourceType.APPLICATION,
            },
            # Banking Permissions
            {
                "name": "Create Payment",
                "action": "CREATE_PAYMENT",
                "resource_type": ResourceType.APPLICATION,
            },
            {
                "name": "Approve Payment",
                "action": "APPROVE_PAYMENT",
                "resource_type": ResourceType.APPLICATION,
            },
            {
                "name": "Create User",
                "action": "CREATE_USER",
                "resource_type": ResourceType.APPLICATION,
            },
            {
                "name": "Approve User",
                "action": "APPROVE_USER",
                "resource_type": ResourceType.APPLICATION,
            },

        ]

        for perm in permission_data:
            permission = (
                db.query(Permission)
                .filter(
                    Permission.action == perm["action"]
                )
                .first()
            )

            if not permission:
                permission = Permission(
                    name=perm["name"],
                    action=perm["action"],
                    resource_type=perm["resource_type"],
                )
                db.add(permission)
                db.flush()

            permissions[perm["action"]] = permission

        # =====================
        # Employees
        # =====================

        employee_data = [
            {
                "employee_id": "EMP001",
                "first_name": "John",
                "last_name": "Smith",
                "email": "john.smith@aegisai.local",
                "department": "IT",
                "employment_type": EmploymentType.FULL_TIME,
                "employment_status": EmploymentStatus.ACTIVE,
            },
            {
                "employee_id": "EMP002",
                "first_name": "Sarah",
                "last_name": "Johnson",
                "email": "sarah.johnson@aegisai.local",
                "department": "Finance",
                "employment_type": EmploymentType.FULL_TIME,
                "employment_status": EmploymentStatus.ACTIVE,
            },
            {
                "employee_id": "EMP003",
                "first_name": "Mike",
                "last_name": "Brown",
                "email": "mike.brown@aegisai.local",
                "department": "Security",
                "employment_type": EmploymentType.FULL_TIME,
                "employment_status": EmploymentStatus.ACTIVE,
            },
        ]

        employees = {}

        for emp in employee_data:
            employee = (
                db.query(Employee)
                .filter(
                    Employee.employee_id == emp["employee_id"]
                )
                .first()
            )

            if not employee:
                employee = Employee(
                    employee_id=emp["employee_id"],
                    first_name=emp["first_name"],
                    last_name=emp["last_name"],
                    email=emp["email"],
                    department_id=departments[
                        emp["department"]
                    ].id,
                    employment_type=emp["employment_type"],
                    employment_status=emp["employment_status"],
                )

                db.add(employee)
                db.flush()

            employees[emp["employee_id"]] = employee

        # =====================
        # Role Permissions
        # =====================

        role_permission_map = {
            "Employee": [
                "READ"
            ],

            "Manager": [
                "READ",
                "WRITE",
                "APPROVE",
                "CREATE_PAYMENT"
            ],

            "Admin": [
                "READ",
                "WRITE",
                "APPROVE",
                "ADMIN",
                "APPROVE_PAYMENT",
                "CREATE_USER",
                "APPROVE_USER"
            ],

            "Security Analyst": [
                "READ",
                "WRITE"
            ],
        }

        for role_name, actions in role_permission_map.items():
            role = roles[role_name]

            for action in actions:
                permission = permissions[action]

                exists = (
                    db.query(RolePermission)
                    .filter(
                        RolePermission.role_id == role.id,
                        RolePermission.permission_id == permission.id,
                    )
                    .first()
                )

                if not exists:
                    db.add(
                        RolePermission(
                            role_id=role.id,
                            permission_id=permission.id,
                        )
                    )
        # =====================
        # Resources
        # =====================

        resources = [
            {
                "name": "Finance Dashboard",
                "resource_type": ResourceType.APPLICATION,
                "resource_identifier": "finance-dashboard",
                "sensitivity_level": SensitivityLevel.CONFIDENTIAL,
                "environment": EnvironmentType.PRODUCTION,
            },
            {
                "name": "Payment API",
                "resource_type": ResourceType.API,
                "resource_identifier": "payment-api",
                "sensitivity_level": SensitivityLevel.CRITICAL,
                "environment": EnvironmentType.PRODUCTION,
            },
            {
                "name": "Customer Database",
                "resource_type": ResourceType.DATABASE,
                "resource_identifier": "customer-db",
                "sensitivity_level": SensitivityLevel.RESTRICTED,
                "environment": EnvironmentType.PRODUCTION,
            },
            {
                "name": "Security Console",
                "resource_type": ResourceType.APPLICATION,
                "resource_identifier": "security-console",
                "sensitivity_level": SensitivityLevel.CRITICAL,
                "environment": EnvironmentType.PRODUCTION,
            },
            {
                "name": "HR Portal",
                "resource_type": ResourceType.APPLICATION,
                "resource_identifier": "hr-portal",
                "sensitivity_level": SensitivityLevel.CONFIDENTIAL,
                "environment": EnvironmentType.PRODUCTION,
            },
        ]
        for resource_data in resources:
            resource = (
                db.query(Resource)
                .filter(
                    Resource.resource_identifier
                    == resource_data["resource_identifier"]
                )
                .first()
            )

            if not resource:
                resource = Resource(
                    name=resource_data["name"],
                    resource_type=resource_data["resource_type"],
                    resource_identifier=resource_data["resource_identifier"],
                    sensitivity_level=resource_data["sensitivity_level"],
                    environment=resource_data["environment"],
                )

                db.add(resource)
        # =====================
        # User Roles
        # =====================

        user_role_map = [
            ("EMP001", "Employee"),
            ("EMP002", "Manager"),
            ("EMP003", "Admin"),
        ]

        for employee_code, role_name in user_role_map:
            employee = employees[employee_code]
            role = roles[role_name]

            exists = (
                db.query(UserRole)
                .filter(
                    UserRole.employee_id == employee.id,
                    UserRole.role_id == role.id,
                )
                .first()
            )

            if not exists:
                db.add(
                    UserRole(
                        employee_id=employee.id,
                        role_id=role.id,
                    )
                )

        db.commit()

        print("✅ Seed complete")

    except Exception as e:
        db.rollback()
        print("❌ Seed failed")
        print(e)
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()