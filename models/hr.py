from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint, Float, Date
from sqlalchemy.sql import func
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from database import Base  # Assuming `Base` is defined in your project

class EmployeeInfo(Base):
    __tablename__ = "employees_info"

    employee_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    company_domain = Column(String(100), ForeignKey("company_info.company_domain"), nullable=False)
    contact_name = Column(String(50), nullable=False)
    business_phone = Column(String(50), nullable=True)
    personal_phone = Column(String(50), nullable=True)
    business_email = Column(String(50), nullable=True)
    personal_email = Column(String(50), nullable=True)
    gender = Column(String(10), nullable=True)
    is_company_admin = Column(Boolean, nullable=False, default=False)
    user_uid = Column(UNIQUEIDENTIFIER, nullable=True)
    date_added = Column(DateTime, nullable=False, default=func.now())

    __table_args__ = (
        UniqueConstraint("company_domain", "employee_id", name="uq_company_employee"),
    )
class EmployeeSalary(Base):
    __tablename__ = "employees_salaries"

    company_domain = Column(String(100), ForeignKey("employees_info.company_domain"), primary_key=True, nullable=False)
    employee_id = Column(Integer, ForeignKey("employees_info.employee_id"), primary_key=True, nullable=False)
    gross_salary = Column(Float, nullable=True)
    insurance = Column(Float, nullable=True)
    taxes = Column(Float, nullable=True)
    net_salary = Column(Float, nullable=True)
    due_year = Column(Integer, primary_key=True, nullable=False)
    due_month = Column(Integer, primary_key=True, nullable=False)
    due_date = Column(Date, nullable=True)
    date_added = Column(DateTime, nullable=False, default=func.now())