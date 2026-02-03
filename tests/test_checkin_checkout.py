# tests/test_checkin_checkout.py
from parking_system.database.db_utils import create_slot, register_vehicle, checkin_vehicle, checkout_vehicle

def test_create_and_checkin_checkout():
    # Create slot
    success, msg = create_slot("T1")
    assert success

    # Register vehicle
    success, msg = register_vehicle("TEST123", "Car")
    assert success

    # Check-in vehicle
    success, msg = checkin_vehicle("TEST123")
    assert success

    # Check-out vehicle
    success, msg = checkout_vehicle("TEST123")
    assert success
