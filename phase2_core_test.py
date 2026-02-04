#!/usr/bin/env python3
import sqlite3
from parking_system.database.db import init_db, get_conn
from parking_system.core import slot_manager, vehicle_manager

# Initialize DB (safe: creates tables if not exist)
init_db()

def print_db_state():
    conn = get_conn()
    cur = conn.cursor()
    print("\n=== DATABASE STATE ===")
    # Slots
    print("\n--- Slots ---")
    cur.execute("SELECT * FROM slots")
    for row in cur.fetchall():
        print(dict(zip([col[0] for col in cur.description], row)))
    # Vehicles
    print("\n--- Vehicles ---")
    cur.execute("SELECT * FROM vehicles")
    for row in cur.fetchall():
        print(dict(zip([col[0] for col in cur.description], row)))
    print("=====================\n")
    conn.close()

def safe_create_slot(slot_type, level):
    # Check if slot exists to avoid duplicates
    existing_slots = slot_manager.list_slots()
    for s in existing_slots:
        if s['slot_type'] == slot_type and s['level'] == level:
            print(f"Slot already exists: {s}")
            return s
    # Otherwise, create new
    slot = slot_manager.create_slot(slot_type, level)
    print(f"Created slot {slot_type}, level {level}: 200, {slot}")
    return slot

def safe_register_vehicle(license_plate, vehicle_type):
    # Check if vehicle exists
    existing_vehicles = vehicle_manager.list_vehicles()
    for v in existing_vehicles:
        if v['license_plate'] == license_plate:
            print(f"Vehicle already exists: {v}")
            return v
    # Otherwise, register
    vehicle = vehicle_manager.register_vehicle(license_plate, vehicle_type)
    print(f"Registered vehicle {license_plate}: 200, {vehicle}")
    return vehicle

def safe_allocate_vehicle(license_plate):
    vehicle = vehicle_manager.list_vehicles()
    for v in vehicle:
        if v['license_plate'] == license_plate and v['slot_id'] is not None:
            print(f"Vehicle {license_plate} already allocated to slot {v['slot_id']}")
            return v
    slot = slot_manager.allocate_slot(license_plate)
    print(f"Allocated slot for {license_plate}: 200, {slot}")
    return slot

def safe_checkin_vehicle(license_plate):
    v = vehicle_manager.list_vehicles()
    for vehicle in v:
        if vehicle['license_plate'] == license_plate and vehicle['checked_in']:
            print(f"Vehicle {license_plate} already checked-in")
            return vehicle
    vehicle = vehicle_manager.checkin_vehicle(license_plate)
    print(f"Checked-in {license_plate}: 200, {vehicle}")
    return vehicle

def safe_checkout_vehicle(license_plate):
    v = vehicle_manager.list_vehicles()
    for vehicle in v:
        if vehicle['license_plate'] == license_plate and not vehicle['checked_in']:
            print(f"Vehicle {license_plate} already checked-out")
            return vehicle
    vehicle = vehicle_manager.checkout_vehicle(license_plate)
    print(f"Checked-out {license_plate}: 200, {vehicle}")
    return vehicle

def main():
    # Phase 2 Test Data
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
        safe_create_slot(s['slot_type'], s['level'])

    print_db_state()

    # Register vehicles
    for v in vehicles:
        safe_register_vehicle(v['license_plate'], v['vehicle_type'])

    print_db_state()

    # Allocate slots
    for v in vehicles:
        safe_allocate_vehicle(v['license_plate'])

    print_db_state()

    # Check-in vehicles
    for v in vehicles:
        safe_checkin_vehicle(v['license_plate'])

    print_db_state()

    # Check-out vehicles
    for v in vehicles:
        safe_checkout_vehicle(v['license_plate'])

    print_db_state()

if __name__ == "__main__":
    main()

#run with python3 phase2_core_test.py
#rm src/parking_system/database/parking.db
'''
export PYTHONPATH=$(pwd)/src
python3 - <<EOF
from parking_system.database.db import init_db
init_db()
EOF
python3 phase2_core_test.py
'''
