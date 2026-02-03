import pytest
from parking_system.database.db_utils import (
    create_slot,
    list_slots,
    register_vehicle,
    list_vehicles,
    allocate_slot_to_vehicle,
    checkin_vehicle,
    checkout_vehicle
)
from parking_system.database.db import Base, engine, Session
from parking_system.database.models import Slot, Vehicle

# ----------------- Fixture: clean database -----------------
@pytest.fixture(scope="function", autouse=True)
def setup_database():
    # Drop all tables and recreate
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup after test
    Base.metadata.drop_all(bind=engine)

# ----------------- Slot Tests -----------------
def test_create_slot_success():
    success, msg = create_slot("A1")
    assert success is True
    assert "created successfully" in msg

def test_create_duplicate_slot():
    create_slot("A1")
    success, msg = create_slot("A1")
    assert success is False
    assert "already exists" in msg

def test_list_slots():
    create_slot("A1")
    create_slot("B1")
    slots = list_slots()
    assert len(slots) == 2
    numbers = [s[0] for s in slots]
    assert "A1" in numbers and "B1" in numbers

# ----------------- Vehicle Tests -----------------
def test_register_vehicle_success():
    success, msg = register_vehicle("ABC123", "Car")
    assert success is True
    assert "registered successfully" in msg

def test_register_duplicate_vehicle():
    register_vehicle("ABC123", "Car")
    success, msg = register_vehicle("ABC123", "Car")
    assert success is False
    assert "already registered" in msg

def test_list_vehicles():
    create_slot("A1")
    register_vehicle("ABC123", "Car")
    allocate_slot_to_vehicle("ABC123")
    vehicles = list_vehicles()
    assert len(vehicles) == 1
    assert vehicles[0][0] == "ABC123"
    assert vehicles[0][2] == "A1"

# ----------------- Allocation Tests -----------------
def test_allocate_slot_to_vehicle_success():
    create_slot("A1")
    register_vehicle("ABC123", "Car")
    success, msg = allocate_slot_to_vehicle("ABC123")
    assert success is True
    assert "allocated to slot A1" in msg

def test_allocate_already_allocated_vehicle():
    create_slot("A1")
    register_vehicle("ABC123", "Car")
    allocate_slot_to_vehicle("ABC123")
    success, msg = allocate_slot_to_vehicle("ABC123")
    assert success is False
    assert "already allocated" in msg

def test_allocate_no_free_slot():
    create_slot("A1")
    register_vehicle("ABC123", "Car")
    register_vehicle("XYZ789", "Bike")
    allocate_slot_to_vehicle("ABC123")
    success, msg = allocate_slot_to_vehicle("XYZ789")
    assert success is False
    assert "No free slots" in msg

# ----------------- Check-in / Check-out Tests -----------------
def test_checkin_vehicle():
    create_slot("A1")
    register_vehicle("ABC123", "Car")
    success, msg = checkin_vehicle("ABC123")
    assert success is True
    assert "checked in to slot A1" in msg

def test_checkin_already_checked_in_vehicle():
    create_slot("A1")
    register_vehicle("ABC123", "Car")
    checkin_vehicle("ABC123")
    success, msg = checkin_vehicle("ABC123")
    assert success is False
    assert "already checked in" in msg

def test_checkout_vehicle():
    create_slot("A1")
    register_vehicle("ABC123", "Car")
    checkin_vehicle("ABC123")
    success, msg = checkout_vehicle("ABC123")
    assert success is True
    assert "checked out from slot A1" in msg

def test_checkout_vehicle_not_checked_in():
    register_vehicle("ABC123", "Car")
    success, msg = checkout_vehicle("ABC123")
    assert success is False
    assert "is not checked in" in msg
