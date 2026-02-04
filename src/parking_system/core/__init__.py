# Expose all core functionalities for clean imports
from .vehicle_manager import (
    register_vehicle,
    checkin_vehicle,
    checkout_vehicle
)
from .slot_manager import (
    create_slot,
    list_slots,
    allocate_slot,
    set_slot_occupancy,
    get_slot_by_id
)
