# Hotel Booking Dashboard

An interactive dashboard built with Streamlit and Flask to analyze hotel booking data.

## Features

- Interactive filters for hotel, year, and month
- Real-time KPI metrics
- Multiple visualizations (bar, pie, line charts)
- Responsive layout
- Cached data loading for better performance
- Dual interface: Streamlit dashboard and Flask web application

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

3. Run the Streamlit app:
```bash
streamlit run src/streamlit_app.py
```

4. Run the Flask app:
```bash
python app.py
```

## Project Structure

```
hotel_booking_dashboard/
├── src/
│   ├── streamlit_app.py      # Main Streamlit application
│   ├── components/           # Reusable Streamlit components
│   ├── utils/               # Utility functions
│   └── pages/               # Streamlit pages
├── app.py                   # Flask application
├── templates/               # Flask HTML templates
├── static/                  # Static files (CSS, JS, images)
├── data/                    # Data files
├── docs/                    # Documentation
├── requirements.txt         # Project dependencies
└── README.md               # Project documentation
```

## Development

- The app uses SQLite for faster data loading after initial CSV import
- All data processing is cached for better performance
- Charts are built with Plotly for interactivity
- Flask backend provides RESTful API endpoints
- Streamlit frontend offers interactive data exploration

## Deployment

1. Push your code to GitHub
2. Sign up for Streamlit Cloud
3. Connect your GitHub repository
4. Deploy!

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License 