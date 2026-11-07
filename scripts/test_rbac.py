import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
from app.core.database import SessionLocal
from app.services.authorization import can_access


def main():
    db = SessionLocal()

    try:
        employee_id = "EMP003"
        action = "ADMIN"

        result = can_access(
            db=db,
            employee_id=employee_id,
            action=action
        )

        print(f"Employee: {employee_id}")
        print(f"Action: {action}")
        print(f"Access: {result}")

    finally:
        db.close()


if __name__ == "__main__":
    main()