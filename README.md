# Hotel Booking Analytics Dashboard

A comprehensive analytics dashboard for hotel booking data, providing strategic and operational insights for hotel management.

## Project Overview

This project includes two purpose-driven dashboards designed to meet the distinct needs of strategic decision-makers and operational managers within the hospitality sector. Each dashboard is tailored with specific users, goals, and metrics in mind, ensuring actionable insights aligned to business priorities.

### 📊 Dashboard 1: Booking Trends Overview
* **Type:** Strategic Dashboard
* **Primary Purpose:** To provide a high-level overview of hotel performance across key dimensions such as bookings, revenue, pricing, occupancy, and customer segmentation.
* **Target Audience:** Hotel Executives, Regional Directors, Strategy Teams

#### Key Metrics Tracked:
* Total Bookings & Total Revenue
* Average Daily Rate (ADR)
* Occupancy Rate
* Cancellation Ratio (%)
* Customer Type Distribution
* Seasonal ADR Trends
* City vs Resort Hotel Comparisons

### 📊 Dashboard 2: Revenue & Guest Behavior
* **Type:** Analytical Dashboard
* **Primary Purpose:** To uncover patterns in guest behavior, booking channels, and revenue drivers to support tactical optimization.
* **Target Audience:** Hotel Managers, Revenue Managers, Marketing & Operations Teams

#### Key Metrics Tracked:
* Revenue by Distribution Channel
* Cancellation Rate by Market Segment
* ADR vs Lead Time
* Special Requests by Customer Type
* Guest Origin by Country

### 🔁 Holistic Insight Integration
Together, these dashboards form a dual-layered decision support system:
* **Dashboard 1** provides the strategic "big picture" for executives to guide long-term goals.
* **Dashboard 2** dives into operational intelligence, offering granular insights that help hotel teams fine-tune processes and improve guest experience.

## Features

- Interactive data visualization with Chart.js
- Real-time filtering by hotel, year, and month
- Responsive design using Tailwind CSS
- Comprehensive KPI tracking
- Detailed market segment analysis
- Customer behavior insights
- Revenue optimization recommendations

## Technical Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, JavaScript, Tailwind CSS
- **Data Visualization:** Chart.js
- **Database:** SQLite (via Pandas)
- **Data Processing:** Pandas, NumPy

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hotel-booking-dashboard
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare the dataset**
   - Place the `hotel_booking_cleaned.csv` file in the project root directory
   - Ensure the CSV file has the required columns (see Data Structure section)

5. **Run the application**
   ```bash
   python app.py
   ```
   The dashboard will be available at `http://localhost:5002`

## Data Structure

The application expects a CSV file with the following key columns:
- `hotel`: Hotel type (City/Resort)
- `arrival_date_year`: Year of arrival
- `arrival_date_month`: Month of arrival
- `is_canceled`: Booking cancellation status
- `adr`: Average Daily Rate
- `market_segment`: Market segment of the booking
- `distribution_channel`: Booking distribution channel
- `customer_type`: Type of customer
- `total_of_special_requests`: Number of special requests
- `stays_in_weekend_nights`: Weekend nights booked
- `stays_in_week_nights`: Weekday nights booked
- `lead_time`: Days between booking and arrival
- `country`: Guest's country of origin

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Hotel booking dataset provided by [source]
- Chart.js for data visualization
- Tailwind CSS for styling
- Flask framework for backend 