from fastapi import APIRouter, HTTPException
from typing import List
from parking_system.api.schemas import (
    SlotCreate,
    SlotResponse,
    VehicleCreate,
    VehicleResponse,
    VehicleAction
)
from parking_system.core import slot_manager, vehicle_manager

router = APIRouter()

# ---------------------------
# SLOT ENDPOINTS
# ---------------------------

@router.post("/slots/", response_model=SlotResponse)
def create_slot(slot: SlotCreate):
    """
    Create a new parking slot.
    """
    try:
        new_slot = slot_manager.create_slot(slot_type=slot.slot_type, level=slot.level)
        return SlotResponse(
            id=new_slot.id,
            slot_type=new_slot.slot_type,
            level=new_slot.level,
            is_occupied=new_slot.is_occupied
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/slots/", response_model=List[SlotResponse])
def list_slots():
    """
    List all slots.
    """
    try:
        slots = slot_manager.list_slots()
        return [
            SlotResponse(
                id=s.id,
                slot_type=s.slot_type,
                level=s.level,
                is_occupied=s.is_occupied
            )
            for s in slots
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/slots/allocate/", response_model=SlotResponse)
def allocate_slot(vehicle: VehicleAction):
    """
    Allocate a slot to a vehicle by license plate.
    """
    try:
        allocated_slot = slot_manager.allocate_slot_to_vehicle(vehicle.license_plate)
        if not allocated_slot:
            raise HTTPException(status_code=404, detail="No available slots")
        return SlotResponse(
            id=allocated_slot.id,
            slot_type=allocated_slot.slot_type,
            level=allocated_slot.level,
            is_occupied=allocated_slot.is_occupied
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------
# VEHICLE ENDPOINTS
# ---------------------------

@router.post("/vehicles/", response_model=VehicleResponse)
def register_vehicle(vehicle: VehicleCreate):
    """
    Register a new vehicle.
    """
    try:
        v = vehicle_manager.register_vehicle(
            license_plate=vehicle.license_plate,
            vehicle_type=vehicle.vehicle_type
        )
        return VehicleResponse(
            id=v.id,
            license_plate=v.license_plate,
            vehicle_type=v.vehicle_type,
            checked_in=v.checked_in,
            slot_id=v.slot_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/vehicles/", response_model=List[VehicleResponse])
def list_vehicles():
    """
    List all vehicles.
    """
    try:
        vehicles = vehicle_manager.list_vehicles()
        return [
            VehicleResponse(
                id=v.id,
                license_plate=v.license_plate,
                vehicle_type=v.vehicle_type,
                checked_in=v.checked_in,
                slot_id=v.slot_id
            )
            for v in vehicles
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vehicles/checkin/", response_model=VehicleResponse)
def checkin_vehicle(action: VehicleAction):
    """
    Check in a vehicle.
    """
    try:
        vehicle = vehicle_manager.checkin_vehicle(action.license_plate)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return VehicleResponse(
            id=vehicle.id,
            license_plate=vehicle.license_plate,
            vehicle_type=vehicle.vehicle_type,
            checked_in=vehicle.checked_in,
            slot_id=vehicle.slot_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/vehicles/checkout/", response_model=VehicleResponse)
def checkout_vehicle(action: VehicleAction):
    """
    Check out a vehicle.
    """
    try:
        vehicle = vehicle_manager.checkout_vehicle(action.license_plate)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found or not checked in")
        return VehicleResponse(
            id=vehicle.id,
            license_plate=vehicle.license_plate,
            vehicle_type=vehicle.vehicle_type,
            checked_in=vehicle.checked_in,
            slot_id=vehicle.slot_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
