from parking_system.core.slot_manager import create_slot, list_slots, allocate_slot

def create_slot_cli():
    slot_type = input("Enter slot type: ")
    level = int(input("Enter level: "))
    slot = create_slot(slot_type, level)
    print(f"Slot created: ID={slot.id}, type={slot.slot_type}, level={slot.level}")


def list_slots_cli():
    slots = list_slots()
    for slot in slots:
        status = "Occupied" if slot.is_occupied else "Free"
        print(f"Slot {slot.id} [{slot.slot_type}] Level {slot.level}: {status}")


def allocate_slot_cli():
    plate = input("Enter vehicle plate number: ")
    slot = allocate_slot(plate)
    print(f"Vehicle allocated to slot {slot.id}")
