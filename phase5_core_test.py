#!/usr/bin/env python3
import os
import threading
import time

# Set PYTHONPATH for module resolution
os.environ["PYTHONPATH"] = os.path.join(os.getcwd(), "src")

from parking_system.database.db import init_db
from parking_system.core import vehicle_manager, slot_manager
from parking_system.analytics import reports, prediction
from parking_system.io_integration import sensor_reader, camera_plate_recognition, mqtt_publisher
from parking_system.security import auth

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

    # Allocate & check-in/out using Phase 5 role-based access
    for v in vehicles:
        slot = slot_manager.allocate_slot(v["license_plate"])
        print(f"Vehicle allocated: {slot}")

        # Check-in as staff
        checkin = vehicle_manager.checkin_vehicle(v["license_plate"], username="staff")
        print(f"Vehicle checked-in: {checkin}")

        # Checkout with mock payment
        checkout = vehicle_manager.checkout_vehicle(v["license_plate"], amount=50 + len(v["license_plate"])*5, username="staff")
        print(f"Vehicle checked-out: {checkout}")

    print("\n=== DATABASE STATE ===")
    print("\n--- Slots ---")
    for s in slot_manager.list_slots():
        print(s)
    print("\n--- Vehicles ---")
    for v in vehicle_manager.list_vehicles():
        print(v)
    print("=====================")
    print("Phase 2 simulation completed.\n")

# -----------------------------
# Phase 4: IoT & MQTT
# -----------------------------
def start_sensor_simulation():
    t = threading.Thread(target=sensor_reader.update_slots_from_sensors, daemon=True)
    t.start()
    return t

def start_camera_simulation():
    t = threading.Thread(target=camera_plate_recognition.simulate_camera_checkins, daemon=True)
    t.start()
    return t

def start_mqtt_publisher():
    t = threading.Thread(target=mqtt_publisher.publish_loop, daemon=True)
    t.start()
    return t

# -----------------------------
# Phase 3: Analytics & Prediction
# -----------------------------
def run_phase3_analytics():
    print("\nRunning Phase 3 analytics & predictions...\n")
    df_report = reports.generate_enhanced_report("phase5_report.xlsx")
    df_pred = prediction.predict_slot_demand("slot_demand_phase5.xlsx")
    return df_report, df_pred

# -----------------------------
# Phase 5: Security Login Demo
# -----------------------------
def demo_security_login():
    print("\n=== Phase 5: Security & Roles Demo ===")
    user = auth.login_user("staff", "staff123")
    if user:
        print(f"Login successful: {user['username']} with role {user['role']}")
    else:
        print("Login failed")

# -----------------------------
# Main Phase 5 Pipeline
# -----------------------------
def main():
    print("=== Starting Full Parking System Pipeline (Phase 5) ===")

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
    
    # Give some time for IoT simulations to update
    time.sleep(3)

    # Phase 3 Analytics
    df_report, df_pred = run_phase3_analytics()
    print("\nReports generated:")
    print("- Enhanced report:", "phase5_report.xlsx")
    print("- Predicted demand:", "slot_demand_phase5.xlsx")

    # Phase 5 Security login demo
    demo_security_login()

    # Keep threads alive for demo (optional, 10s)
    print("\nRunning sensor & MQTT threads for demo (10s)...")
    time.sleep(10)
    print("Demo finished. Exiting.")

if __name__ == "__main__":
    main()
#find src -type d -name "__pycache__" -exec rm -rf {} +
'''export PYTHONPATH=$(pwd)/src
python3 phase5_core_test.py'''