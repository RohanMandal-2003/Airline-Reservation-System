import streamlit as st
from flight_utils import add_flight, get_flights, book_ticket, get_bookings

st.set_page_config(page_title="✈️ Airline Reservation System", layout="centered")

st.title("✈️ Airline Reservation System")

menu = st.sidebar.radio("📋 Select Option", ["Add Flight (Admin)", "Book Ticket", "View Bookings"])

# ---------------------- ADD FLIGHT (ADMIN) -------------------------
if menu == "Add Flight (Admin)":
    st.markdown("## 🛫 Add New Flight")

    with st.form("add_flight_form"):
        col1, col2 = st.columns(2)
        with col1:
            origin = st.text_input("From (Origin)")
            departure = st.text_input("Departure Time (YYYY-MM-DD HH:MM)")
            base_price = st.number_input("Base Price (₹)", min_value=500.0)
        with col2:
            destination = st.text_input("To (Destination)")
            arrival = st.text_input("Arrival Time (YYYY-MM-DD HH:MM)")
            total_seats = st.number_input("Total Seats", min_value=1, step=1)

        submitted = st.form_submit_button("Add Flight ✈️")
        if submitted:
            if origin and destination and departure and arrival:
                add_flight(origin, destination, departure, arrival, base_price, total_seats)
                st.success("✅ Flight added successfully!")
            else:
                st.error("⚠️ Please complete all fields.")

# ------------------------- BOOK TICKET -----------------------------
elif menu == "Book Ticket":
    st.markdown("## 🎟️ Book Your Flight Ticket")

    flights = get_flights()

    if flights:
        st.markdown("### 📊 Flight Price Board")
        for f in flights:
            flight_id, origin, dest, dep, arr, base_price, total_seats, seats_left = f
            occupancy_rate = (total_seats - seats_left) / total_seats
            current_price = round(base_price * (1 + 0.5 * occupancy_rate), 2)

            with st.expander(f"🔹 {origin} → {dest} | {dep}"):
                st.write(f"🕑 Arrival: {arr}")
                st.write(f"💺 Seats Left: {seats_left} / {total_seats}")
                st.write(f"💰 Current Price: ₹{current_price}")

        st.markdown("---")

        st.markdown("### 🧾 Book a Ticket")
        flight_choices = {
            f"{f[1]} → {f[2]} | {f[3]} | ₹{round(f[5] * (1 + 0.5 * ((f[6] - f[7]) / f[6])), 2)} | Seats Left: {f[7]}": f[0]
            for f in flights
        }

        selected = st.selectbox("✈️ Choose a Flight", list(flight_choices.keys()))
        passenger_name = st.text_input("👤 Passenger Name")

        if st.button("Confirm Booking ✅"):
            if not selected or not passenger_name.strip():
                st.warning("Please select a flight and enter your name.")
            else:
                result = book_ticket(flight_choices[selected], passenger_name.strip())
                st.success(result)
    else:
        st.warning("❌ No flights available for booking.")

# ------------------------ VIEW BOOKINGS ----------------------------
elif menu == "View Bookings":
    st.markdown("## 📄 Your Bookings")

    bookings = get_bookings()

    if bookings:
        for b in bookings:
            booking_id, flight_id, name, booked_on, seat_no, paid = b
            st.info(f"""
🧾 **Booking ID**: {booking_id}  
👤 **Passenger**: {name}  
✈️ **Flight ID**: {flight_id}  
💺 **Seat No**: {seat_no}  
💰 **Paid**: ₹{paid}
""")
    else:
        st.warning("No bookings found.")
