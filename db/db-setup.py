import sqlite3
from datetime import datetime

# Connect to DB
conn = sqlite3.connect("enterprise_db.db")
c = conn.cursor()


# 1. USERS TABLE
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")


# 2. EMPLOYEE COMPENSATION DATA
c.execute("""
CREATE TABLE IF NOT EXISTS employees_comp (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary REAL NOT NULL,
    bonus REAL NOT NULL,
    last_updated TEXT NOT NULL
)
""")


# 3. ACCESS LOGS (who accessed what)
c.execute("""
CREATE TABLE IF NOT EXISTS access_logs (
    log_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    timestamp TEXT,
    action TEXT,
    status TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
""")


# 4. APPROVAL REQUESTS (workflow)
c.execute("""
CREATE TABLE IF NOT EXISTS approval_requests (
    request_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    dataset TEXT NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL, -- pending, approved, rejected
    requested_at TEXT NOT NULL,
    reviewed_at TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
""")

conn.commit()
conn.close()

print("Database setup complete.")
