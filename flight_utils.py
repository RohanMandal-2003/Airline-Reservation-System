from db_connection import get_connection
import datetime

def calculate_dynamic_price(base_price, seats_left, total_seats):
    occupancy = (total_seats - seats_left) / total_seats
    multiplier = 1 + (0.5 * occupancy)
    return round(base_price * multiplier, 2)

def add_flight(origin, destination, departure, arrival, base_price, total_seats):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO flights (origin, destination, departure_time, arrival_time, base_price, total_seats, available_seats)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (origin, destination, departure, arrival, base_price, total_seats, total_seats))
    conn.commit()
    conn.close()

def get_flights():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flights")
    return cursor.fetchall()

def book_ticket(flight_id, passenger_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flights WHERE flight_id=?", (flight_id,))
    flight = cursor.fetchone()

    if flight and flight[7] > 0:
        price = calculate_dynamic_price(flight[5], flight[7], flight[6])
        seat_no = flight[6] - flight[7] + 1
        booking_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
            INSERT INTO bookings (flight_id, passenger_name, booking_date, seat_number, price_paid)
            VALUES (?, ?, ?, ?, ?)
        ''', (flight_id, passenger_name, booking_date, seat_no, price))

        cursor.execute("UPDATE flights SET available_seats = available_seats - 1 WHERE flight_id=?", (flight_id,))
        conn.commit()
        conn.close()
        return f"✅ Ticket Booked! Seat {seat_no}, Price ₹{price}"
    else:
        return "❌ No seats available."

def get_bookings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    return cursor.fetchall()
