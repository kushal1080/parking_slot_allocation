import sqlite3
from datetime import datetime
from parking_system.database.db import get_conn

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
            # Already exists
            return {"license_plate": license_plate, "vehicle_type": vehicle_type, "checked_in": 0, "slot_id": None}

def checkin_vehicle(license_plate):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT slot_id FROM vehicles WHERE license_plate=?", (license_plate,))
        row = cur.fetchone()
        if not row or row[0] is None:
            raise Exception("Vehicle not allocated to any slot")
        slot_id = row[0]

        cur.execute("UPDATE vehicles SET checked_in=1 WHERE license_plate=?", (license_plate,))
        cur.execute("UPDATE slots SET is_occupied=1, vehicle_plate=? WHERE id=?", (license_plate, slot_id))
        cur.execute("INSERT INTO vehicle_logs (license_plate, checkin_time) VALUES (?, ?)",
                    (license_plate, datetime.now().isoformat()))
        return {"license_plate": license_plate, "checked_in": 1, "slot_id": slot_id}

def checkout_vehicle(license_plate, amount=0):
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
        return {"license_plate": license_plate, "checked_in": 0, "slot_id": None, "amount": amount}

# --- Utility Functions (needed for Phase2_core_test.py) ---
def list_vehicles():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM vehicles")
        return [dict(row) for row in cur.fetchall()]
