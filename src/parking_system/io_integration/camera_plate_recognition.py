from parking_system.core import vehicle_manager, slot_manager
import time
import random

SIM_VEHICLES = ["ABC123", "XYZ789"]

def simulate_camera_checkins():
    """
    Simulate automatic vehicle check-ins via camera recognition
    """
    while True:
        vehicle_plate = random.choice(SIM_VEHICLES)
        try:
            slot = slot_manager.allocate_slot(vehicle_plate)
            vehicle_manager.checkin_vehicle(vehicle_plate)
            print(f"[Camera] Vehicle auto-checked-in: {vehicle_plate} -> Slot {slot['id']}")
        except Exception:
            pass
        time.sleep(5)
