#!/usr/bin/env python3
import os
import threading
import time

# Set PYTHONPATH for proper module resolution
os.environ["PYTHONPATH"] = os.path.join(os.getcwd(), "src")

from parking_system.database.db import init_db
from parking_system.core import vehicle_manager, slot_manager
from parking_system.analytics import reports, prediction
from parking_system.io_integration import (
    update_slots_from_sensors,
    simulate_camera_checkins,
    publish_loop
)

# -----------------------------
# Phase 2: Simulation
# -----------------------------
def run_phase2_simulation():
    print("\nRunning Phase 2 simulation (slots & vehicles)...")
    
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
        slot = slot_manager.create_slot(s["slot_type"], s["level"])
        print(f"Slot created/existing: {slot}")

    # Register vehicles
    for v in vehicles:
        vehicle = vehicle_manager.register_vehicle(v["license_plate"], v["vehicle_type"])
        print(f"Vehicle registered/existing: {vehicle}")

    # Allocate & check-in/out
    for v in vehicles:
        slot = slot_manager.allocate_slot(v["license_plate"])
        print(f"Vehicle allocated: {slot}")
        checkin = vehicle_manager.checkin_vehicle(v["license_plate"])
        print(f"Vehicle checked-in: {checkin}")
        checkout = vehicle_manager.checkout_vehicle(v["license_plate"], amount=50 + len(v["license_plate"])*5)
        print(f"Vehicle checked-out: {checkout}")

    # Show DB state
    print("\n=== DATABASE STATE ===")
    print("\n--- Slots ---")
    for s in slot_manager.list_slots():
        print(s)
    print("\n--- Vehicles ---")
    from parking_system.database.db import get_conn
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM vehicles")
        for row in cur.fetchall():
            print(dict(row))
    print("=====================")
    print("Phase 2 simulation completed.\n")


# -----------------------------
# Phase 4: IoT & MQTT
# -----------------------------
def start_sensor_simulation():
    t = threading.Thread(target=update_slots_from_sensors, daemon=True)
    t.start()
    return t

def start_camera_simulation():
    t = threading.Thread(target=simulate_camera_checkins, daemon=True)
    t.start()
    return t

def start_mqtt_publisher():
    t = threading.Thread(target=publish_loop, daemon=True)
    t.start()
    return t


# -----------------------------
# Phase 3: Analytics & Prediction
# -----------------------------
def run_phase3_analytics():
    print("\nRunning Phase 3 analytics & predictions...\n")
    df_report = reports.generate_enhanced_report("phase4_report.xlsx")
    df_pred = prediction.predict_slot_demand("slot_demand_phase4.xlsx")
    return df_report, df_pred


# -----------------------------
# Main Phase 4 Pipeline
# -----------------------------
def main():
    print("=== Starting Full Parking System Pipeline ===")

    # Reset and initialize DB
    db_path = "src/parking_system/database/parking.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    print(f"Database reset: {db_path}")
    init_db()
    print("Database initialized.\n")

    # Phase 2 Simulation
    run_phase2_simulation()

    # Phase 4 IoT Simulation
    print("Starting IoT sensor & camera simulations...\n")
    sensor_thread = start_sensor_simulation()
    camera_thread = start_camera_simulation()
    mqtt_thread = start_mqtt_publisher()
    
    # Give some time for sensor simulation to run
    time.sleep(2)

    # Phase 3 Analytics
    df_report, df_pred = run_phase3_analytics()

    print("\n=== Full Pipeline Completed ===")
    print("Reports saved:")
    print("- Enhanced report: phase4_report.xlsx")
    print("- Predicted demand: slot_demand_phase4.xlsx")

    # Keep the pipeline alive for MQTT / sensor threads (demo mode)
    print("\nRunning sensor & MQTT threads for demo (10s)...")
    time.sleep(10)
    print("Demo finished. Exiting.")


if __name__ == "__main__":
    main()
