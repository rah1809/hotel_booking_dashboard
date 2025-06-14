from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from app.models import db, Hotel, Room, Booking, Customer, ServiceRequest, MaintenanceRecord, CustomerFeedback, Staff

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Load and preprocess the dataset
data = pd.read_csv('hotel_booking_cleaned.csv')

# Helper function to clean data for JSON
def clean_for_json(data):
    cleaned = []
    for row in data:
        cleaned_row = []
        for val in row:
            if val is None or (isinstance(val, float) and math.isnan(val)):
                cleaned_row.append(0)
            else:
                cleaned_row.append(val)
        cleaned.append(cleaned_row)
    return cleaned

# Helper function to apply filters
def apply_filters(df, hotel=None, year=None, month=None):
    filtered = df.copy()
    if hotel and hotel != "All Hotels":
        filtered = filtered[filtered['hotel'] == hotel]
    if year and year != "All Years":
        filtered = filtered[filtered['arrival_date_year'] == int(year)]
    if month and month != "All Months":
        filtered = filtered[filtered['arrival_date_month'] == month]
    return filtered

# Route for Dashboard 1 (Strategic Overview)
@app.route('/')
def dashboard1():
    return render_template('dashboard1.html')

# Route for Dashboard 2 (Operational Analytics)
@app.route('/dashboard2')
def dashboard2():
    hotel = request.args.get('hotel')
    year = request.args.get('year')
    month = request.args.get('month')
    
    filtered = apply_filters(data, hotel, year, month)
    
    # 1. Cancellations by Market Segment
    cancel_by_segment = filtered.groupby('market_segment')['is_canceled'].value_counts().unstack(fill_value=0)
    cancel_by_segment = [
        (seg, int(cancel_by_segment.loc[seg].get(1, 0)), int(cancel_by_segment.loc[seg].get(0, 0)))
        for seg in cancel_by_segment.index
    ]
    
    # 2. ADR vs Lead Time (sample 200 rows for better visualization)
    lead_vs_adr = filtered[(filtered['adr'] > 0) & (filtered['lead_time'] > 0)][['lead_time', 'adr']]
    if len(lead_vs_adr) > 200:
        lead_vs_adr = lead_vs_adr.sample(n=200, random_state=1)
    lead_vs_adr = lead_vs_adr.values.tolist()
    
    # 3. Revenue by Distribution Channel
    revenue_by_channel = filtered.groupby('distribution_channel').apply(
        lambda x: (x['adr'] * (x['stays_in_weekend_nights'] + x['stays_in_week_nights'])).sum()
    )
    revenue_by_channel = [(ch, float(revenue_by_channel.loc[ch])) for ch in revenue_by_channel.index]
    
    # 4. Special Requests by Customer Type
    special_requests = filtered.groupby('customer_type')['total_of_special_requests'].mean()
    special_requests = [(ct, float(special_requests.loc[ct])) for ct in special_requests.index]
    
    # 5. Repeat vs New Guests
    repeat_guests = filtered['is_repeated_guest'].value_counts().sort_index()
    repeat_guests = [(int(k), int(v)) for k, v in repeat_guests.items()]
    
    return render_template(
        "dashboard2.html",
        cancel_by_segment=clean_for_json(cancel_by_segment),
        lead_vs_adr=clean_for_json(lead_vs_adr),
        revenue_by_channel=clean_for_json(revenue_by_channel),
        special_requests=clean_for_json(special_requests),
        repeat_guests=clean_for_json(repeat_guests)
    )

# Route for Dashboard 3 (Customer Insights)
@app.route('/dashboard3')
def dashboard3():
    """Strategic Revenue Management Dashboard"""
    return render_template('dashboard3.html')

# Route for Dashboard 4 (Revenue Optimization)
@app.route('/dashboard4')
def dashboard4():
    """Customer Insights Dashboard"""
    return render_template('dashboard4.html')

# Route for Dashboard 5 (Operational Efficiency)
@app.route('/dashboard5')
def dashboard5():
    """Operational Efficiency Dashboard"""
    return render_template('dashboard5.html')

