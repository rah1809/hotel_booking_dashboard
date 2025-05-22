## ✅ Step 2: Database Integration – Hotel Booking Dashboard

### 🔗 1. Database Connection

You've successfully connected your dashboards to the database created in **Capstone Project 2**:

* **Database Format:** SQLite (`hotel_booking.db`)
* **Connection Method (Streamlit version):**

```python
import sqlite3
conn = sqlite3.connect("data/hotel_booking.db")
cursor = conn.cursor()
```

* **Connection Method (Flask version, with SQLAlchemy):**

```python
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/hotel_booking.db'
db = SQLAlchemy(app)
```

---

### ⚙️ 2. Query Optimization and Filtering

Your dashboard supports filtering and aggregation based on:

* `hotel` (City Hotel or Resort Hotel)
* `arrival_date_year` (2015–2017)
* `arrival_date_month` (January–December)

**Optimized Pandas Query Example (Streamlit):**

```python
filtered_df = df[
    (df["hotel"] == selected_hotel) &
    (df["arrival_date_year"] == selected_year) &
    (df["arrival_date_month"] == selected_month)
]
```

**SQL Query Example:**

```sql
SELECT hotel, COUNT(*) as booking_count
FROM bookings
WHERE arrival_date_year = 2016 AND hotel = 'City Hotel'
GROUP BY hotel;
```

---

### 📊 3. Aggregations Performed

* **Total Bookings**: `COUNT(*)`
* **Total Revenue**: `SUM(adr * stays)`
* **Occupancy Rate**: `booked_nights / available_nights`
* **Lead Time Average**: `AVG(lead_time)`
* **Cancellations by Segment**: `GROUP BY market_segment, is_canceled`

---

### ✅ Deliverables

| Deliverable                     | File / Code Reference                                             |
| ------------------------------- | ----------------------------------------------------------------- |
| SQL Queries                     | `docs/DATABASE_INTEGRATION.md`, inline in code                    |
| Database Connection Code        | `streamlit_app.py` or `app.py` (Flask)                            |
| Optimized Filtering Logic       | `streamlit_app.py` / Flask routes                                 |
| Aggregation Code for Visuals    | All chart functions using groupby or SQL `GROUP BY`               |
| Data Migration Script (if used) | `migrate_data.py` (optional but useful for moving from CSV to DB) |

---

### 🧠 Summary

* Your dashboards dynamically pull data from a SQLite database created in Capstone Project 2.
* Queries are filtered based on user input for hotel, year, and month.
* All charts and KPIs are powered by efficient SQL or pandas-based queries using aggregations.
* SQL queries and integration logic are well-documented and follow best practices. 