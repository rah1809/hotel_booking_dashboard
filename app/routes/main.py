from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Booking, Room

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    # Get recent bookings
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    
    # Get room statistics
    total_rooms = Room.query.count()
    available_rooms = Room.query.filter_by(status='available').count()
    occupied_rooms = Room.query.filter_by(status='occupied').count()
    
    # Get booking statistics
    total_bookings = Booking.query.count()
    active_bookings = Booking.query.filter_by(status='active').count()
    completed_bookings = Booking.query.filter_by(status='completed').count()
    
    return render_template('main/index.html',
                         recent_bookings=recent_bookings,
                         total_rooms=total_rooms,
                         available_rooms=available_rooms,
                         occupied_rooms=occupied_rooms,
                         total_bookings=total_bookings,
                         active_bookings=active_bookings,
                         completed_bookings=completed_bookings)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Get all bookings
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    
    # Get all rooms
    rooms = Room.query.all()
    
    return render_template('main/dashboard.html',
                         bookings=bookings,
                         rooms=rooms) 