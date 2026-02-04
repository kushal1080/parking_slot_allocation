from pydantic import BaseModel

class SlotCreate(BaseModel):
    slot_type: str
    level: int

class VehicleCreate(BaseModel):
    license_plate: str
    vehicle_type: str

class VehiclePlate(BaseModel):
    license_plate: str
