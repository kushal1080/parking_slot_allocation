#!/usr/bin/env python3
"""
Phase 2 Full Backend Test Script
- Creates 2 slots
- Registers 2 vehicles
- Allocates slots
- Checks in/out
- Prints database state after each step
"""

import requests
import sqlite3
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"

DB_PATH = Path("src/parking_system/database/parking.db")

def print_db_state():
    print("\n=== DATABASE STATE ===")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    print("\n--- Slots ---")
    for row in cur.execute("SELECT * FROM slots"):
        print(dict(row))

    print("\n--- Vehicles ---")
    for row in cur.execute("SELECT * FROM vehicles"):
        print(dict(row))

    conn.close()
    print("=====================\n")


def main():
    # 1️⃣ Create Slots
    slots_payload = [
        {"slot_type": "compact", "level": 1},
        {"slot_type": "large", "level": 1}
    ]
    for payload in slots_payload:
        r = requests.post(f"{BASE_URL}/api/slots/", json=payload)
        print(f"Create slot {payload}: {r.status_code}, {r.json()}")

    print_db_state()

    # 2️⃣ Register Vehicles
    vehicles_payload = [
        {"license_plate": "ABC123", "vehicle_type": "Car"},
        {"license_plate": "XYZ789", "vehicle_type": "Truck"}
    ]
    for payload in vehicles_payload:
        r = requests.post(f"{BASE_URL}/api/vehicles/", json=payload)
        print(f"Register vehicle {payload}: {r.status_code}, {r.json()}")

    print_db_state()

    # 3️⃣ Allocate Slots
    for plate in ["ABC123", "XYZ789"]:
        r = requests.post(f"{BASE_URL}/api/slots/allocate/", json={"license_plate": plate})
        print(f"Allocate slot for {plate}: {r.status_code}, {r.json()}")

    print_db_state()

    # 4️⃣ Check-in Vehicles
    for plate in ["ABC123", "XYZ789"]:
        r = requests.post(f"{BASE_URL}/api/vehicles/checkin/", json={"license_plate": plate})
        print(f"Check-in {plate}: {r.status_code}, {r.json()}")

    print_db_state()

    # 5️⃣ Check-out Vehicles
    for plate in ["ABC123", "XYZ789"]:
        r = requests.post(f"{BASE_URL}/api/vehicles/checkout/", json={"license_plate": plate})
        print(f"Check-out {plate}: {r.status_code}, {r.json()}")

    print_db_state()

    # 6️⃣ Final GET checks
    r_slots = requests.get(f"{BASE_URL}/api/slots/")
    r_vehicles = requests.get(f"{BASE_URL}/api/vehicles/")
    print(f"\nFinal GET /api/slots/: {r_slots.status_code}, {r_slots.json()}")
    print(f"Final GET /api/vehicles/: {r_vehicles.status_code}, {r_vehicles.json()}")


if __name__ == "__main__":
    main()
