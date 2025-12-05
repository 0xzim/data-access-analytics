# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from typing import List
import os
import uuid

from .auth import router as auth_router
from .database import Base, engine, get_db
from . import models
from .schemas import AccessApprovalRequest, AccessApprovalResponse, ApproveAccessRequest, EmployeeCompResponse
from app import schemas   # <-- NEW import

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cloud Data Access Monitoring System")
app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "Welcome to the Cloud Data Access Monitoring Project"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# app/main.py (inside get_employees_comp)
@app.get("/employees_comp", response_model=List[EmployeeCompResponse])
def get_employees_comp(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Baseline role check
    if current_user.role not in ["CEO", "Manager"]:
        # Check time-based approval
        approval = db.query(models.AccessApproval).filter(
            models.AccessApproval.user_id == current_user.id,
            models.AccessApproval.route == "employees_comp",
            models.AccessApproval.expires_at > datetime.now(UTC)
        ).first()

        if not approval:
            # Log unauthorized attempt
            log = models.AccessLog(
                user_id=current_user.id,
                action="view_employees_comp",
                status="unauthorized",
                timestamp=datetime.now(UTC)
            )
            db.add(log)
            db.commit()
            raise HTTPException(status_code=403, detail="Access not approved or approval expired")

    # Authorized or approved
    employees = db.query(models.Employee).all()

    log = models.AccessLog(
        user_id=current_user.id,
        action="view_employees_comp",
        status="success",
        timestamp=datetime.now(UTC)
    )
    db.add(log)
    db.commit()
    return employees

@app.post("/request_access", response_model=schemas.AccessApprovalResponse)
def request_access(
    body: schemas.AccessApprovalRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    approval = models.AccessApproval(
        id=str(uuid.uuid4()),
        user_id=body.user_id,        # requester’s ID
        route=body.route,
        approved_by=None,
        created_at=datetime.now(UTC),
        expires_at=None              # empty until approved
    )
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return approval



@app.post("/approve_access", response_model=schemas.AccessApprovalResponse)
def approve_access(
    body: schemas.ApproveAccessRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Only CEO/Manager can approve
    if current_user.role not in ["CEO", "Manager"]:
        raise HTTPException(status_code=403, detail="Not authorized to approve access")

    approval = db.query(models.AccessApproval).filter_by(id=body.approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found")

    approval.approved_by = current_user.id
    approval.expires_at = datetime.now(UTC) + timedelta(hours=body.hours)

    db.commit()
    db.refresh(approval)
    return approval


