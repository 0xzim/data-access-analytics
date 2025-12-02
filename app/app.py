import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect('enterprise_db.db')
c = conn.cursor()

# -------------------------------
# ROLE-BASED ACCESS PERMISSIONS
# -------------------------------
PERMISSIONS = {
    "admin": ["READ", "UPDATE"],
    "analyst": ["READ"],
    "intern": []   # cannot access sensitive table
}

# -------------------------------
# Helper: Get user role
# -------------------------------
def get_user_role(user_id):
    c.execute("SELECT role FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    return result[0] if result else None


# -------------------------------
# Log Access Attempt
# -------------------------------
def log_access(user_id, action, status):
    timestamp = datetime.now().isoformat()

    c.execute("""
        INSERT INTO access_logs (user_id, timestamp, action, status)
        VALUES (?, ?, ?, ?)
    """, (user_id, timestamp, action, status))

    conn.commit()


# -------------------------------
# Access Request Function
# -------------------------------
def request_access(user_id, action):
    role = get_user_role(user_id)

    if not role:
        print(f"❌ User {user_id} not found!")
        return

    action_type = action.split()[0]  # e.g., "READ employees_comp" → "READ"

    if action_type in PERMISSIONS.get(role, []):
        print(f"✅ Access GRANTED for user {user_id} ({role}) → {action}")
        log_access(user_id, action, "SUCCESS")
    else:
        print(f"🚫 Access DENIED for user {user_id} ({role}) → {action}")
        log_access(user_id, action, "FAILED_UNAUTHORIZED")


# -------------------------------
# Simulate Access Attempts
# -------------------------------
if __name__ == "__main__":
    print("\n=== Simulated Access Requests ===\n")

    request_access(1, "READ employees_comp")      # admin → success
    request_access(2, "UPDATE employees_comp")    # analyst → denied
    request_access(3, "READ employees_comp")      # intern → denied
    request_access(1, "UPDATE employees_comp")    # admin → success

    print("\nDone.")
