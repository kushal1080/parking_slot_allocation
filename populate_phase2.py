#!/usr/bin/env python3
from parking_system.database.db import init_db
from parking_system.core import slot_manager, vehicle_manager

init_db()

# Create slots
slot_manager.create_slot("compact", 1)
slot_manager.create_slot("large", 1)

# Register vehicles
vehicle_manager.register_vehicle("ABC123", "Car")
vehicle_manager.register_vehicle("XYZ789", "Truck")

# Allocate vehicles
slot_manager.allocate_slot("ABC123")
slot_manager.allocate_slot("XYZ789")

# Check in/out vehicles to create logs
vehicle_manager.checkin_vehicle("ABC123")
vehicle_manager.checkout_vehicle("ABC123", amount=50)

vehicle_manager.checkin_vehicle("XYZ789")
vehicle_manager.checkout_vehicle("XYZ789", amount=100)

print("Phase 2 test data inserted.")
