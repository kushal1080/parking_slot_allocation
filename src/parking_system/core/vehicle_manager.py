# src/parking_system/core/vehicle_manager.py
import sqlite3
from datetime import datetime
from parking_system.database.db import get_conn
from parking_system.security import audit, check_user_role
from parking_system.notifications import email_service, sms_service, push_service
from parking_system.payment import payment_gateway

# --- Vehicle Operations ---
def register_vehicle(license_plate, vehicle_type):
    with get_conn() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO vehicles (license_plate, vehicle_type, checked_in, slot_id) VALUES (?, ?, 0, NULL)",
                (license_plate, vehicle_type)
            )
            return {"license_plate": license_plate, "vehicle_type": vehicle_type, "checked_in": 0, "slot_id": None}
        except sqlite3.IntegrityError:
            return {"license_plate": license_plate, "vehicle_type": vehicle_type, "checked_in": 0, "slot_id": None}

def checkin_vehicle(license_plate, username="staff"):
    if not check_user_role(username, "Staff") and not check_user_role(username, "Admin"):
        raise Exception("Permission denied for check-in")

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT slot_id FROM vehicles WHERE license_plate=?", (license_plate,))
        row = cur.fetchone()
        if not row or row[0] is None:
            raise Exception("Vehicle not allocated to any slot")
        slot_id = row[0]

        cur.execute("UPDATE vehicles SET checked_in=1 WHERE license_plate=?", (license_plate,))
        cur.execute("UPDATE slots SET is_occupied=1, vehicle_plate=? WHERE id=?", (license_plate, slot_id))
        cur.execute("INSERT INTO vehicle_logs (license_plate, checkin_time, slot_id) VALUES (?, ?, ?)",
                    (license_plate, datetime.now().isoformat(), slot_id))

        # Notifications
        email_service.send_email_notification("user@example.com", "Vehicle Checked In", f"{license_plate} checked in")
        sms_service.send_sms_notification("+11111111", f"{license_plate} checked in")
        push_service.send_push_notification(username, f"{license_plate} checked in")

        # Audit log
        audit.log_admin_action({"username": username, "role": "Staff"}, "checkin", f"{license_plate} checked in")

        return {"license_plate": license_plate, "checked_in": 1, "slot_id": slot_id}

def checkout_vehicle(license_plate, amount=0, username="staff"):
    if not check_user_role(username, "Staff") and not check_user_role(username, "Admin"):
        raise Exception("Permission denied for checkout")

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT slot_id FROM vehicles WHERE license_plate=?", (license_plate,))
        row = cur.fetchone()
        if not row or row[0] is None:
            raise Exception("Vehicle not allocated to any slot")
        slot_id = row[0]

        cur.execute("UPDATE vehicles SET checked_in=0, slot_id=NULL WHERE license_plate=?", (license_plate,))
        cur.execute("UPDATE slots SET is_occupied=0, vehicle_plate=NULL WHERE id=?", (slot_id,))
        cur.execute("""
            UPDATE vehicle_logs
            SET checkout_time=?, amount=?
            WHERE license_plate=? AND checkout_time IS NULL
        """, (datetime.now().isoformat(), amount, license_plate))

        # Mock payment
        payment_gateway.process_payment(license_plate, amount, method="mock")

        # Notifications
        email_service.send_email_notification("user@example.com", "Vehicle Checked Out", f"{license_plate} checked out")
        sms_service.send_sms_notification("+11111111", f"{license_plate} checked out")
        push_service.send_push_notification(username, f"{license_plate} checked out")

        # Audit log
        audit.log_admin_action({"username": username, "role": "Staff"}, "checkout", f"{license_plate} checked out")

        return {"license_plate": license_plate, "checked_in": 0, "slot_id": None, "amount": amount}

# --- Utility Functions ---
def list_vehicles():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM vehicles")
        return [dict(row) for row in cur.fetchall()]
