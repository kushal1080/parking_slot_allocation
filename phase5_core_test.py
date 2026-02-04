#!/usr/bin/env python3
import os
import threading
import time

# Set PYTHONPATH for module resolution
os.environ["PYTHONPATH"] = os.path.join(os.getcwd(), "src")

# Core imports
from parking_system.database.db import init_db
from parking_system.core import vehicle_manager, slot_manager
from parking_system.analytics import reports, prediction
from parking_system.io_integration import sensor_reader, camera_plate_recognition, mqtt_publisher
from parking_system.security import auth, audit
from parking_system.notifications import email_service, sms_service, push_service
from parking_system.payment import payment_gateway

# -----------------------------
# Phase 0: Security Setup
# -----------------------------
def setup_users():
    # Mock users for testing
    users = [
        {"username": "admin", "password": "admin123", "role": "Admin"},
        {"username": "staff1", "password": "staff123", "role": "Staff"},
        {"username": "user1", "password": "user123", "role": "User"},
    ]
    for u in users:
        auth.register_user(u["username"], u["password"], u["role"])
    print("Mock users created.")

# -----------------------------
# Phase 2: Simulation
# -----------------------------
def run_phase2_simulation():
    print("\nRunning Phase 2 simulation (slots & vehicles)...")
    
    # Sample slots & vehicles
    slots = [{"slot_type": "compact", "level": 1}, {"slot_type": "large", "level": 1}]
    vehicles = [{"license_plate": "ABC123", "vehicle_type": "Car"}, {"license_plate": "XYZ789", "vehicle_type": "Truck"}]

    # Create slots
    for s in slots:
        slot = slot_manager.create_slot(s["slot_type"], s["level"])
        print(f"Slot created/existing: {slot}")

    # Register vehicles
    for v in vehicles:
        vehicle = vehicle_manager.register_vehicle(v["license_plate"], v["vehicle_type"])
        print(f"Vehicle registered/existing: {vehicle}")

    # Allocate, check-in & payment
    for v in vehicles:
        slot = slot_manager.allocate_slot(v["license_plate"])
        print(f"Vehicle allocated: {slot}")

        # Simulate payment for premium slot
        amount = payment_gateway.simulate_payment(v["license_plate"], slot["slot_type"])
        checkout = vehicle_manager.checkout_vehicle(v["license_plate"], amount=amount)
        print(f"Vehicle checked-out (payment {amount}): {checkout}")

        # Audit log
        audit.log_action({"username": "staff1", "role": "Staff"}, f"Vehicle {v['license_plate']} checked-out", f"Paid {amount}")

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
# Phase 5: Notifications
# -----------------------------
def send_notifications(license_plate, slot_id):
    # Placeholder notifications
    email_service.send_email(f"Vehicle {license_plate} checked-in to slot {slot_id}")
    sms_service.send_sms(f"Vehicle {license_plate} checked-in to slot {slot_id}")
    push_service.send_push(f"Vehicle {license_plate} checked-in to slot {slot_id}")
    # Audit log
    audit.log_action({"username": "staff1", "role": "Staff"}, "Notification sent", f"Vehicle {license_plate} slot {slot_id}")


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
    # Ensure audit table exists
    audit.init_audit_table()
    print("Database initialized.\n")

    # Setup users
    setup_users()

    # Phase 2 Simulation
    run_phase2_simulation()

    # Phase 4 IoT Simulation
    print("Starting IoT sensor & camera simulations...\n")
    sensor_thread = start_sensor_simulation()
    camera_thread = start_camera_simulation()
    mqtt_thread = start_mqtt_publisher()
    
    time.sleep(2)  # Let sensors run

    # Phase 3 Analytics
    df_report, df_pred = run_phase3_analytics()

    # Example notifications for vehicles
    for v in ["ABC123", "XYZ789"]:
        slot = slot_manager.get_slot_by_id(1)  # demo slot
        send_notifications(v, slot["id"])

    print("\n=== Full Phase 5 Pipeline Completed ===")
    print("Reports saved:")
    print("- Enhanced report: phase5_report.xlsx")
    print("- Predicted demand: slot_demand_phase5.xlsx")

    # Keep sensor & MQTT threads alive for demo
    print("\nRunning sensor & MQTT threads for demo (10s)...")
    time.sleep(10)
    print("Demo finished. Exiting.")

if __name__ == "__main__":
    main()
#export PYTHONPATH=$(pwd)/src python3 phase5_core_test.py
