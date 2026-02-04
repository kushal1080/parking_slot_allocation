from fastapi import APIRouter, HTTPException
from typing import List
from parking_system.api.schemas import VehicleCreate, VehiclePlate
from parking_system.core import vehicle_manager

router = APIRouter(prefix="/api/vehicles", tags=["Vehicles"])

@router.post("/", response_model=dict)
def register_vehicle_api(payload: VehicleCreate):
    try:
        return vehicle_manager.register_vehicle(payload.license_plate, payload.vehicle_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[dict])
def list_vehicles_api():
    return vehicle_manager.list_vehicles()

@router.post("/checkin/", response_model=dict)
def checkin_vehicle_api(payload: VehiclePlate):
    try:
        return vehicle_manager.checkin_vehicle(payload.license_plate)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/checkout/", response_model=dict)
def checkout_vehicle_api(payload: VehiclePlate):
    try:
        return vehicle_manager.checkout_vehicle(payload.license_plate)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
