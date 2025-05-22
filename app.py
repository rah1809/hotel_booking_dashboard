from flask import Flask, render_template, jsonify, request
import pandas as pd
import math

# Initialize the Flask app
app = Flask(__name__)

# Load the dataset
data = pd.read_csv('hotel_booking_cleaned.csv')

# Route for Dashboard 1
@app.route('/')
def dashboard1():
    return render_template('dashboard1.html')

# API route to send data for Chart.js
@app.route('/hotel_data')
def hotel_data():
    hotel = request.args.get('hotel')
    year = request.args.get('year')
    month = request.args.get('month')

    filtered = data.copy()
    if hotel and hotel != "All Hotels":
        filtered = filtered[filtered['hotel'] == hotel]
    if year and year != "All Years":
        filtered = filtered[filtered['arrival_date_year'] == int(year)]
    if month and month != "All Months":
        filtered = filtered[filtered['arrival_date_month'] == month]

    hotel_counts = filtered['hotel'].value_counts()
    response = {
        'labels': list(hotel_counts.index),
        'counts': [int(x) for x in hotel_counts.values]
    }
    return jsonify(response)

# API route for booking cancellation status
@app.route('/cancellation_data')
def cancellation_data():
    hotel = request.args.get('hotel')
    year = request.args.get('year')
    month = request.args.get('month')

    filtered = data.copy()
    if hotel and hotel != "All Hotels":
        filtered = filtered[filtered['hotel'] == hotel]
    if year and year != "All Years":
        filtered = filtered[filtered['arrival_date_year'] == int(year)]
    if month and month != "All Months":
        filtered = filtered[filtered['arrival_date_month'] == month]

    cancel_counts = filtered['is_canceled'].value_counts().sort_index()
    # Always return [not_canceled, canceled] counts
    not_canceled = int(cancel_counts.get(0, 0))
    canceled = int(cancel_counts.get(1, 0))
    response = {
        'labels': ['Not Canceled', 'Canceled'],
        'counts': [not_canceled, canceled]
    }
    return jsonify(response)

# API route for KPIs (now with filters)
@app.route('/kpi_data')
def kpi_data():
    hotel = request.args.get('hotel')
    year = request.args.get('year')
    month = request.args.get('month')

    filtered = data.copy()
    if hotel and hotel != "All Hotels":
        filtered = filtered[filtered['hotel'] == hotel]
    if year and year != "All Years":
        filtered = filtered[filtered['arrival_date_year'] == int(year)]
    if month and month != "All Months":
        filtered = filtered[filtered['arrival_date_month'] == month]

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

# API route for revenue trend by month
@app.route('/revenue_data')
def revenue_data():
    hotel = request.args.get('hotel')
    year = request.args.get('year')

    filtered = data.copy()
    if hotel and hotel != "All Hotels":
        filtered = filtered[filtered['hotel'] == hotel]
    if year and year != "All Years":
        filtered = filtered[filtered['arrival_date_year'] == int(year)]

    months_order = ['January','February','March','April','May','June','July','August','September','October','November','December']
    revenue_by_month = filtered.groupby('arrival_date_month').apply(
        lambda x: (x['adr'] * (x['stays_in_weekend_nights'] + x['stays_in_week_nights'])).sum()
    ).reindex(months_order, fill_value=0)

    response = {
        'labels': list(revenue_by_month.index),
        'values': [float(x) for x in revenue_by_month.values]
    }
    return jsonify(response)

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

@app.route('/dashboard2')
def dashboard2():
    hotel = request.args.get('hotel')
    year = request.args.get('year')
    month = request.args.get('month')
    filtered = data.copy()
    if hotel and hotel != "All Hotels":
        filtered = filtered[filtered['hotel'] == hotel]
    if year and year != "All Years":
        filtered = filtered[filtered['arrival_date_year'] == int(year)]
    if month and month != "All Months":
        filtered = filtered[filtered['arrival_date_month'] == month]

    # 1. Cancellations by Market Segment
    cancel_by_segment = filtered.groupby('market_segment')['is_canceled'].value_counts().unstack(fill_value=0)
    cancel_by_segment = [
        (seg, int(cancel_by_segment.loc[seg].get(1, 0)), int(cancel_by_segment.loc[seg].get(0, 0)))
        for seg in cancel_by_segment.index
    ]

    # 2. ADR vs Lead Time (sample 200 rows)
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

# API route for top countries data
@app.route('/top_countries_data')
def top_countries_data():
    hotel = request.args.get('hotel')
    year = request.args.get('year')
    month = request.args.get('month')

    filtered = data.copy()
    if hotel and hotel != "All Hotels":
        filtered = filtered[filtered['hotel'] == hotel]
    if year and year != "All Years":
        filtered = filtered[filtered['arrival_date_year'] == int(year)]
    if month and month != "All Months":
        filtered = filtered[filtered['arrival_date_month'] == month]

    if filtered.empty:
        return jsonify({'labels': ['No Data'], 'counts': [1]})

    top_countries = filtered['country'].value_counts().head(5)
    response = {
        'labels': list(top_countries.index),
        'counts': list(top_countries.values)
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

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5002)

print(data[(data['arrival_date_year'] == 2015) & (data['arrival_date_month'] == 'March')].shape) 