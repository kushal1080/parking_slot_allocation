# src/parking_system/security/audit.py
from parking_system.database.db import get_conn
import time

def log_admin_action(user: dict, action: str, details: str):
    timestamp = int(time.time())
    with get_conn() as conn:
        cur = conn.cursor()
        # Create audit_logs table if not exists
        cur.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            user TEXT,
            role TEXT,
            action TEXT,
            details TEXT
        )
        """)
        cur.execute(
            "INSERT INTO audit_logs (timestamp, user, role, action, details) VALUES (?, ?, ?, ?, ?)",
            (timestamp, user["username"], user["role"], action, details)
        )
