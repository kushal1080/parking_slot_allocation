# src/parking_system/notifications/sms_service.py
def send_sms_notification(phone: str, message: str):
    print(f"[SMS] To: {phone}, Message: {message}")
