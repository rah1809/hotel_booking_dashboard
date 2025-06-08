# Hotel Booking Analytics Dashboard

A comprehensive analytics dashboard for hotel booking data, providing strategic and operational insights for hotel management.

## Project Overview

This project delivers two dashboards, each designed with a specific business user, goal, and storyline in mind. The dashboards are intentionally connected: the first provides a strategic overview for executives, while the second offers operational insights for managers. Together, they enable data-driven decisions at every level of hotel management.

### 📊 Dashboard 1: Executive Performance Overview

- **Type:** Strategic Dashboard  
- **Target User:** Hotel Executives, Regional Directors  
- **User Goal:**  
  *"I want to quickly understand how our hotels are performing overall, spot trends, and identify areas needing attention."*

#### Storyline & Business Question:  
*"Are we meeting our business objectives, and where should we focus our strategic efforts?"*

#### How the Dashboard Solves the Problem:  
This dashboard aggregates high-level KPIs—total bookings, revenue, ADR, occupancy, and cancellations—across all hotels and segments. By comparing City vs Resort hotels and tracking trends over time, executives can:
- Monitor progress toward annual targets
- Identify underperforming segments or periods
- Make informed decisions about resource allocation and strategy

#### Key Charts & Their Connection:
- **Total Bookings & Revenue Trend:** Show overall business health and seasonality
- **ADR & Occupancy Rate:** Reveal pricing power and demand
- **Cancellation Ratio:** Highlights risk areas
- **Customer Type & Market Segment Distribution:** Identify which guest types drive business
- **City vs Resort Comparison:** Pinpoint which hotel types need attention

All charts are interlinked to answer the core question: *"Where are we winning, and where do we need to act?"*

### 📊 Dashboard 2: Revenue & Guest Behavior Insights

- **Type:** Analytical Dashboard  
- **Target User:** Revenue Managers, Operations Managers, Marketing Teams  
- **User Goal:**  
  *"I want to understand what drives revenue and guest behavior, so I can optimize pricing, reduce cancellations, and improve guest experience."*

#### Storyline & Business Question:  
*"What guest behaviors and channels drive our revenue, and how can we optimize them?"*

#### How the Dashboard Solves the Problem:  
This dashboard dives into the details behind the numbers, connecting guest behavior to revenue outcomes. It helps managers:
- Identify which channels and segments have the highest revenue or cancellation rates
- See how lead time affects ADR and booking patterns
- Understand guest preferences (special requests, country of origin) for targeted marketing

#### Key Charts & Their Connection:
- **Revenue by Channel & Market Segment:** Show where money is coming from and where it's lost
- **Cancellation Rate by Segment:** Pinpoint high-risk areas
- **ADR vs Lead Time:** Reveal booking behaviors that impact pricing
- **Special Requests & Guest Origin:** Inform service and marketing strategies

Each chart builds on the others to answer: *"How can we act on guest and channel insights to drive better results?"*

### 🔗 How the Dashboards Work Together

- **Dashboard 1** gives executives the "big picture" and flags areas for deeper analysis.
- **Dashboard 2** lets managers drill down, find root causes, and take action.
- The story flows from strategy to operations, ensuring every chart and metric is part of a unified, actionable business narrative.

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