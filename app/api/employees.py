from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Employee

router = APIRouter()

@router.get("/employees")
def get_employees(db: Session = Depends(get_db)):
    """
    Retrieve all employees with their basic information.

    Returns:
        List of employees with employee_id, first_name, last_name, and email.
    """
    employees = db.query(Employee).all()
    return [
        {
            "employee_id": employee.employee_id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "email": employee.email,
        }
        for employee in employees
    ]