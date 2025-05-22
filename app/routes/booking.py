from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Booking, Room
from app import db
from datetime import datetime

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/bookings')
@login_required
def index():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template('booking/index.html', bookings=bookings)

@booking_bp.route('/bookings/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        room_id = request.form.get('room_id')
        check_in = datetime.strptime(request.form.get('check_in'), '%Y-%m-%d')
        check_out = datetime.strptime(request.form.get('check_out'), '%Y-%m-%d')
        guest_name = request.form.get('guest_name')
        guest_email = request.form.get('guest_email')
        guest_phone = request.form.get('guest_phone')
        
        # Validate room availability
        room = Room.query.get_or_404(room_id)
        if room.status != 'available':
            flash('Room is not available for the selected dates', 'error')
            return redirect(url_for('booking.new'))
        
        # Create new booking
        booking = Booking(
            room_id=room_id,
            user_id=current_user.id,
            check_in=check_in,
            check_out=check_out,
            guest_name=guest_name,
            guest_email=guest_email,
            guest_phone=guest_phone,
            status='active'
        )
        
        # Update room status
        room.status = 'occupied'
        
        db.session.add(booking)
        db.session.commit()
        
        flash('Booking created successfully', 'success')
        return redirect(url_for('booking.index'))
    
    rooms = Room.query.filter_by(status='available').all()
    return render_template('booking/new.html', rooms=rooms)

@booking_bp.route('/bookings/<int:id>')
@login_required
def show(id):
    booking = Booking.query.get_or_404(id)
    return render_template('booking/show.html', booking=booking)

@booking_bp.route('/bookings/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    booking = Booking.query.get_or_404(id)
    
    if request.method == 'POST':
        booking.check_in = datetime.strptime(request.form.get('check_in'), '%Y-%m-%d')
        booking.check_out = datetime.strptime(request.form.get('check_out'), '%Y-%m-%d')
        booking.guest_name = request.form.get('guest_name')
        booking.guest_email = request.form.get('guest_email')
        booking.guest_phone = request.form.get('guest_phone')
        booking.status = request.form.get('status')
        
        db.session.commit()
        flash('Booking updated successfully', 'success')
        return redirect(url_for('booking.show', id=booking.id))
    
    return render_template('booking/edit.html', booking=booking)

@booking_bp.route('/bookings/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    booking = Booking.query.get_or_404(id)
    
    # Update room status back to available
    room = booking.room
    room.status = 'available'
    
    db.session.delete(booking)
    db.session.commit()
    
    flash('Booking deleted successfully', 'success')
    return redirect(url_for('booking.index')) 