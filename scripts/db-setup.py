import sqlite3
from datetime import datetime


conn = sqlite3.connect('enterprise_db.db')

c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS employees_comp (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        salary REAL NOT NULL,
        bonus REAL NOT NULL,
        last_updated TEXT NOT NULL
    )
''')


c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
''')
          

# Create 'access_logs' table
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
        
conn.commit()
# conn.close()