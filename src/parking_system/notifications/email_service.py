# src/parking_system/notifications/email_service.py
def send_email_notification(user_email: str, subject: str, message: str):
    print(f"[Email] To: {user_email}, Subject: {subject}, Message: {message}")
