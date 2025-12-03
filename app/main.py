# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from typing import List
import os

from .auth import router as auth_router
from .database import Base, engine, get_db
from . import models
from .schemas import EmployeeCompResponse   # <-- NEW import

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

@app.get("/employees_comp", response_model=List[EmployeeCompResponse])   # <-- UPDATED
def get_employees_comp(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role not in ["CEO", "Manager"]:
        log = models.AccessLog(
            user_id=current_user.id,
            action="view_employees_comp",
            status="unauthorized",
            timestamp=datetime.utcnow()
        )
        db.add(log)
        db.commit()
        raise HTTPException(status_code=403, detail="Not authorized to view employee compensation data")

    employees = db.query(models.Employee).all()
    log = models.AccessLog(
        user_id=current_user.id,
        action="view_employees_comp",
        status="success",
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    return employees