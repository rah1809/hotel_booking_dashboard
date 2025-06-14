from app import app, db
from app.models import Hotel, Room, Customer, Booking, ServiceRequest, MaintenanceRecord, CustomerFeedback, Staff
from datetime import datetime, timedelta
import random

def seed_database():
    with app.app_context():
        # Create sample hotels
        hotels = [
            Hotel(name="Grand Hotel", type="City", location="New York", total_rooms=100),
            Hotel(name="Beach Resort", type="Resort", location="Miami", total_rooms=150)
        ]
        db.session.add_all(hotels)
        db.session.commit()

        # Create sample rooms
        rooms = []
        for hotel in hotels:
            for i in range(1, hotel.total_rooms + 1):
                room = Room(
                    hotel_id=hotel.id,
                    room_number=f"{hotel.id}-{i:03d}",
                    room_type=random.choice(["Standard", "Deluxe", "Suite"]),
                    capacity=random.randint(1, 4),
                    rate=random.randint(100, 500)
                )
                rooms.append(room)
        db.session.add_all(rooms)
        db.session.commit()

        # Create sample customers
        customers = []
        for i in range(100):
            customer = Customer(
                name=f"Customer {i+1}",
                email=f"customer{i+1}@example.com",
                phone=f"+1{random.randint(1000000000, 9999999999)}",
                customer_type=random.choice(["Transient", "Contract", "Group"]),
                country=random.choice(["USA", "Canada", "UK", "Germany", "France"])
            )
            customers.append(customer)
        db.session.add_all(customers)
        db.session.commit()

        # Create sample bookings
        bookings = []
        for customer in customers:
            for _ in range(random.randint(1, 5)):
                check_in = datetime.now() - timedelta(days=random.randint(0, 365))
                check_out = check_in + timedelta(days=random.randint(1, 14))
                room = random.choice(rooms)
                booking = Booking(
                    hotel_id=room.hotel_id,
                    room_id=room.id,
                    customer_id=customer.id,
                    check_in=check_in,
                    check_out=check_out,
                    status=random.choice(["active", "completed", "cancelled"]),
                    total_amount=room.rate * (check_out - check_in).days,
                    payment_status=random.choice(["pending", "completed", "refunded"]),
                    booking_channel=random.choice(["Direct", "OTA", "Corporate"])
                )
                bookings.append(booking)
        db.session.add_all(bookings)
        db.session.commit()

        # Create sample service requests
        service_requests = []
        for booking in bookings:
            for _ in range(random.randint(0, 3)):
                service_request = ServiceRequest(
                    booking_id=booking.id,
                    request_type=random.choice(["Housekeeping", "Maintenance", "Room Service"]),
                    description=f"Service request for booking {booking.id}",
                    status=random.choice(["pending", "in_progress", "completed"]),
                    priority=random.choice(["low", "normal", "high"]),
                    assigned_to=f"Staff {random.randint(1, 10)}",
                    created_at=booking.check_in + timedelta(hours=random.randint(1, 24)),
                    completed_at=datetime.now()
                )
                service_requests.append(service_request)
        db.session.add_all(service_requests)
        db.session.commit()

        # Create sample maintenance records
        maintenance_records = []
        for room in rooms:
            for _ in range(random.randint(0, 2)):
                start_date = datetime.now() - timedelta(days=random.randint(0, 30))
                maintenance_record = MaintenanceRecord(
                    room_id=room.id,
                    maintenance_type=random.choice(["Routine", "Repair", "Renovation"]),
                    description=f"Maintenance for room {room.room_number}",
                    status=random.choice(["scheduled", "in_progress", "completed"]),
                    start_date=start_date,
                    end_date=start_date + timedelta(days=random.randint(1, 7)),
                    cost=random.randint(100, 1000)
                )
                maintenance_records.append(maintenance_record)
        db.session.add_all(maintenance_records)
        db.session.commit()

        # Create sample customer feedback
        feedback = []
        for booking in bookings:
            if random.random() < 0.7:  # 70% chance of feedback
                customer_feedback = CustomerFeedback(
                    customer_id=booking.customer_id,
                    booking_id=booking.id,
                    rating=random.randint(1, 5),
                    comment=f"Feedback for booking {booking.id}",
                    category=random.choice(["Service", "Cleanliness", "Value", "Location"])
                )
                feedback.append(customer_feedback)
        db.session.add_all(feedback)
        db.session.commit()

        # Create sample staff
        staff = []
        departments = ["Front Desk", "Housekeeping", "Maintenance", "Food & Beverage"]
        for i in range(20):
            staff_member = Staff(
                name=f"Staff Member {i+1}",
                role=random.choice(["Manager", "Supervisor", "Staff"]),
                department=random.choice(departments),
                status=random.choice(["active", "on_leave", "inactive"])
            )
            staff.append(staff_member)
        db.session.add_all(staff)
        db.session.commit()

if __name__ == "__main__":
    seed_database() 