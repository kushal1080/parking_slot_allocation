# src/parking_system/security/auth.py

from datetime import datetime

# ---------------------------
# Phase 5 in-memory user store
# ---------------------------
_USERS = {
    "admin": {"password": "admin123", "roles": {"Admin"}},
    "staff": {"password": "staff123", "roles": {"Staff"}},
    "system": {"password": "system", "roles": {"Admin"}},
}

# ---------------------------
# Authentication Functions
# ---------------------------

def login_user(username: str, password: str):
    """
    Authenticate user credentials.
    Phase 5: in-memory validation (Phase 6 → hashed + DB)
    Returns single role for Phase 5 demo compatibility.
    """
    user = _USERS.get(username)
    if not user:
        raise ValueError(f"User '{username}' does not exist")

    if user["password"] != password:
        raise PermissionError("Invalid credentials")

    # Take first role (Phase 5 demo requires singular 'role')
    role = list(user["roles"])[0]

    return {
        "username": username,
        "role": role,
        "login_time": datetime.utcnow().isoformat()
    }


def logout_user(username: str):
    """
    Placeholder for session / token invalidation.
    """
    # Here you could clear session or token cache in future
    return True


def check_user_role(username: str, role: str) -> bool:
    """
    Role-Based Access Control check.
    Returns True if user has specified role.
    """
    user = _USERS.get(username)
    if not user:
        return False
    return role in user["roles"]
