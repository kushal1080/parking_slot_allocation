from parking_system.database.db import get_conn

def create_slot(slot_type: str, level: int) -> dict:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO slots (slot_type, level) VALUES (?, ?)",
            (slot_type, level)
        )
        slot_id = cur.lastrowid
        cur.execute("SELECT * FROM slots WHERE id=?", (slot_id,))
        row = cur.fetchone()
        return dict(row)

def list_slots() -> list:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM slots")
        return [dict(r) for r in cur.fetchall()]

def allocate_slot(vehicle_plate: str) -> dict:
    with get_conn() as conn:
        cur = conn.cursor()
        # Check vehicle exists
        cur.execute("SELECT * FROM vehicles WHERE license_plate=?", (vehicle_plate,))
        vehicle = cur.fetchone()
        if not vehicle:
            raise ValueError("Vehicle does not exist")
        # Find first available slot
        cur.execute("SELECT * FROM slots WHERE is_occupied=0 ORDER BY id LIMIT 1")
        slot = cur.fetchone()
        if not slot:
            raise ValueError("No available slots")
        # Assign slot
        cur.execute(
            "UPDATE slots SET is_occupied=1, vehicle_plate=? WHERE id=?",
            (vehicle_plate, slot["id"])
        )
        cur.execute(
            "UPDATE vehicles SET slot_id=? WHERE license_plate=?",
            (slot["id"], vehicle_plate)
        )
        cur.execute("SELECT * FROM slots WHERE id=?", (slot["id"],))
        return dict(cur.fetchone())

# CLI helpers
def create_slot_cli():
    slot_type = input("Enter slot type: ")
    level = int(input("Enter level: "))
    slot = create_slot(slot_type, level)
    print(f"Created slot: {slot}")

def list_slots_cli():
    slots = list_slots()
    for s in slots:
        print(s)

def allocate_slot_cli():
    plate = input("Enter vehicle plate: ")
    slot = allocate_slot(plate)
    print(f"Allocated: {slot}")
