from sqlalchemy import Column, Integer, String, ForeignKey, DateTime , Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True, nullable=True)
    company_domain = Column(String(100), nullable=True)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(50), unique=True, nullable=True)
    email = Column(String(50), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    gender = Column(String(10), nullable=True)
    date_added = Column(DateTime, nullable=False)

    # Add relationship to Lead
    leads = relationship("Lead", back_populates="assigned_user")
    role_mappings = relationship("UserRoleMapping", back_populates="user")

   

class Lead(Base):
    __tablename__ = "leads_info"

    lead_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    lead_phone = Column(String, unique=True, nullable=False)
    lead_stage = Column(Integer, ForeignKey("leads_stage.id"), nullable=False)
    lead_status = Column(Integer, ForeignKey("leads_status.id"), nullable=False)
    lead_type = Column(Integer, ForeignKey("lead_type.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("user_info.id"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    company_domain = Column(String, nullable=False)  # Added column


    # Relationships
    assigned_user = relationship("User", back_populates="leads")
    lead_stage_details = relationship("LeadStage", back_populates="leads")
    lead_status_details = relationship("LeadStatus", back_populates="leads")
    lead_type_details = relationship("LeadType", back_populates="leads")
    calls = relationship("ClientCall", back_populates="lead")
    meetings = relationship("ClientMeeting", back_populates="lead")
class LeadStage(Base):
    __tablename__ = "leads_stage"

    id = Column(Integer, primary_key=True, index=True)
    company_domain = Column(String, nullable=False)
    lead_stage = Column(String, nullable=False)
    date_added = Column(DateTime, nullable=False)
    is_assigned = Column(Boolean, nullable=False, default=False)
    is_not_assigned = Column(Boolean, nullable=False, default=False)
    is_action_taken = Column(Boolean, nullable=False, default=False)

    # Relationship to leads (if applicable)
    leads = relationship("Lead", back_populates="lead_stage_details")

class LeadStatus(Base):
    __tablename__ = "leads_status"

    id = Column(Integer, primary_key=True, index=True)
    status_name = Column(String, nullable=False)

    # Relationship with leads
    leads = relationship("Lead", back_populates="lead_status_details")

class LeadType(Base):
    __tablename__ = "lead_type"

    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String, nullable=False)

    # Relationship with leads
    leads = relationship("Lead", back_populates="lead_type_details")


class ClientCall(Base):
    __tablename__ = "client_calls"

    call_id = Column(Integer, primary_key=True, index=True)  # Primary key
    lead_id = Column(Integer, ForeignKey("leads_info.lead_id"), nullable=False)
    call_date = Column(DateTime, nullable=False, default=func.now())  # Default to current timestamp
    date_added = Column(DateTime, nullable=False, default=func.now())  # Default to current timestamp
    assigned_to = Column(Integer, nullable=True)  # Optional assigned user ID
    company_domain = Column(String(100), nullable=True)  # Optional company domain
    call_status = Column(Integer, nullable=True)  # Status of the call

    # Relationship to Lead
    lead = relationship("Lead", back_populates="calls")


class ClientMeeting(Base):
    __tablename__ = "client_meetings"

    meeting_id = Column(Integer, primary_key=True, index=True)  # Primary key
    lead_id = Column(Integer, ForeignKey("leads_info.lead_id"), nullable=False)
    meeting_date = Column(DateTime, nullable=False, default=func.now())  # Default to current timestamp
    date_added = Column(DateTime, nullable=False, default=func.now())  # Default to current timestamp
    assigned_to = Column(Integer, nullable=True)  # Optional assigned user ID
    company_domain = Column(String(100), nullable=True)  # Optional company domain
    meeting_status = Column(Integer, nullable=True)  # Status of the meeting

    # Relationship to Lead
    lead = relationship("Lead", back_populates="meetings")



class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    company_domain = Column(String(100), ForeignKey("company_info.company_domain"), nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)  # Reference to the `modules` table
    name = Column(String(50), nullable=False)

    # Relationships
    permissions = relationship("UserRolePermission", back_populates="role")
    module = relationship("Module", backref="roles")  # Relationship with `Module`
    user_mappings = relationship("UserRoleMapping", back_populates="role")


class UserRolePermission(Base):
    __tablename__ = "user_role_permissions"

    role_id = Column(Integer, ForeignKey("user_roles.id"), primary_key=True, index=True)  # Role ID
    permission_id = Column(Integer, nullable=True)  # Permission ID (if applicable)
    module_id = Column(Integer, nullable=True)  # Module ID
    feature_id = Column(Integer, nullable=True)  # Feature ID
    d_read = Column(Boolean, nullable=True)  # Read permission
    d_write = Column(Boolean, nullable=True)  # Write permission
    d_edit = Column(Boolean, nullable=True)  # Edit permission
    d_delete = Column(Boolean, nullable=True)  # Delete permission

    # Relationship to UserRole
    role = relationship("UserRole", back_populates="permissions")

class UserRoleMapping(Base):
    __tablename__ = "user_role_mapping"

    user_id = Column(Integer, ForeignKey("user_info.id"), primary_key=True, nullable=False)
    role_id = Column(Integer, ForeignKey("user_roles.id"), primary_key=True, nullable=False)

    # Relationships
    user = relationship("User", back_populates="role_mappings")
    role = relationship("UserRole", back_populates="user_mappings")


class CompanyInfo(Base):
    __tablename__ = "company_info"

    company_domain = Column(String(100), primary_key=True)
    name = Column(String(100), nullable=True)
    field = Column(String(100), nullable=True)
    address = Column(String(255), nullable=True)
    country = Column(String(50), nullable=True)
    telephone_number = Column(String(50), nullable=True)
    date_added = Column(DateTime, nullable=False)


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    name = Column(String(255), nullable=False)  # Module name, e.g., 'REAL_ESTATE'
    display_name = Column(String(255), nullable=True)  # Optional display name
    description = Column(String(255), nullable=True)  # Optional description
    available = Column(Boolean, nullable=True)  # Whether the module is available
    comming_on = Column(DateTime, nullable=True)  # Date when the module becomes available
    color = Column(String(50), nullable=True)  # Optional color associated with the module
    url = Column(String(255), nullable=True)  # URL or path for the module
