from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db  # Database dependency
from models.real_estate import Lead  # Import your models (to be created)
from schemas.real_estate import LeadCreateRequest  # Import schemas (to be created)
from models.real_estate import User
from models.real_estate import LeadStage
from models.real_estate import LeadStatus
from models.real_estate import ClientCall
from models.real_estate import ClientMeeting
from fastapi import status
from sqlalchemy.sql import func
from models.real_estate import UserRole
from models.real_estate import UserRolePermission
from models.real_estate import LeadStage
from sqlalchemy.sql import text
from typing import Optional 
from schemas.real_estate import UpdateLead
from models.real_estate import UserRoleMapping
from models.real_estate import CompanyInfo

from pydantic import BaseModel
from typing import Optional
real_estate_router = APIRouter()


class MeetingRequest(BaseModel):
    meeting_status: Optional[int] = None
    assigned_to: Optional[int] = None
    company_domain: Optional[str] = None
    meeting_date: Optional[str] = None

class CallRequest(BaseModel):
    call_status: Optional[int] = None
    assigned_to: Optional[int] = None
    company_domain: Optional[str] = None
class LeadCreateRequest(BaseModel):
    name: str
    email: str
    lead_phone: str
    lead_stage: int
    lead_status: int  # 1 = Hot, 2 = Warm, 3 = Cold, 4 = New
    lead_type: int
    assigned_to: int  # User ID
    company_domain: str


@real_estate_router.post("/leads", status_code=201)
def add_lead(request: LeadCreateRequest, db: Session = Depends(get_db)):
    # Check if the assigned user exists
    user = db.query(User).filter(User.id == request.assigned_to).first()
    if not user:
        raise HTTPException(status_code=404, detail="Assigned user not found")

    # Create a new lead
    new_lead = Lead(
        name=request.name,
        email=request.email,
        lead_phone=request.lead_phone,
        lead_stage=request.lead_stage,
        lead_status=request.lead_status,
        lead_type=request.lead_type,  
        assigned_to=request.assigned_to,
        company_domain=request.company_domain,
    )

    # Add the lead to the database
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    return {"message": "Lead added successfully", "lead": new_lead}


@real_estate_router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}

@real_estate_router.get("/leads")
def get_all_leads(db: Session = Depends(get_db)):
    leads = db.query(Lead).all()
    return {"leads": leads}

@real_estate_router.get("/lead-stages")
def get_lead_stages(db: Session = Depends(get_db)):
    stages = db.query(LeadStage).all()
    return {"lead_stages": stages}

@real_estate_router.get("/leads/{lead_id}", status_code=status.HTTP_200_OK)
def get_lead_details(lead_id: int, db: Session = Depends(get_db)):
    # Fetch the lead by ID with calls and meetings preloaded
    lead = (
        db.query(Lead)
        .filter(Lead.lead_id == lead_id)
        .options(
            joinedload(Lead.calls),  # Preload calls
            joinedload(Lead.meetings),  # Preload meetings
        )
        .first()
    )

    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found"
        )

    # Prepare the response structure
    lead_details = {
        "lead_id": lead.lead_id,
        "name": lead.name,
        "email": lead.email,
        "lead_phone": lead.lead_phone,
        "lead_stage": lead.lead_stage,
        "lead_status": lead.lead_status,
        "assigned_to": lead.assigned_to,
        "created_at": lead.created_at,
        "company_domain": lead.company_domain,
        "calls": [
            {
                "call_id": call.call_id,
                "call_date": call.call_date,
                "date_added": call.date_added,
                "assigned_to": call.assigned_to,
                "call_status": call.call_status,
                "company_domain": call.company_domain,
            }
            for call in lead.calls
        ],
        "meetings": [
            {
                "meeting_id": meeting.meeting_id,
                "meeting_date": meeting.meeting_date,
                "date_added": meeting.date_added,
                "assigned_to": meeting.assigned_to,
                "meeting_status": meeting.meeting_status,
                "company_domain": meeting.company_domain,
            }
            for meeting in lead.meetings
        ],
    }

    return {"lead": lead_details}
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse

@real_estate_router.post("/leads/{lead_id}/calls", status_code=status.HTTP_201_CREATED)
def add_call(
    lead_id: int,
    call_request: CallRequest,  # Use the request model
    db: Session = Depends(get_db)
):
    # Extract data from the request model
    call_status = call_request.call_status
    assigned_to = call_request.assigned_to
    company_domain = call_request.company_domain

    # Debugging logs
    print("Received call_status:", call_status)
    print("Received assigned_to:", assigned_to)
    print("Received company_domain:", company_domain)

    # Verify that the lead exists
    lead = db.query(Lead).filter(Lead.lead_id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")

    # Create a new client call
    new_call = ClientCall(
        lead_id=lead_id,
        call_status=call_status,
        assigned_to=assigned_to,
        company_domain=company_domain,
    )

    try:
        db.add(new_call)
        db.commit()
        db.refresh(new_call)
    except IntegrityError as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Invalid foreign key reference provided. Please verify the input."},
        )

    return {"message": "Call added successfully", "call": new_call}

