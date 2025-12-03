import sqlite3, os, uuid, hashlib
from datetime import datetime
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "enterprise_db.db")

# bcrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def preprocess_password(password: str) -> bytes:
    """Return raw SHA-256 digest (32 bytes) safe for bcrypt."""
    return hashlib.sha256(password.encode("utf-8")).digest()

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

users = [
    ("Alice Weaver", "alice@weaver.com", "CEO", "alice353"),
    ("Bob Stone", "bob@stone.com", "Manager", "bobpass"),
    ("Charlie Ray", "charlie@ray.com", "Analyst", "charliepw"),
]

for name, email, role, password in users:
    user_id = str(uuid.uuid4())
    password_hash = pwd_context.hash(preprocess_password(password))
    c.execute("""
        INSERT OR IGNORE INTO users (id, name, email, role, password_hash, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, name, email, role, password_hash, datetime.now()))

employees = [
    ("John Doe", "Engineering", 75000, 5000),
    ("Jane Smith", "Marketing", 65000, 4000),
    ("Mike Johnson", "Finance", 80000, 6000),
]

for name, department, salary, bonus in employees:
    emp_id = str(uuid.uuid4())
    c.execute("""
        INSERT OR IGNORE INTO employees_comp (id, name, department, salary, bonus, last_updated)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (emp_id, name, department, salary, bonus, datetime.now()))

conn.commit()
conn.close()
print("Seed data inserted successfully.")