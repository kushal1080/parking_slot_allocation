#!/usr/bin/env python3
import random
from parking_system.database.db import init_db, get_conn
from parking_system.core import slot_manager, vehicle_manager

# Initialize DB safely
init_db()

def print_db_state():
    with get_conn() as conn:
        cur = conn.cursor()
        print("\n=== DATABASE STATE ===")
        print("\n--- Slots ---")
        cur.execute("SELECT * FROM slots")
        for row in cur.fetchall():
            print(dict(row))
        print("\n--- Vehicles ---")
        cur.execute("SELECT * FROM vehicles")
        for row in cur.fetchall():
            print(dict(row))
        print("=====================\n")

# Safe helpers
def safe_create_slot(slot_type, level):
    existing_slots = slot_manager.list_slots()
    for s in existing_slots:
        if s['slot_type'] == slot_type and s['level'] == level:
            return s
    return slot_manager.create_slot(slot_type, level)

def safe_register_vehicle(license_plate, vehicle_type):
    existing_vehicles = vehicle_manager.list_vehicles()
    for v in existing_vehicles:
        if v['license_plate'] == license_plate:
            return v
    return vehicle_manager.register_vehicle(license_plate, vehicle_type)

def safe_allocate_vehicle(license_plate):
    vehicles = vehicle_manager.list_vehicles()
    for v in vehicles:
        if v['license_plate'] == license_plate and v['slot_id'] is not None:
            return v
    return slot_manager.allocate_slot(license_plate)

def safe_checkin_vehicle(license_plate):
    vehicles = vehicle_manager.list_vehicles()
    for v in vehicles:
        if v['license_plate'] == license_plate and v['checked_in']:
            return v
    return vehicle_manager.checkin_vehicle(license_plate)

def safe_checkout_vehicle(license_plate, amount):
    vehicles = vehicle_manager.list_vehicles()
    for v in vehicles:
        if v['license_plate'] == license_plate and not v['checked_in']:
            return v
    return vehicle_manager.checkout_vehicle(license_plate, amount)

def main():
    # Phase 2 test data
    slots = [
        {"slot_type": "compact", "level": 1},
        {"slot_type": "large", "level": 1}
    ]
    vehicles = [
        {"license_plate": "ABC123", "vehicle_type": "Car"},
        {"license_plate": "XYZ789", "vehicle_type": "Truck"}
    ]

    # Create slots
    for s in slots:
        slot = safe_create_slot(s['slot_type'], s['level'])
        print(f"Slot created/existing: {slot}")

    # Register vehicles
    for v in vehicles:
        vehicle = safe_register_vehicle(v['license_plate'], v['vehicle_type'])
        print(f"Vehicle registered/existing: {vehicle}")

    print_db_state()

    # Allocate slots
    for v in vehicles:
        allocation = safe_allocate_vehicle(v['license_plate'])
        print(f"Vehicle allocated: {allocation}")

    # Check-in all vehicles
    for v in vehicles:
        checkin = safe_checkin_vehicle(v['license_plate'])
        print(f"Vehicle checked-in: {checkin}")

    # Simulate check-outs with random amounts for revenue
    for v in vehicles:
        amount = random.choice([50, 75, 100, 150])  # Example charges
        checkout = safe_checkout_vehicle(v['license_plate'], amount)
        print(f"Vehicle checked-out: {checkout}")

    print_db_state()

if __name__ == "__main__":
    main()
