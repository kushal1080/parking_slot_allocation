from parking_system.database.db import get_conn

def create_slot(slot_type: str, level: int):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO slots (slot_type, level) VALUES (?, ?)",
            (slot_type, level)
        )
        return dict(cur.execute(
            "SELECT * FROM slots WHERE id = last_insert_rowid()"
        ).fetchone())


def list_slots():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM slots")]


def register_vehicle(plate: str, vtype: str):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO vehicles (license_plate, vehicle_type) VALUES (?, ?)",
            (plate, vtype)
        )
        return {"license_plate": plate, "vehicle_type": vtype}


def allocate_slot(plate: str):
    with get_conn() as conn:
        cur = conn.cursor()

        vehicle = cur.execute(
            "SELECT * FROM vehicles WHERE license_plate = ?",
            (plate,)
        ).fetchone()
        if not vehicle:
            raise ValueError("Vehicle not registered")

        slot = cur.execute(
            "SELECT * FROM slots WHERE occupied = 0 LIMIT 1"
        ).fetchone()
        if not slot:
            raise ValueError("No available slots")

        cur.execute(
            "UPDATE slots SET occupied = 1, vehicle_plate = ? WHERE id = ?",
            (plate, slot["id"])
        )

        cur.execute(
            "UPDATE vehicles SET checked_in = 1 WHERE license_plate = ?",
            (plate,)
        )

        return dict(cur.execute(
            "SELECT * FROM slots WHERE id = ?",
            (slot["id"],)
        ).fetchone())


def checkout_vehicle(plate: str):
    with get_conn() as conn:
        cur = conn.cursor()

        slot = cur.execute(
            "SELECT * FROM slots WHERE vehicle_plate = ?",
            (plate,)
        ).fetchone()
        if not slot:
            raise ValueError("Vehicle not checked in")

        cur.execute(
            "UPDATE slots SET occupied = 0, vehicle_plate = NULL WHERE id = ?",
            (slot["id"],)
        )
        cur.execute(
            "UPDATE vehicles SET checked_in = 0 WHERE license_plate = ?",
            (plate,)
        )

        return {"released_slot": slot["id"]}
