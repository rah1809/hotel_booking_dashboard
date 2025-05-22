from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Booking, Room
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    # Get total bookings
    total_bookings = Booking.query.count()
    
    # Get active bookings
    active_bookings = Booking.query.filter_by(status='active').count()
    
    # Calculate total revenue
    total_revenue = db.session.query(func.sum(Booking.total_amount)).scalar() or 0
    
    # Get bookings by hotel type
    hotel_types = db.session.query(
        Room.room_type,
        func.count(Booking.id)
    ).join(Booking).group_by(Room.room_type).all()
    
    hotel_type_labels = [ht[0] for ht in hotel_types]
    hotel_type_data = [ht[1] for ht in hotel_types]
    
    # Get cancellation distribution
    cancelled = Booking.query.filter_by(status='cancelled').count()
    not_cancelled = total_bookings - cancelled
    cancellation_data = [not_cancelled, cancelled]
    
    # Get monthly revenue
    six_months_ago = datetime.now() - timedelta(days=180)
    monthly_revenue = db.session.query(
        func.strftime('%Y-%m', Booking.created_at),
        func.sum(Booking.total_amount)
    ).filter(Booking.created_at >= six_months_ago).group_by(
        func.strftime('%Y-%m', Booking.created_at)
    ).all()
    
    monthly_labels = [mr[0] for mr in monthly_revenue]
    monthly_revenue_data = [float(mr[1]) for mr in monthly_revenue]
    
    # Get customer type distribution
    customer_types = db.session.query(
        Booking.customer_type,
        func.count(Booking.id)
    ).group_by(Booking.customer_type).all()
    
    customer_type_labels = [ct[0] for ct in customer_types]
    customer_type_data = [ct[1] for ct in customer_types]
    
    return render_template('dashboard/index.html',
                         total_bookings=total_bookings,
                         active_bookings=active_bookings,
                         total_revenue=total_revenue,
                         hotel_types=hotel_type_labels,
                         hotel_type_data=hotel_type_data,
                         cancellation_data=cancellation_data,
                         monthly_labels=monthly_labels,
                         monthly_revenue=monthly_revenue_data,
                         customer_types=customer_type_labels,
                         customer_type_data=customer_type_data) 