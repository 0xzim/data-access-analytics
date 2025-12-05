from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
import uuid
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(String(50), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    logs = relationship("AccessLog", back_populates="user")

class Employee(Base):
    __tablename__ = "employees_comp"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    salary = Column(Float, nullable=False)
    bonus = Column(Float, nullable=False)
    last_updated = Column(DateTime, default=datetime.now(UTC))

class AccessLog(Base):
    __tablename__ = "access_logs"
    log_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.now(UTC))
    action = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    user = relationship("User", back_populates="logs")

class AccessApproval(Base):
    __tablename__ = "access_approvals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    route = Column(String(100), nullable=False)
    approved_by = Column(String(36), ForeignKey("users.id"), nullable=True)   # can be NULL
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    expires_at = Column(DateTime, nullable=True) 

