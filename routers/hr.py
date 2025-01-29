from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from database import get_db
from models.hr import EmployeeInfo, EmployeeSalary
from sqlalchemy.sql import func
from typing import Optional
from pydantic import BaseModel
from typing import Optional

class EditSalaryInput(BaseModel):
    company_domain: str
    gross_salary: Optional[float] = None
    insurance: Optional[float] = None
    taxes: Optional[float] = None
    net_salary: Optional[float] = None
    due_year: Optional[int] = None
    due_month: Optional[int] = None



hr_router = APIRouter()
@hr_router.post("/employees", status_code=status.HTTP_201_CREATED)
def add_employee(
    contact_name: str,
    company_domain: str,
    business_phone: str = None,
    personal_phone: str = None,
    business_email: str = None,
    personal_email: str = None,
    gender: str = None,
    is_company_admin: bool = False,
    db: Session = Depends(get_db)
):
    # Add the new employee
    new_employee = EmployeeInfo(
        contact_name=contact_name,
        company_domain=company_domain,
        business_phone=business_phone,
        personal_phone=personal_phone,
        business_email=business_email,
        personal_email=personal_email,
        gender=gender,
        is_company_admin=is_company_admin,
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {"message": "Employee added successfully", "employee": new_employee}
@hr_router.post("/employees/{employee_id}/salaries", status_code=status.HTTP_201_CREATED)
def add_salary(
    employee_id: int,
    company_domain: str,
    due_year: int,
    due_month: int,
    gross_salary: float = None,
    insurance: float = None,
    taxes: float = None,
    net_salary: float = None,
    due_date: str = None,
    db: Session = Depends(get_db)
):

    # Verify the employee exists and belongs to the correct company domain
    employee = db.query(EmployeeInfo).filter(
        EmployeeInfo.employee_id == employee_id,
        EmployeeInfo.company_domain == company_domain
    ).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found or incorrect company domain")

    # Add the salary
    new_salary = EmployeeSalary(
        employee_id=employee_id,
        company_domain=company_domain,
        gross_salary=gross_salary,
        insurance=insurance,
        taxes=taxes,
        net_salary=net_salary,
        due_year=due_year,
        due_month=due_month,
        due_date=due_date or func.now(),
    )
    db.add(new_salary)
    db.commit()
    db.refresh(new_salary)

    return {"message": "Salary added successfully", "salary": new_salary}


# Define a Pydantic model for the request body
class EmployeeUpdateRequest(BaseModel):
    contact_name: Optional[str] = None
    business_phone: Optional[str] = None
    personal_phone: Optional[str] = None
    business_email: Optional[str] = None
    personal_email: Optional[str] = None
    gender: Optional[str] = None
    is_company_admin: Optional[bool] = None

@hr_router.put("/employees/{employee_id}", status_code=status.HTTP_200_OK)
def edit_employee(
    employee_id: int,
    company_domain: str,  # Still from query parameters
    payload: EmployeeUpdateRequest,  # Request body
    db: Session = Depends(get_db)
):

    # Verify the employee exists
    employee = db.query(EmployeeInfo).filter(
        EmployeeInfo.employee_id == employee_id,
        EmployeeInfo.company_domain == company_domain,
    ).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )

    # Update fields if provided
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)

    return {"message": "Employee updated successfully", "employee": employee}
@hr_router.put("/employees/{employee_id}/salaries", status_code=status.HTTP_200_OK)
def edit_salary(
    employee_id: int,
    salary_data: EditSalaryInput,  # Use the Pydantic model
    db: Session = Depends(get_db)
):
    # Verify the salary record exists
    salary = db.query(EmployeeSalary).filter(
        EmployeeSalary.employee_id == employee_id,
        EmployeeSalary.company_domain == salary_data.company_domain
    ).first()
    if not salary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Salary record not found")

    # Update fields
    if salary_data.gross_salary is not None:
        salary.gross_salary = salary_data.gross_salary
    if salary_data.insurance is not None:
        salary.insurance = salary_data.insurance
    if salary_data.taxes is not None:
        salary.taxes = salary_data.taxes
    if salary_data.net_salary is not None:
        salary.net_salary = salary_data.net_salary
    if salary_data.due_year is not None:
        salary.due_year = salary_data.due_year
    if salary_data.due_month is not None:
        salary.due_month = salary_data.due_month

    db.commit()
    db.refresh(salary)

    return {"message": "Salary updated successfully", "salary": salary}

@hr_router.get("/employees", status_code=status.HTTP_200_OK)
def view_all_employees(
    db: Session = Depends(get_db)
):
    employees = db.query(EmployeeInfo).all()
    return {"employees": employees}

@hr_router.delete("/employees/{employee_id}", status_code=status.HTTP_200_OK)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    # Verify the employee exists
    employee = db.query(EmployeeInfo).filter(
        EmployeeInfo.employee_id == employee_id,
    ).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    db.query(EmployeeSalary).filter(EmployeeSalary.employee_id == employee_id).delete()

    # Delete the employee
    db.delete(employee)
    db.commit()

    return {"message": "Employee deleted successfully"}

@hr_router.get("/employees/{employee_id}/salaries", status_code=status.HTTP_200_OK)
def view_salaries(
    employee_id: int,
    db: Session = Depends(get_db)
):
    salary = db.query(EmployeeSalary).filter(
        EmployeeSalary.employee_id == employee_id
    ).all()
    return {"salary": salary}