@real_estate_router.post("/leads/{lead_id}/meetings", status_code=status.HTTP_201_CREATED)
def add_meeting(
    lead_id: int,
    meeting_request: MeetingRequest,  # Use the request model
    db: Session = Depends(get_db)
):
    # Extract data from the request model
    meeting_status = meeting_request.meeting_status
    assigned_to = meeting_request.assigned_to
    company_domain = meeting_request.company_domain
    meeting_date = meeting_request.meeting_date

    print("Received meeting_status:", meeting_status)
    print("Received assigned_to:", assigned_to)
    print("Received company_domain:", company_domain)
    print("Received meeting_date:", meeting_date)

    # Verify that the lead exists
    lead = db.query(Lead).filter(Lead.lead_id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")

    # Create a new client meeting
    new_meeting = ClientMeeting(
        lead_id=lead_id,
        meeting_status=meeting_status,
        assigned_to=assigned_to,
        company_domain=company_domain,
        meeting_date=meeting_date or func.now(),
    )

    try:
        db.add(new_meeting)
        db.commit()
        db.refresh(new_meeting)
    except IntegrityError as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Invalid foreign key reference provided. Please verify the input."}
        )

    return {"message": "Meeting added successfully", "meeting": new_meeting}

@real_estate_router.delete("/leads/{lead_id}", status_code=status.HTTP_200_OK)
def delete_lead(lead_id: int, user_id: int, db: Session = Depends(get_db)):
    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Check if the user has delete permission
    has_permission = (
        db.query(UserRolePermission)
        .join(UserRoleMapping, UserRolePermission.role_id == UserRoleMapping.role_id)
        .filter(
            UserRoleMapping.user_id == user_id,  # Map to the user
            UserRolePermission.d_delete == True  # Check delete permission
        )
        .first()
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied"
        )

    # Fetch the lead to delete
    lead = db.query(Lead).filter(Lead.lead_id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")

    # Delete the lead
    db.delete(lead)
    db.commit()

    return {"message": "Lead deleted successfully"}

from sqlalchemy.exc import IntegrityError

@real_estate_router.put("/leads/{lead_id}", status_code=status.HTTP_200_OK)
def edit_lead(
    lead_id: int,
    user_id: int,
    update_data: UpdateLead,
    db: Session = Depends(get_db),
):
    print (update_data)
    # Step 1: Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Step 2: Check if the user has edit permission
    has_permission = (
        db.query(UserRolePermission)
        .join(UserRoleMapping, UserRolePermission.role_id == UserRoleMapping.role_id)
        .filter(
            UserRoleMapping.user_id == user_id,  # Map to the user
            UserRolePermission.d_edit == True  # Check edit permission
        )
        .first()
    )

    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied. User does not have edit permissions.",
        )

    # Step 3: Fetch the lead to edit
    lead = db.query(Lead).filter(Lead.lead_id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")

    # Step 4: Update lead fields if new values are provided
    if update_data.name:
        lead.name = update_data.name
    if update_data.email:
        lead.email = update_data.email
    if update_data.lead_phone:
        lead.lead_phone = update_data.lead_phone
    if update_data.lead_stage:
        lead.lead_stage = update_data.lead_stage
    if update_data.lead_status:
        lead.lead_status = update_data.lead_status
    if update_data.lead_type:
        lead.lead_type = update_data.lead_type
    if update_data.assigned_to:
        lead.assigned_to = update_data.assigned_to
    if update_data.company_domain:
        lead.company_domain = update_data.company_domain

    # Step 5: Commit changes and handle foreign key constraint errors
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # Check if it's a foreign key violation
        if "FOREIGN KEY" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid foreign key provided. Please check your input."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred."
            )

    db.refresh(lead)
    return {"message": "Lead updated successfully", "lead": lead}

@real_estate_router.get("/domains")
def get_all_domains(db: Session = Depends(get_db)):
    # Fetch only the company domains
    results = db.query(CompanyInfo.company_domain).all()
    
    # Flatten the list of tuples to a list of strings
    domains = [domain[0] for domain in results]

    return {"domains": domains}
