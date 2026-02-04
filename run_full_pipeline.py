#!/usr/bin/env python3
import os
from parking_system.database.db import init_db
from phase2_core_test import main as phase2_main
from phase3_core_test import main as phase3_main

DB_PATH = "src/parking_system/database/parking.db"

def reset_db():
    """Delete existing DB and reinitialize."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Database reset: {DB_PATH}")
    else:
        print(f"No existing database found at {DB_PATH}")
    init_db()
    print("Database initialized.\n")

def run_pipeline():
    print("\n=== Starting Full Parking System Pipeline ===\n")

    # Step 1: Reset DB
    reset_db()

    # Step 2: Run Phase 2 (simulate slots, vehicles, allocation, check-in/out)
    print("Running Phase 2 simulation (slots & vehicles)...")
    phase2_main()
    print("Phase 2 simulation completed.\n")

    # Step 3: Run Phase 3 (enhanced analytics + predictions)
    print("Running Phase 3 analytics & predictions...")
    phase3_main()
    print("Phase 3 analytics completed.\n")

    print("=== Full Pipeline Completed ===\n")
    print("Reports saved:")
    print("- Enhanced report: phase3_report.xlsx")
    print("- Predicted demand: slot_demand.xlsx")
    print("\nYou can now review Excel reports with revenue, hourly charts, and 24-hour predictions.")

if __name__ == "__main__":
    run_pipeline()
