# src/parking_system/payment/payment_gateway.py

def validate_payment_credentials(method: str) -> bool:
    """
    Mock credential validation.
    In real systems this would validate API keys / tokens.
    """
    allowed_methods = {"mock", "card", "upi"}
    return method in allowed_methods


def process_payment(license_plate: str, amount: float, method: str = "mock"):
    """
    Simulate payment processing.
    """
    if not validate_payment_credentials(method):
        raise ValueError(f"Invalid payment method: {method}")

    if amount < 0:
        raise ValueError("Payment amount cannot be negative")

    # Mock success
    return {
        "license_plate": license_plate,
        "amount": amount,
        "method": method,
        "status": "SUCCESS",
    }
