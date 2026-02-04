# src/parking_system/security/auth.py
from parking_system.database.db import get_conn
import hashlib

# --- User registration & authentication ---
def register_user(username: str, password: str, role: str):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    with get_conn() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, hashed, role)
            )
        except:
            pass  # user exists

def login_user(username: str, password: str):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE username=? AND password=?", (username, hashed))
        row = cur.fetchone()
        if row:
            return {"username": username, "role": row[0]}
        return None

def logout_user(username: str):
    # Placeholder for session handling
    print(f"{username} logged out.")

# --- Role check function (needed by vehicle_manager.py) ---
def check_user_role(username: str, role: str) -> bool:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE username=?", (username,))
        row = cur.fetchone()
        return row and row[0] == role
