from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.models import Room
from app import db

room_bp = Blueprint('room', __name__)

@room_bp.route('/rooms')
@login_required
def index():
    rooms = Room.query.all()
    return render_template('room/index.html', rooms=rooms)

@room_bp.route('/rooms/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        room_number = request.form.get('room_number')
        room_type = request.form.get('room_type')
        price = float(request.form.get('price'))
        capacity = int(request.form.get('capacity'))
        description = request.form.get('description')
        
        # Check if room number already exists
        if Room.query.filter_by(room_number=room_number).first():
            flash('Room number already exists', 'error')
            return redirect(url_for('room.new'))
        
        room = Room(
            room_number=room_number,
            room_type=room_type,
            price=price,
            capacity=capacity,
            description=description,
            status='available'
        )
        
        db.session.add(room)
        db.session.commit()
        
        flash('Room created successfully', 'success')
        return redirect(url_for('room.index'))
    
    return render_template('room/new.html')

@room_bp.route('/rooms/<int:id>')
@login_required
def show(id):
    room = Room.query.get_or_404(id)
    return render_template('room/show.html', room=room)

@room_bp.route('/rooms/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    room = Room.query.get_or_404(id)
    
    if request.method == 'POST':
        room.room_type = request.form.get('room_type')
        room.price = float(request.form.get('price'))
        room.capacity = int(request.form.get('capacity'))
        room.description = request.form.get('description')
        room.status = request.form.get('status')
        
        db.session.commit()
        flash('Room updated successfully', 'success')
        return redirect(url_for('room.show', id=room.id))
    
    return render_template('room/edit.html', room=room)

@room_bp.route('/rooms/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    room = Room.query.get_or_404(id)
    
    # Check if room has active bookings
    if room.bookings:
        flash('Cannot delete room with active bookings', 'error')
        return redirect(url_for('room.index'))
    
    db.session.delete(room)
    db.session.commit()
    
    flash('Room deleted successfully', 'success')
    return redirect(url_for('room.index')) 