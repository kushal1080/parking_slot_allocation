# src/parking_system/security/auth.py
import hashlib

# Mock users (in a real system, use secure DB)
USERS = {
    "admin": {"username": "admin", "password": hashlib.sha256("admin123".encode()).hexdigest(), "role": "Admin"},
    "staff": {"username": "staff", "password": hashlib.sha256("staff123".encode()).hexdigest(), "role": "Staff"},
    "user": {"username": "user", "password": hashlib.sha256("user123".encode()).hexdigest(), "role": "User"},
}

def login_user(username: str, password: str):
    user = USERS.get(username)
    if not user:
        return None
    if hashlib.sha256(password.encode()).hexdigest() == user["password"]:
        return user
    return None

def logout_user(username: str):
    # Mock logout
    return f"{username} logged out"

def check_user_role(username: str, role: str):
    user = USERS.get(username)
    return user and user["role"] == role
