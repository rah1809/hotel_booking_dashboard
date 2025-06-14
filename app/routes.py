from flask import Blueprint, render_template, jsonify, request
from app.models import Hotel, Room, Customer, Booking, ServiceRequest, MaintenanceRecord, CustomerFeedback, Staff
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('dashboard3.html')

@main.route('/dashboard3')
def dashboard3():
    return render_template('dashboard3.html')

@main.route('/dashboard4')
def dashboard4():
    return render_template('dashboard4.html')

@main.route('/dashboard5')
def dashboard5():
    return render_template('dashboard5.html')

# API endpoints for Revenue Management Dashboard
@main.route('/api/revenue/trend')
def revenue_trend():
    period = request.args.get('period', 'month')
    hotel_type = request.args.get('hotel_type', 'all')
    
    query = db.session.query(
        func.date(Booking.check_in).label('date'),
        func.sum(Booking.total_amount).label('revenue')
    )
    
    if hotel_type != 'all':
        query = query.join(Room).join(Hotel).filter(Hotel.type == hotel_type)
    
    if period == 'month':
        query = query.group_by(func.strftime('%Y-%m', Booking.check_in))
    else:  # week
        query = query.group_by(func.strftime('%Y-%W', Booking.check_in))
    
    results = query.all()
    
    return jsonify({
        'dates': [r.date for r in results],
        'revenue': [float(r.revenue) for r in results]
    })

@main.route('/api/revenue/segments')
def revenue_segments():
    hotel_type = request.args.get('hotel_type', 'all')
    
    query = db.session.query(
        Customer.customer_type,
        func.sum(Booking.total_amount).label('revenue')
    ).join(Booking).join(Room).join(Hotel)
    
    if hotel_type != 'all':
        query = query.filter(Hotel.type == hotel_type)
    
    results = query.group_by(Customer.customer_type).all()
    
    return jsonify({
        'segments': [r.customer_type for r in results],
        'revenue': [float(r.revenue) for r in results]
    })

@main.route('/api/revenue/geographic')
def revenue_geographic():
    hotel_type = request.args.get('hotel_type', 'all')
    
    query = db.session.query(
        Customer.country,
        func.sum(Booking.total_amount).label('revenue')
    ).join(Booking).join(Room).join(Hotel)
    
    if hotel_type != 'all':
        query = query.filter(Hotel.type == hotel_type)
    
    results = query.group_by(Customer.country).all()
    
    return jsonify({
        'countries': [r.country for r in results],
        'revenue': [float(r.revenue) for r in results]
    })

# API endpoints for Customer Insights Dashboard
@main.route('/api/customers/segmentation')
def customer_segmentation():
    query = db.session.query(
        Customer.customer_type,
        func.count(Customer.id).label('count'),
        func.avg(Booking.total_amount).label('avg_spend')
    ).join(Booking).group_by(Customer.customer_type)
    
    results = query.all()
    
    return jsonify({
        'segments': [r.customer_type for r in results],
        'counts': [r.count for r in results],
        'avg_spend': [float(r.avg_spend) for r in results]
    })

@main.route('/api/customers/satisfaction')
def customer_satisfaction():
    query = db.session.query(
        func.strftime('%Y-%m', CustomerFeedback.created_at).label('month'),
        func.avg(CustomerFeedback.rating).label('avg_rating')
    ).group_by(func.strftime('%Y-%m', CustomerFeedback.created_at))
    
    results = query.all()
    
    return jsonify({
        'months': [r.month for r in results],
        'ratings': [float(r.avg_rating) for r in results]
    })

@main.route('/api/customers/channels')
def booking_channels():
    query = db.session.query(
        Booking.booking_channel,
        func.count(Booking.id).label('count'),
        func.avg(Booking.total_amount).label('avg_amount')
    ).group_by(Booking.booking_channel)
    
    results = query.all()
    
    return jsonify({
        'channels': [r.booking_channel for r in results],
        'counts': [r.count for r in results],
        'avg_amounts': [float(r.avg_amount) for r in results]
    })

# API endpoints for Operational Efficiency Dashboard
@main.route('/api/operations/room-utilization')
def room_utilization():
    query = db.session.query(
        Room.room_type,
        func.count(Room.id).label('total_rooms'),
        func.sum(case([(Room.status == 'occupied', 1)], else_=0)).label('occupied_rooms')
    ).group_by(Room.room_type)
    
    results = query.all()
    
    return jsonify({
        'room_types': [r.room_type for r in results],
        'utilization': [float(r.occupied_rooms) / float(r.total_rooms) * 100 for r in results]
    })

@main.route('/api/operations/service-requests')
def service_requests():
    query = db.session.query(
        ServiceRequest.request_type,
        func.count(ServiceRequest.id).label('count'),
        func.avg(func.extract('epoch', ServiceRequest.completed_at - ServiceRequest.created_at) / 3600).label('avg_response_time')
    ).group_by(ServiceRequest.request_type)
    
    results = query.all()
    
    return jsonify({
        'request_types': [r.request_type for r in results],
        'counts': [r.count for r in results],
        'avg_response_times': [float(r.avg_response_time) for r in results]
    })

@main.route('/api/operations/maintenance')
def maintenance_metrics():
    query = db.session.query(
        MaintenanceRecord.maintenance_type,
        func.count(MaintenanceRecord.id).label('count'),
        func.avg(MaintenanceRecord.cost).label('avg_cost')
    ).group_by(MaintenanceRecord.maintenance_type)
    
    results = query.all()
    
    return jsonify({
        'maintenance_types': [r.maintenance_type for r in results],
        'counts': [r.count for r in results],
        'avg_costs': [float(r.avg_cost) for r in results]
    }) 