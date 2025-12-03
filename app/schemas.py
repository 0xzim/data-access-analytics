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
