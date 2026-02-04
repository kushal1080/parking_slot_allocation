#!/usr/bin/env python3
from parking_system.database.db import init_db, get_conn
from parking_system.core import slot_manager, vehicle_manager
from parking_system.analytics import reports, prediction
from datetime import datetime
import os

# -----------------------
# Helper functions
# -----------------------

def safe_create_slot(slot_type, level):
    """Create slot if not exists, else return existing."""
    existing = slot_manager.list_slots()
    for s in existing:
        if s['slot_type'] == slot_type and s['level'] == level:
            print(f"Slot created/existing: {s}")
            return s
    slot = slot_manager.create_slot(slot_type, level)
    print(f"Slot created/existing: {slot}")
    return slot

def safe_register_vehicle(license_plate, vehicle_type):
    """Register vehicle if not exists."""
    # Since we fixed list_vehicles in vehicle_manager
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM vehicles WHERE license_plate=?", (license_plate,))
        row = cur.fetchone()
        if row:
            vehicle = dict(row)
            print(f"Vehicle registered/existing: {vehicle}")
            return vehicle

        # Otherwise register
        vehicle = vehicle_manager.register_vehicle(license_plate, vehicle_type)
        print(f"Vehicle registered/existing: {vehicle}")
        return vehicle

def safe_allocate_vehicle(license_plate):
    """Allocate a slot to vehicle."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT slot_id FROM vehicles WHERE license_plate=?", (license_plate,))
        row = cur.fetchone()
        if row and row[0]:
            print(f"Vehicle allocated: {row}")
            return row
    slot = slot_manager.allocate_slot(license_plate)
    print(f"Vehicle allocated: {slot}")
    return slot

def safe_checkin_vehicle(license_plate):
    """Check-in vehicle safely."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT checked_in FROM vehicles WHERE license_plate=?", (license_plate,))
        row = cur.fetchone()
        if row and row[0]:
            print(f"Vehicle checked-in: {dict(row)}")
            return row
    vehicle = vehicle_manager.checkin_vehicle(license_plate)
    print(f"Vehicle checked-in: {vehicle}")
    return vehicle

def safe_checkout_vehicle(license_plate, amount=0):
    """Check-out vehicle safely."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT checked_in FROM vehicles WHERE license_plate=?", (license_plate,))
        row = cur.fetchone()
        if row and not row[0]:
            print(f"Vehicle checked-out: {dict(row)}")
            return row
    vehicle = vehicle_manager.checkout_vehicle(license_plate, amount)
    print(f"Vehicle checked-out: {vehicle}")
    return vehicle

# -----------------------
# Main Phase 3 flow
# -----------------------

def main():
    print("\n--- Phase 3: Parking Analytics & Prediction ---\n")

    # Step 1: Initialize DB
    init_db()

    # Step 2: Create sample slots and vehicles (Phase 2 setup)
    slots = [
        {"slot_type": "compact", "level": 1},
        {"slot_type": "large", "level": 1}
    ]
    vehicles = [
        {"license_plate": "ABC123", "vehicle_type": "Car"},
        {"license_plate": "XYZ789", "vehicle_type": "Truck"}
    ]

    for s in slots:
        safe_create_slot(s['slot_type'], s['level'])

    for v in vehicles:
        safe_register_vehicle(v['license_plate'], v['vehicle_type'])

    # Allocate slots
    for v in vehicles:
        safe_allocate_vehicle(v['license_plate'])

    # Check-in all vehicles
    for v in vehicles:
        safe_checkin_vehicle(v['license_plate'])

    # Check-out all vehicles with example amounts
    amounts = [50, 75]
    for i, v in enumerate(vehicles):
        safe_checkout_vehicle(v['license_plate'], amounts[i])

    # Step 3: Generate enhanced reports
    report_file = "phase3_report.xlsx"
    reports.generate_enhanced_report(report_file)

    # Step 4: Generate slot demand prediction for next 24 hours
    prediction_file = "slot_demand.xlsx"
    prediction.predict_slot_demand(prediction_file)

    print("\n--- Phase 3 Completed ---\n")

# -----------------------
# Entry point
# -----------------------

if __name__ == "__main__":
    main()
