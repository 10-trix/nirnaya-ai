import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.db import get_db
from backend.database.models import Employee
from backend.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee_in: EmployeeCreate, db: Session = Depends(get_db)):
    """
    Create a new employee record.
    The onboarding chat's parsed output will be POSTed here by GenAI teammate.
    """
    new_employee = Employee(
        id=str(uuid.uuid4()),
        name=employee_in.name,
        role=employee_in.role,
        department=employee_in.department,
        tenure_months=employee_in.tenure_months or 0,
        engagement_score=employee_in.engagement_score if employee_in.engagement_score is not None else 3.0,
        time_since_promotion_months=employee_in.time_since_promotion_months or 0,
        overtime_hours=employee_in.overtime_hours if employee_in.overtime_hours is not None else 0.0,
        JobLevel=employee_in.JobLevel or 1,
        WorkLifeBalance=employee_in.WorkLifeBalance or 3,
        skills=employee_in.skills or []
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


@router.get("", response_model=List[EmployeeResponse])
def list_employees(department: Optional[str] = None, db: Session = Depends(get_db)):
    """
    List all employees. Optionally filter by department.
    """
    query = db.query(Employee)
    if department:
        query = query.filter(Employee.department.ilike(department))
    return query.all()


@router.get("/{id}", response_model=EmployeeResponse)
def get_employee(id: str, db: Session = Depends(get_db)):
    """
    Fetch a single employee record by ID.
    """
    employee = db.query(Employee).filter(Employee.id == id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id '{id}' not found"
        )
    return employee


@router.put("/{id}", response_model=EmployeeResponse)
def update_employee(id: str, employee_in: EmployeeUpdate, db: Session = Depends(get_db)):
    """
    Update an existing employee record.
    """
    employee = db.query(Employee).filter(Employee.id == id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id '{id}' not found"
        )

    update_data = employee_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)
    return employee


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(id: str, db: Session = Depends(get_db)):
    """
    Delete an employee record by ID.
    """
    employee = db.query(Employee).filter(Employee.id == id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id '{id}' not found"
        )

    db.delete(employee)
    db.commit()
    return None
