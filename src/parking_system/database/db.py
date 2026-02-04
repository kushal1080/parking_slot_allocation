import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_FILE = Path(__file__).parent / "parking.db"

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")  # Enforce foreign keys
    try:
        yield conn
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Create all tables for full Phase 5 support."""
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    with get_conn() as conn:
        cur = conn.cursor()

        # Slots
        cur.execute("""
        CREATE TABLE IF NOT EXISTS slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_type TEXT NOT NULL,
            level INTEGER NOT NULL,
            is_occupied INTEGER NOT NULL DEFAULT 0,
            vehicle_plate TEXT UNIQUE
        )
        """)

        # Vehicles
        cur.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            license_plate TEXT PRIMARY KEY,
            vehicle_type TEXT NOT NULL,
            checked_in INTEGER NOT NULL DEFAULT 0,
            slot_id INTEGER,
            FOREIGN KEY(slot_id) REFERENCES slots(id)
        )
        """)

        # Vehicle logs
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

        # Users (Phase 5 Security)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Admin','Staff','User'))
        )
        """)

        # Audit logs
        cur.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER NOT NULL,
            user TEXT NOT NULL,
            role TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT
        )
        """)


        # Audit logs table (Phase 5)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp INTEGER NOT NULL,
        user TEXT NOT NULL,
        role TEXT NOT NULL,
        action TEXT NOT NULL,
        details TEXT
)
""")


        # Payments (Phase 5 Payment integration)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_plate TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT,
            timestamp TEXT,
            FOREIGN KEY(license_plate) REFERENCES vehicles(license_plate)
        )
        """)
