from fastapi import FastAPI
from parking_system.database.db import init_db

from parking_system.api.slot_routes import router as slot_router
from parking_system.api.vehicle_routes import router as vehicle_router

# Initialize DB once at startup
init_db()

# Create FastAPI app
app = FastAPI(
    title="Parking Allocation System",
    version="0.1.0"
)

# Include routers (routers themselves have prefixes)
app.include_router(slot_router)
app.include_router(vehicle_router)

# Optional health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# CLI entry point
if __name__ == "__main__":
    import sys
    from parking_system.core import slot_manager, vehicle_manager

    def run_cli():
        while True:
            print("=== Parking CLI ===")
            print("1. Create Slot")
            print("2. List Slots")
            print("3. Register Vehicle")
            print("4. List Vehicles")
            print("5. Allocate Slot")
            print("6. Check-in Vehicle")
            print("7. Check-out Vehicle")
            print("8. Exit")
            choice = input("Choice: ")
            if choice=="1": slot_manager.create_slot_cli()
            elif choice=="2": slot_manager.list_slots_cli()
            elif choice=="3": vehicle_manager.register_vehicle_cli()
            elif choice=="4": vehicle_manager.list_vehicles_cli()
            elif choice=="5": slot_manager.allocate_slot_cli()
            elif choice=="6": vehicle_manager.checkin_vehicle_cli()
            elif choice=="7": vehicle_manager.checkout_vehicle_cli()
            elif choice=="8": break
            else: print("Invalid choice")

    if "--cli" in sys.argv:
        run_cli()
