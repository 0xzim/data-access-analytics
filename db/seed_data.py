import uuid
import hashlib
from datetime import datetime, UTC
from passlib.context import CryptContext
from dotenv import load_dotenv

from app.database import SessionLocal
from app import models

# Load environment variables
load_dotenv()

# bcrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def preprocess_password(password: str) -> bytes:
    """Return raw SHA-256 digest (32 bytes) safe for bcrypt."""
    return hashlib.sha256(password.encode("utf-8")).digest()

def seed_data():
    db = SessionLocal()

    # --- Users ---
    users = [
        ("Alice Weaver", "alice@corp.com", "CEO", "Alice353!"),
        ("Bob Stone", "bob@corp.com", "Manager", "BobPass#1"),
        ("Charlie Ray", "charlie@corp.com", "Software Engineer", "Char!ie_pw"),
        ("Diana Prince", "diana@corp.com", "Operations Manager", "D!ana2025$"),
        ("Ethan Hunt", "ethan@corp.com", "Data Analyst", "Eth@n*Secure"),
        ("Fiona Clark", "fiona@corp.com", "HR Officer", "F!ona_HR@123"),
        ("George Miles", "george@corp.com", "Accountant", "Geo#Miles99"),
        ("Hannah Lee", "hannah@corp.com", "Data Scientist", "Han!ah_pw$"),
        ("Ian Wright", "ian@corp.com", "Treasurer", "IanWright@2025"),
        ("Julia Chen", "julia@corp.com", "Service Desk", "Ju!iaC#en88"),
    ]

    for name, email, role, password in users:
        # Check for duplicates by email
        existing = db.query(models.User).filter_by(email=email).first()
        if existing:
            continue

        user = models.User(
            id=str(uuid.uuid4()),
            name=name,
            email=email,
            role=role,
            password_hash=pwd_context.hash(preprocess_password(password)),
            created_at=datetime.now(UTC)
        )
        db.add(user)

    # --- Employees ---
    employees = [
        ("Alice Weaver", "Executive", 150000, 20000),
        ("Bob Stone", "Operations", 95000, 10000),
        ("Charlie Ray", "Engineering", 85000, 7000),
        ("Diana Prince", "Operations", 90000, 8000),
        ("Ethan Hunt", "Analytics", 78000, 6000),
        ("Fiona Clark", "Human Resources", 70000, 5000),
        ("George Miles", "Finance", 82000, 6000),
        ("Hannah Lee", "Data Science", 95000, 9000),
        ("Ian Wright", "Finance", 88000, 7000),
        ("Julia Chen", "IT Support", 60000, 4000),
    ]

    for name, department, salary, bonus in employees:
        # Check for duplicates by name + department
        existing = db.query(models.Employee).filter_by(name=name, department=department).first()
        if existing:
            continue

        emp = models.Employee(
            id=str(uuid.uuid4()),
            name=name,
            department=department,
            salary=salary,
            bonus=bonus,
            last_updated=datetime.now(UTC)
        )
        db.add(emp)

    db.commit()
    db.close()
    print("✅ Seed data inserted successfully.")

if __name__ == "__main__":
    seed_data()