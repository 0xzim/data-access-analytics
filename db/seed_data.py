import sqlite3
from datetime import datetime

# Connect to the same database
conn = sqlite3.connect('enterprise_db.db')
c = conn.cursor()

# --- Insert sample employees ---
employees = [
    ("Alice Johnson", "Finance", 72000, 5000, datetime.now().isoformat()),
    ("Bob Smith", "Engineering", 85000, 7000, datetime.now().isoformat()),
    ("Charlie Brown", "HR", 60000, 4000, datetime.now().isoformat()),
    ("Diana Prince", "Engineering", 95000, 10000, datetime.now().isoformat())
]
c.executemany(
    "INSERT INTO employees_comp (name, department, salary, bonus, last_updated) VALUES (?, ?, ?, ?, ?)",
    employees
)

# --- Insert sample users ---
users = [
    ("Alice Admin", "admin", datetime.now().isoformat()),
    ("Ben Analyst", "analyst", datetime.now().isoformat()),
    ("Cindy Intern", "intern", datetime.now().isoformat())
]
c.executemany(
    "INSERT INTO users (name, role, created_at) VALUES (?, ?, ?)",
    users
)

# --- Simulate access logs ---
logs = [
    # Successful authorized access
    (1, datetime.now().isoformat(), "READ employees_comp", "SUCCESS"),
    (2, datetime.now().isoformat(), "READ employees_comp", "SUCCESS"),
    
    # Unauthorized attempt
    (3, datetime.now().isoformat(), "READ employees_comp", "FAILED_UNAUTHORIZED"),
    
    # Admin updating employee data
    (1, datetime.now().isoformat(), "UPDATE employees_comp", "SUCCESS")
]
c.executemany(
    "INSERT INTO access_logs (user_id, timestamp, action, status) VALUES (?, ?, ?, ?)",
    logs
)

# Commit and close
conn.commit()
conn.close()

print("✅ Sample data inserted successfully!")
