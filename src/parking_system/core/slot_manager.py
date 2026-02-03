from parking_system.database.db_utils import create_slot, list_slots, allocate_slot_to_vehicle

def create_slot_cli():
    number = input("Enter slot number: ")
    success, msg = create_slot(number)
    print(msg)

def list_slots_cli():
    slots = list_slots()
    for number, status in slots:
        print(f"Slot {number}: {status}")

def allocate_slot_cli():
    plate = input("Enter vehicle plate number: ")
    success, msg = allocate_slot_to_vehicle(plate)
    print(msg)