# API route for hotel distribution data
@app.route('/hotel_data')
def hotel_data():
    hotel = request.args.get('hotel')
    year = request.args.get('year')
    month = request.args.get('month')
    
    filtered = apply_filters(data, hotel, year, month)
    hotel_counts = filtered['hotel'].value_counts()
    
    response = {
        'labels': list(hotel_counts.index),
        'counts': [int(x) for x in hotel_counts.values]
    }
    return jsonify(response)

# API route for cancellation data
@app.route('/cancellation_data')
def cancellation_data():
    hotel = request.args.get('hotel')
    year = request.args.get('year')
    month = request.args.get('month')
    
    filtered = apply_filters(data, hotel, year, month)
    cancel_counts = filtered['is_canceled'].value_counts().sort_index()
    
    not_canceled = int(cancel_counts.get(0, 0))
    canceled = int(cancel_counts.get(1, 0))
    
    response = {
        'labels': ['Not Canceled', 'Canceled'],
        'counts': [not_canceled, canceled]
    }
    return jsonify(response)

# API route for KPI data
@app.route('/kpi_data')
def kpi_data():
    hotel = request.args.get('hotel')
    year = request.args.get('year')
    month = request.args.get('month')
    
    filtered = apply_filters(data, hotel, year, month)
    
    total_bookings = len(filtered)
    total_revenue = (filtered['adr'] * (filtered['stays_in_weekend_nights'] + filtered['stays_in_week_nights'])).sum()
    avg_adr = filtered['adr'].mean() if not filtered.empty else 0
    occupancy_rate = 100 * (filtered['stays_in_weekend_nights'] + filtered['stays_in_week_nights']).mean() / 7 if not filtered.empty else 0
    
    kpis = {
        'total_bookings': int(total_bookings),
        'total_revenue': round(total_revenue, 2),
        'average_adr': round(avg_adr, 2),
        'occupancy_rate': round(occupancy_rate, 2)
    }
    
    return jsonify(kpis)

# API route for revenue trend data
@app.route('/revenue_data')
def revenue_data():
    hotel = request.args.get('hotel')
    year = request.args.get('year')
    
    filtered = apply_filters(data, hotel, year)
    
    months_order = ['January','February','March','April','May','June','July','August','September','October','November','December']
    revenue_by_month = filtered.groupby('arrival_date_month').apply(
        lambda x: (x['adr'] * (x['stays_in_weekend_nights'] + x['stays_in_week_nights'])).sum()
    ).reindex(months_order, fill_value=0)
    
    response = {
        'labels': list(revenue_by_month.index),
        'values': [float(x) for x in revenue_by_month.values]
    }
    return jsonify(response)

# API route for top countries data
@app.route('/top_countries_data')
def top_countries_data():
    hotel = request.args.get('hotel')
    year = request.args.get('year')
    month = request.args.get('month')
    
    filtered = apply_filters(data, hotel, year, month)
    
    if filtered.empty:
        return jsonify({'labels': ['No Data'], 'counts': [1]})
    
    top_countries = filtered['country'].value_counts().head(5)
    response = {
        'labels': list(top_countries.index),
        'counts': list(top_countries.values)
    }
    return jsonify(response)

# API route for market segment analysis
@app.route('/market_segment_data')
def market_segment_data():
    hotel = request.args.get('hotel')
    year = request.args.get('year')
    month = request.args.get('month')
    
    filtered = apply_filters(data, hotel, year, month)
    
    segment_analysis = filtered.groupby('market_segment').agg({
        'is_canceled': ['count', 'mean'],
        'adr': 'mean',
        'total_of_special_requests': 'mean'
    }).round(2)
    
    response = {
        'labels': list(segment_analysis.index),
        'bookings': [int(x) for x in segment_analysis[('is_canceled', 'count')]],
        'cancel_rate': [float(x) for x in segment_analysis[('is_canceled', 'mean')]],
        'avg_adr': [float(x) for x in segment_analysis[('adr', 'mean')]],
        'avg_special_requests': [float(x) for x in segment_analysis[('total_of_special_requests', 'mean')]]
    }
    return jsonify(response)

