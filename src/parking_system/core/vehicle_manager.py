import sqlite3
from datetime import datetime

from parking_system.database.db import get_conn
from parking_system.security import log_action, check_user_role
from parking_system.notifications import (
    send_email_notification,
    send_sms_notification,
    send_push_notification,
)
from parking_system.payment import payment_gateway


# --------------------------------------------------
# Vehicle Operations
# --------------------------------------------------

def register_vehicle(license_plate: str, vehicle_type: str):
    with get_conn() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO vehicles (license_plate, vehicle_type, checked_in, slot_id)
                VALUES (?, ?, 0, NULL)
                """,
                (license_plate, vehicle_type),
            )

            log_action(
                user_id=None,
                action="REGISTER_VEHICLE",
                resource=license_plate,
            )

            return {
                "license_plate": license_plate,
                "vehicle_type": vehicle_type,
                "checked_in": 0,
                "slot_id": None,
            }

        except sqlite3.IntegrityError:
            # Vehicle already exists → idempotent behavior
            return {
                "license_plate": license_plate,
                "vehicle_type": vehicle_type,
                "checked_in": 0,
                "slot_id": None,
            }


def checkin_vehicle(license_plate: str, username: str = "staff"):
    if not (
        check_user_role(username, "Staff")
        or check_user_role(username, "Admin")
    ):
        raise PermissionError("Permission denied for check-in")

    with get_conn() as conn:
        cur = conn.cursor()

        cur.execute(
            "SELECT slot_id FROM vehicles WHERE license_plate=?",
            (license_plate,),
        )
        row = cur.fetchone()

        if not row or row["slot_id"] is None:
            raise ValueError("Vehicle not allocated to any slot")

        slot_id = row["slot_id"]

        cur.execute(
            "UPDATE vehicles SET checked_in=1 WHERE license_plate=?",
            (license_plate,),
        )
        cur.execute(
            """
            UPDATE slots
            SET is_occupied=1, vehicle_plate=?
            WHERE id=?
            """,
            (license_plate, slot_id),
        )
        cur.execute(
            """
            INSERT INTO vehicle_logs (license_plate, checkin_time, slot_id)
            VALUES (?, ?, ?)
            """,
            (license_plate, datetime.now().isoformat(), slot_id),
        )

        # Notifications
        send_email_notification(
            "user@example.com",
            "Vehicle Checked In",
            f"{license_plate} checked in",
        )
        send_sms_notification(
            "+11111111",
            f"{license_plate} checked in",
        )
        send_push_notification(
            username,
            f"{license_plate} checked in",
        )

        # Audit log
        log_action(
            user_id=username,
            action="CHECKIN_VEHICLE",
            resource=license_plate,
        )

        return {
            "license_plate": license_plate,
            "checked_in": 1,
            "slot_id": slot_id,
        }


def checkout_vehicle(
    license_plate: str,
    amount: float = 0,
    username: str = "staff",
):
    if not (
        check_user_role(username, "Staff")
        or check_user_role(username, "Admin")
    ):
        raise PermissionError("Permission denied for checkout")

    with get_conn() as conn:
        cur = conn.cursor()

        cur.execute(
            "SELECT slot_id FROM vehicles WHERE license_plate=?",
            (license_plate,),
        )
        row = cur.fetchone()

        if not row or row["slot_id"] is None:
            raise ValueError("Vehicle not allocated to any slot")

        slot_id = row["slot_id"]

        cur.execute(
            """
            UPDATE vehicles
            SET checked_in=0, slot_id=NULL
            WHERE license_plate=?
            """,
            (license_plate,),
        )
        cur.execute(
            """
            UPDATE slots
            SET is_occupied=0, vehicle_plate=NULL
            WHERE id=?
            """,
            (slot_id,),
        )
        cur.execute(
            """
            UPDATE vehicle_logs
            SET checkout_time=?, amount=?
            WHERE license_plate=? AND checkout_time IS NULL
            """,
            (datetime.now().isoformat(), amount, license_plate),
        )

        # Payment
        payment_gateway.process_payment(
            license_plate,
            amount,
            method="mock",
        )

        # Notifications
        send_email_notification(
            "user@example.com",
            "Vehicle Checked Out",
            f"{license_plate} checked out",
        )
        send_sms_notification(
            "+11111111",
            f"{license_plate} checked out",
        )
        send_push_notification(
            username,
            f"{license_plate} checked out",
        )

        # Audit log
        log_action(
            user_id=username,
            action="CHECKOUT_VEHICLE",
            resource=license_plate,
        )

        return {
            "license_plate": license_plate,
            "checked_in": 0,
            "slot_id": None,
            "amount": amount,
        }


# --------------------------------------------------
# Utility Functions
# --------------------------------------------------

def list_vehicles():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM vehicles")
        return [dict(row) for row in cur.fetchall()]
