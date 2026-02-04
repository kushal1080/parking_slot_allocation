# src/parking_system/notifications/push_service.py
def send_push_notification(user: str, message: str):
    print(f"[Push] To: {user}, Message: {message}")
