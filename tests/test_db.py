def init_db():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    with get_conn() as conn:
        cur = conn.cursor()
        # Slots table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_type TEXT NOT NULL,
            level INTEGER NOT NULL,
            is_occupied BOOLEAN NOT NULL DEFAULT 0,
            vehicle_plate TEXT UNIQUE
        )
        """)
        # Vehicles table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            license_plate TEXT PRIMARY KEY,
            vehicle_type TEXT NOT NULL,
            checked_in BOOLEAN NOT NULL DEFAULT 0,
            slot_id INTEGER,
            FOREIGN KEY(slot_id) REFERENCES slots(id)
        )
        """)
        # Vehicle logs table (added slot_id)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS vehicle_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_plate TEXT NOT NULL,
            slot_id INTEGER,
            checkin_time TEXT,
            checkout_time TEXT,
            amount REAL DEFAULT 0,
            FOREIGN KEY(license_plate) REFERENCES vehicles(license_plate),
            FOREIGN KEY(slot_id) REFERENCES slots(id)
        )
        """)
