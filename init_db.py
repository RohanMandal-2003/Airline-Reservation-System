from db_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS flights (
    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin TEXT,
    destination TEXT,
    departure_time TEXT,
    arrival_time TEXT,
    base_price REAL,
    total_seats INTEGER,
    available_seats INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id INTEGER,
    passenger_name TEXT,
    booking_date TEXT,
    seat_number INTEGER,
    price_paid REAL,
    FOREIGN KEY(flight_id) REFERENCES flights(flight_id)
)
''')

conn.commit()
conn.close()
print("✅ Tables created.")
