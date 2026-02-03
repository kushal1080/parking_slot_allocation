from parking_system.core import slot_manager, vehicle_manager

def main():
    while True:
        print("=== Parking Slot Allocation CLI ===")
        print("1. Create Slot")
        print("2. List Slots")
        print("3. Register Vehicle")
        print("4. List Vehicles")
        print("5. Allocate Slot to Vehicle")
        print("6. Check-in Vehicle")
        print("7. Check-out Vehicle")
        print("8. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            slot_manager.create_slot_cli()
        elif choice == "2":
            slot_manager.list_slots_cli()
        elif choice == "3":
            vehicle_manager.register_vehicle_cli()
        elif choice == "4":
            vehicle_manager.list_vehicles_cli()
        elif choice == "5":
            slot_manager.allocate_slot_cli()
        elif choice == "6":
            vehicle_manager.checkin_vehicle_cli()
        elif choice == "7":
            vehicle_manager.checkout_vehicle_cli()
        elif choice == "8":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
