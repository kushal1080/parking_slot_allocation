from parking_system.database.db import get_conn

def register_vehicle(license_plate: str, vehicle_type: str) -> dict:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO vehicles (license_plate, vehicle_type) VALUES (?, ?)",
            (license_plate, vehicle_type)
        )
        cur.execute("SELECT * FROM vehicles WHERE license_plate=?", (license_plate,))
        return dict(cur.fetchone())

def list_vehicles() -> list:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM vehicles")
        return [dict(r) for r in cur.fetchall()]

def checkin_vehicle(license_plate: str) -> dict:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM vehicles WHERE license_plate=?", (license_plate,))
        vehicle = cur.fetchone()
        if not vehicle:
            raise ValueError("Vehicle not found")
        if vehicle["checked_in"]:
            raise ValueError("Vehicle already checked in")
        cur.execute("UPDATE vehicles SET checked_in=1 WHERE license_plate=?", (license_plate,))
        cur.execute("SELECT * FROM vehicles WHERE license_plate=?", (license_plate,))
        return dict(cur.fetchone())

def checkout_vehicle(license_plate: str) -> dict:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM vehicles WHERE license_plate=?", (license_plate,))
        vehicle = cur.fetchone()
        if not vehicle or not vehicle["checked_in"]:
            raise ValueError("Vehicle not checked in")
        # Free slot
        slot_id = vehicle["slot_id"]
        if slot_id:
            cur.execute(
                "UPDATE slots SET is_occupied=0, vehicle_plate=NULL WHERE id=?",
                (slot_id,)
            )
        # Check out
        cur.execute(
            "UPDATE vehicles SET checked_in=0, slot_id=NULL WHERE license_plate=?",
            (license_plate,)
        )
        cur.execute("SELECT * FROM vehicles WHERE license_plate=?", (license_plate,))
        return dict(cur.fetchone())

# CLI helpers
def register_vehicle_cli():
    plate = input("Enter license plate: ")
    vtype = input("Enter vehicle type: ")
    vehicle = register_vehicle(plate, vtype)
    print(f"Registered: {vehicle}")

def list_vehicles_cli():
    vehicles = list_vehicles()
    for v in vehicles:
        print(v)

def checkin_vehicle_cli():
    plate = input("Enter license plate to check-in: ")
    vehicle = checkin_vehicle(plate)
    print(f"Checked-in: {vehicle}")

def checkout_vehicle_cli():
    plate = input("Enter license plate to check-out: ")
    vehicle = checkout_vehicle(plate)
    print(f"Checked-out: {vehicle}")