# API route for customer type analysis
@app.route('/customer_type_data')
def customer_type_data():
    hotel = request.args.get('hotel')
    year = request.args.get('year')
    month = request.args.get('month')
    
    filtered = apply_filters(data, hotel, year, month)
    
    customer_analysis = filtered.groupby('customer_type').agg({
        'is_canceled': ['count', 'mean'],
        'adr': 'mean',
        'total_of_special_requests': 'mean',
        'lead_time': 'mean'
    }).round(2)
    
    response = {
        'labels': list(customer_analysis.index),
        'bookings': [int(x) for x in customer_analysis[('is_canceled', 'count')]],
        'cancel_rate': [float(x) for x in customer_analysis[('is_canceled', 'mean')]],
        'avg_adr': [float(x) for x in customer_analysis[('adr', 'mean')]],
        'avg_special_requests': [float(x) for x in customer_analysis[('total_of_special_requests', 'mean')]],
        'avg_lead_time': [float(x) for x in customer_analysis[('lead_time', 'mean')]]
    }
    return jsonify(response)

@app.route('/routes')
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote(f"{rule.endpoint:30s} {methods:20s} {str(rule)}")
        output.append(line)
    return "<pre>" + "\n".join(output) + "</pre>"

# API endpoints for Dashboard 3 (Strategic Revenue Management)
@app.route('/api/revenue/trend')
def revenue_trend():
    period = request.args.get('period', 'monthly')
    hotel_type = request.args.get('hotel_type', 'all')
    
    query = db.session.query(
        func.date_trunc(period, Booking.check_in).label('period'),
        func.sum(Booking.total_amount).label('revenue')
    ).join(Room).join(Hotel)
    
    if hotel_type != 'all':
        query = query.filter(Hotel.type == hotel_type)
    
    results = query.group_by('period').order_by('period').all()
    
    return jsonify({
        'periods': [r.period.strftime('%Y-%m-%d') for r in results],
        'revenue': [float(r.revenue) for r in results]
    })

@app.route('/api/revenue/segments')
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

@app.route('/api/revenue/geographic')
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

# API endpoints for Dashboard 4 (Customer Insights)
@app.route('/api/customers/segmentation')
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

@app.route('/api/customers/satisfaction')
def customer_satisfaction():
    query = db.session.query(
        func.date_trunc('month', CustomerFeedback.created_at).label('month'),
        func.avg(CustomerFeedback.rating).label('avg_rating')
    ).group_by('month').order_by('month')
    
    results = query.all()
    
    return jsonify({
        'months': [r.month.strftime('%Y-%m') for r in results],
        'ratings': [float(r.avg_rating) for r in results]
    })

@app.route('/api/customers/channels')
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

# API endpoints for Dashboard 5 (Operational Efficiency)
@app.route('/api/operations/room-utilization')
def room_utilization():
    query = db.session.query(
        Room.room_type,
        func.count(Room.id).label('total_rooms'),
        func.sum(case((Room.status == 'occupied', 1), else_=0)).label('occupied_rooms')
    ).group_by(Room.room_type)
    
    results = query.all()
    
    return jsonify({
        'room_types': [r.room_type for r in results],
        'utilization': [float(r.occupied_rooms) / float(r.total_rooms) * 100 for r in results]
    })

@app.route('/api/operations/service-requests')
def service_requests():
    query = db.session.query(
        ServiceRequest.request_type,
        func.count(ServiceRequest.id).label('count'),
        func.avg(
            extract('epoch', ServiceRequest.completed_at - ServiceRequest.created_at)
        ).label('avg_response_time')
    ).group_by(ServiceRequest.request_type)
    
    results = query.all()
    
    return jsonify({
        'request_types': [r.request_type for r in results],
        'counts': [r.count for r in results],
        'response_times': [float(r.avg_response_time) / 3600 for r in results]  # Convert to hours
    })

@app.route('/api/operations/maintenance')
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

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)

print(data[(data['arrival_date_year'] == 2015) & (data['arrival_date_month'] == 'March')].shape) 