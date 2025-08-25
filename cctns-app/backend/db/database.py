# db.py
import sqlite3
import os

DB_PATH = "cctns.db"

# Create DB and table if not exists
if not os.path.exists(DB_PATH):
    print("Creating database and table...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fir (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crime_type TEXT,
            location TEXT,
            date_registered TEXT,
            status TEXT
        )
    """)
    conn.commit()
else:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

# Use these anywhere
def get_connection():
    return conn

def get_cursor():
    return cursor

# Optional: Fill with sample data
def setup_db():
    print("Inserting sample data...")
    cursor.execute("DELETE FROM fir")  # Clean old rows
    sample_data = [
        ("Theft", "Guntur", "2025-07-01", "Open"),
        ("Theft", "Guntur", "2025-07-10", "Closed"),
        ("Assault", "Vijayawada", "2025-06-15", "Open")
    ]
    cursor.executemany(
        "INSERT INTO fir (crime_type, location, date_registered, status) VALUES (?, ?, ?, ?)",
        sample_data
    )
    conn.commit()

