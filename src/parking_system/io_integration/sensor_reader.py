from parking_system.core import slot_manager
import random

def update_slots_from_sensors():
    """
    Simulate sensors updating slot occupancy randomly
    """
    slots = slot_manager.list_slots()
    for s in slots:
        # Randomly occupy or free slots (simulation)
        occupied = random.choice([True, False])
        slot_manager.set_slot_occupancy(s["id"], occupied)
