from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LeadCreate(BaseModel):
    name: str
    email: str
    phone: str
    lead_stage: str
    lead_status: str
    assigned_to: int

class LeadCreateRequest(BaseModel):
    name: str
    email: str
    lead_phone: str
    lead_stage: int
    lead_status: int
    assigned_to: int  # User ID
    company_domain: str  # Added field




class UpdateLead(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    lead_phone: Optional[str] = None
    lead_stage: Optional[int] = None
    lead_status: Optional[int] = None
    assigned_to: Optional[int] = None
    company_domain: Optional[str] = None
    lead_type: Optional[int] = None

