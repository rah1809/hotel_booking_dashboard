# Hotel Booking Dashboard

An interactive dashboard built with Streamlit to analyze hotel booking data.

## Features

- Interactive filters for hotel, year, and month
- Real-time KPI metrics
- Multiple visualizations (bar, pie, line charts)
- Responsive layout
- Cached data loading for better performance

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Place your hotel bookings CSV file in the `data` directory:
```bash
mkdir -p data
# Copy your hotel_bookings.csv to data/
```

4. Run the Streamlit app:
```bash
streamlit run src/streamlit_app.py
```

## Project Structure

```
hotel_booking_dashboard/
├── data/
│   └── hotel_bookings.csv
├── src/
│   ├── streamlit_app.py
│   ├── components/
│   ├── utils/
│   └── pages/
├── requirements.txt
└── README.md
```

## Development

- The app uses SQLite for faster data loading after initial CSV import
- All data processing is cached for better performance
- Charts are built with Plotly for interactivity

## Deployment

1. Push your code to GitHub
2. Sign up for Streamlit Cloud
3. Connect your GitHub repository
4. Deploy!

## Contributing

Feel free to submit issues and enhancement requests! 