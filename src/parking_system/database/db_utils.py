from typing import List, Optional
from parking_system.models.entities import Slot, Vehicle

_slots: List[Slot] = []
_vehicles: List[Vehicle] = []

_slot_id_counter = 1
_vehicle_id_counter = 1


def create_slot(slot_type: str, level: int) -> Slot:
    global _slot_id_counter
    slot = Slot(
        id=_slot_id_counter,
        slot_type=slot_type,
        level=level
    )
    _slots.append(slot)
    _slot_id_counter += 1
    return slot


def list_slots() -> List[Slot]:
    return _slots


def register_vehicle(license_plate: str, vehicle_type: str) -> Vehicle:
    global _vehicle_id_counter

    for v in _vehicles:
        if v.license_plate == license_plate:
            raise ValueError("Vehicle already registered")

    vehicle = Vehicle(
        id=_vehicle_id_counter,
        license_plate=license_plate,
        vehicle_type=vehicle_type
    )
    _vehicles.append(vehicle)
    _vehicle_id_counter += 1
    return vehicle


def allocate_slot_to_vehicle(license_plate: str) -> Slot:
    vehicle = next((v for v in _vehicles if v.license_plate == license_plate), None)
    if not vehicle:
        raise ValueError("Vehicle not registered")

    if vehicle.slot_id is not None:
        raise ValueError("Vehicle already allocated")

    for slot in _slots:
        if not slot.is_occupied:
            slot.is_occupied = True
            slot.vehicle_plate = license_plate
            vehicle.slot_id = slot.id
            return slot

    raise ValueError("No available slots")
