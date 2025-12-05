# app/auth.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, UTC
import os, hashlib
from dotenv import load_dotenv

from .database import get_db
from .models import User
from .schemas import LoginRequest, LoginResponse   # <-- import schemas

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")
TOKEN_EXPIRE_HOURS = int(os.getenv("TOKEN_EXPIRE_HOURS", 1))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/auth", tags=["auth"])

def preprocess_password(password: str) -> bytes:
    """Return raw SHA-256 digest (32 bytes)."""
    return hashlib.sha256(password.encode("utf-8")).digest()

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not pwd_context.verify(preprocess_password(request.password), user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    expire = datetime.now(UTC) + timedelta(hours=TOKEN_EXPIRE_HOURS)
    payload = {"sub": user.id, "role": user.role, "exp": int(expire.timestamp())}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {
        "user_id": user.id,
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }