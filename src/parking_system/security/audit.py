"""
Audit logging module
Tracks sensitive and security-critical actions
"""

from datetime import datetime
from typing import Optional


def log_action(
    user_id: Optional[str],
    action: str,
    resource: Optional[str] = None,
    status: str = "SUCCESS"
) -> None:
    """
    Central audit logger

    Args:
        user_id: ID of the acting user
        action: Action performed
        resource: Optional resource identifier
        status: SUCCESS / FAILURE
    """

    timestamp = datetime.utcnow().isoformat()

    log_entry = {
        "timestamp": timestamp,
        "user_id": user_id,
        "action": action,
        "resource": resource,
        "status": status,
    }

    # For now: console log
    # Later: DB / file / SIEM
    print(f"[AUDIT] {log_entry}")
