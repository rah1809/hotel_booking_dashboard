# Hotel Booking Dashboard

A comprehensive hotel booking analytics dashboard built with Flask, SQLite, and modern web technologies.

## Features

- Strategic Revenue Management Dashboard
- Customer Insights Dashboard
- Operational Efficiency Dashboard
- Interactive visualizations and filters
- Real-time data updates
- Responsive design

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hotel_booking_dashboard
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python
>>> from app import db
>>> db.create_all()
>>> exit()
```

5. Seed the database with sample data:
```bash
python seed_data.py
```

## Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Dashboard Access

- Overview Dashboard: http://localhost:5000/
- Revenue Management Dashboard: http://localhost:5000/dashboard3
- Customer Insights Dashboard: http://localhost:5000/dashboard4
- Operations Dashboard: http://localhost:5000/dashboard5

## Project Structure

```
hotel_booking_dashboard/
├── app.py                 # Main application file
├── app/
│   ├── models.py         # Database models
│   └── __init__.py       # Application factory
├── templates/
│   ├── base.html         # Base template
│   ├── dashboard3.html   # Revenue Management Dashboard
│   ├── dashboard4.html   # Customer Insights Dashboard
│   └── dashboard5.html   # Operations Dashboard
├── static/
│   ├── css/             # CSS files
│   └── js/              # JavaScript files
├── requirements.txt      # Project dependencies
└── seed_data.py         # Database seeding script
```

## Technologies Used

- Backend:
  - Flask
  - SQLAlchemy
  - SQLite

- Frontend:
  - HTML5
  - CSS3 (Tailwind CSS)
  - JavaScript
  - Chart.js

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 