import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Slot, Vehicle

# Delete existing DB to prevent schema mismatch
DB_PATH = os.path.join(os.path.dirname(__file__), "parking.db")
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

# ---------------- Slot Utilities ----------------
def create_slot(number):
    session = Session()
    try:
        if session.query(Slot).filter_by(number=number).first():
            return False, f"Slot {number} already exists."
        slot = Slot(number=number)
        session.add(slot)
        session.commit()
        return True, f"Slot {number} created successfully."
    finally:
        session.close()

def list_slots():
    session = Session()
    try:
        return [(s.number, s.status) for s in session.query(Slot).all()]
    finally:
        session.close()

def allocate_slot_to_vehicle(plate_number):
    session = Session()
    try:
        vehicle = session.query(Vehicle).filter_by(plate_number=plate_number).first()
        if not vehicle:
            return False, f"Vehicle {plate_number} not found."
        if vehicle.slot:
            return False, f"Vehicle already allocated to slot {vehicle.slot.number}."
        free_slot = session.query(Slot).filter_by(status="Free").first()
        if not free_slot:
            return False, "No free slots available."
        free_slot.status = "Occupied"
        vehicle.slot = free_slot
        session.commit()
        return True, f"Vehicle allocated to slot {free_slot.number}."
    finally:
        session.close()

# ---------------- Vehicle Utilities ----------------
def register_vehicle(plate_number, vehicle_type):
    session = Session()
    try:
        if session.query(Vehicle).filter_by(plate_number=plate_number).first():
            return False, f"Vehicle {plate_number} already registered."
        vehicle = Vehicle(plate_number=plate_number, type=vehicle_type)
        session.add(vehicle)
        session.commit()
        return True, f"Vehicle {plate_number} registered successfully."
    finally:
        session.close()

def list_vehicles():
    session = Session()
    try:
        result = []
        for v in session.query(Vehicle).all():
            slot_num = v.slot.number if v.slot else "Not allocated"
            result.append((v.plate_number, v.type, slot_num))
        return result
    finally:
        session.close()

def checkin_vehicle(plate_number):
    session = Session()
    try:
        vehicle = session.query(Vehicle).filter_by(plate_number=plate_number).first()
        if not vehicle:
            return False, f"Vehicle {plate_number} not found."
        if vehicle.checked_in:
            slot_num = vehicle.slot.number if vehicle.slot else "Unknown"
            return False, f"Vehicle already checked in at slot {slot_num}."
        if not vehicle.slot:
            free_slot = session.query(Slot).filter_by(status="Free").first()
            if not free_slot:
                return False, "No free slots available."
            vehicle.slot = free_slot
        vehicle.slot.status = "Occupied"
        vehicle.checked_in = True
        session.commit()
        return True, f"Vehicle {plate_number} checked in to slot {vehicle.slot.number}."
    finally:
        session.close()

def checkout_vehicle(plate_number):
    session = Session()
    try:
        vehicle = session.query(Vehicle).filter_by(plate_number=plate_number).first()
        if not vehicle or not vehicle.checked_in or not vehicle.slot:
            return False, f"Vehicle {plate_number} is not checked in."
        slot_number = vehicle.slot.number
        vehicle.slot.status = "Free"
        vehicle.slot = None
        vehicle.checked_in = False
        session.commit()
        return True, f"Vehicle {plate_number} checked out from slot {slot_number}."
    finally:
        session.close()
