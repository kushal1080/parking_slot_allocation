from fastapi import APIRouter, HTTPException
from typing import List
from parking_system.api.schemas import SlotCreate, VehiclePlate
from parking_system.core import slot_manager

router = APIRouter(prefix="/api/slots", tags=["Slots"])

@router.post("/", response_model=dict)
def create_slot_api(payload: SlotCreate):
    try:
        return slot_manager.create_slot(payload.slot_type, payload.level)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[dict])
def list_slots_api():
    return slot_manager.list_slots()

@router.post("/allocate/", response_model=dict)
def allocate_slot_api(payload: VehiclePlate):
    try:
        return slot_manager.allocate_slot(payload.license_plate)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
