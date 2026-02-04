# src/parking_system/payment/payment_gateway.py
from parking_system.database.db import get_conn
from datetime import datetime

def process_payment(license_plate: str, amount: float, method: str = "mock"):
    # Create payments table if not exists
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_plate TEXT,
            amount REAL,
            method TEXT,
            timestamp TEXT
        )
        """)
        cur.execute(
            "INSERT INTO payments (license_plate, amount, method, timestamp) VALUES (?, ?, ?, ?)",
            (license_plate, amount, method, datetime.now().isoformat())
        )
    print(f"[Payment] Vehicle {license_plate} paid {amount} via {method}")
    return True
