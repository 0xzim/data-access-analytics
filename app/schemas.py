from pydantic import BaseModel
from datetime import datetime


# --- Auth Schemas ---
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    user_id: str
    access_token: str
    token_type: str
    role: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        orm_mode = True


# --- Employee Compensation Schemas ---
class EmployeeCompResponse(BaseModel):
    id: str
    name: str
    department: str
    salary: int
    bonus: int
    last_updated: datetime

    class Config:
        orm_mode = True


class AccessApprovalRequest(BaseModel):
    user_id: str        # requester’s ID (from JWT or passed explicitly)
    route: str          # resource they want access to

class ApproveAccessRequest(BaseModel):
    approval_id: str    # ID of the pending approval request
    hours: int = 1      # duration in hours (default 1)

class AccessApprovalResponse(BaseModel):
    id: str
    user_id: str
    route: str
    approved_by: str | None   # nullable until approved
    created_at: datetime
    expires_at: datetime | None   # nullable until approved

    class Config:
        orm_mode = True

