from dataclasses import dataclass
from typing import Optional

@dataclass
class Slot:
    id: int
    slot_type: str
    level: int
    is_occupied: bool = False
    vehicle_plate: Optional[str] = None


@dataclass
class Vehicle:
    id: int
    license_plate: str
    vehicle_type: str
    checked_in: bool = False
    slot_id: Optional[int] = None
