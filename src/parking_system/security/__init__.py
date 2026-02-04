# Expose all security functionalities

from .auth import (
    login_user,
    logout_user,
    check_user_role,
    get_mock_users  # if you have mock users for testing
)

from .audit import (
    log_admin_action,
    get_audit_logs
)
