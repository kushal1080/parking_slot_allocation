# src/parking_system/core/slot_manager.py
from parking_system.database.db import get_conn

def create_slot(slot_type: str, level: int) -> dict:
    """
    Create a new slot in the DB and return the slot dict.
    """
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO slots (slot_type, level, is_occupied, vehicle_plate) VALUES (?, ?, 0, NULL)",
            (slot_type, level)
        )
        slot_id = cur.lastrowid
        cur.execute("SELECT * FROM slots WHERE id=?", (slot_id,))
        return dict(cur.fetchone())


def list_slots() -> list:
    """
    Return all slots as a list of dicts.
    """
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM slots")
        return [dict(r) for r in cur.fetchall()]


def allocate_slot(vehicle_plate: str) -> dict:
    """
    Allocate the first available slot to a vehicle.
    """
    with get_conn() as conn:
        cur = conn.cursor()
        # Ensure vehicle exists
        cur.execute("SELECT * FROM vehicles WHERE license_plate=?", (vehicle_plate,))
        vehicle = cur.fetchone()
        if not vehicle:
            raise ValueError("Vehicle does not exist")
        # Find first free slot
        cur.execute("SELECT * FROM slots WHERE is_occupied=0 ORDER BY id LIMIT 1")
        slot = cur.fetchone()
        if not slot:
            raise ValueError("No available slots")
        slot_id = slot["id"]
        # Assign slot
        cur.execute(
            "UPDATE slots SET is_occupied=1, vehicle_plate=? WHERE id=?",
            (vehicle_plate, slot_id)
        )
        cur.execute(
            "UPDATE vehicles SET slot_id=? WHERE license_plate=?",
            (slot_id, vehicle_plate)
        )
        cur.execute("SELECT * FROM slots WHERE id=?", (slot_id,))
        return dict(cur.fetchone())


def set_slot_occupancy(slot_id: int, occupied: bool):
    """
    Update slot occupancy and clear vehicle_plate if empty.
    """
    with get_conn() as conn:
        cur = conn.cursor()
        vehicle_plate = None
        if occupied:
            cur.execute("SELECT vehicle_plate FROM slots WHERE id=?", (slot_id,))
            vehicle_plate = cur.fetchone()[0]
        cur.execute(
            "UPDATE slots SET is_occupied=?, vehicle_plate=? WHERE id=?",
            (1 if occupied else 0, vehicle_plate, slot_id)
        )
        conn.commit()
        return {"id": slot_id, "is_occupied": occupied, "vehicle_plate": vehicle_plate}


def get_slot_by_id(slot_id: int):
    """
    Fetch a slot by its ID.
    """
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM slots WHERE id=?", (slot_id,))
        row = cur.fetchone()
        return dict(row) if row else None
