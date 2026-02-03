from parking_system.database.db_utils import register_vehicle, list_vehicles, checkin_vehicle, checkout_vehicle

def register_vehicle_cli():
    plate = input("Enter vehicle plate number: ")
    types = ["Car", "Bike", "EV", "Handicapped"]
    print(f"Vehicle Types: {', '.join(types)}")
    vtype = input("Enter vehicle type: ")
    if vtype not in types:
        print("Invalid vehicle type.")
        return
    success, msg = register_vehicle(plate, vtype)
    print(msg)

def list_vehicles_cli():
    vehicles = list_vehicles()
    for plate, vtype, slot in vehicles:
        print(f"Vehicle {plate} - Type: {vtype} - Slot: {slot}")

def checkin_vehicle_cli():
    plate = input("Enter vehicle plate number: ")
    success, msg = checkin_vehicle(plate)
    print(msg)

def checkout_vehicle_cli():
    plate = input("Enter vehicle plate number: ")
    success, msg = checkout_vehicle(plate)
    print(msg)
