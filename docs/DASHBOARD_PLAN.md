# Hotel Booking Dashboard Plan

## Overview
This dashboard provides comprehensive analytics for hotel booking data, split into two main views:
1. Booking Trends Overview
2. Revenue & Guest Behavior

## ✅ Step 1: Dashboard Requirements – Hotel Booking Dashboard

### 🎯 End Users

* **Hotel Managers & Executives** – to make strategic decisions based on guest behavior, booking trends, and revenue sources.
* **Marketing Teams** – to identify key customer segments and booking sources for targeted campaigns.
* **Revenue Analysts** – to monitor KPIs like ADR, revenue, cancellations, and optimize distribution channels.

---

### 📊 Key Metrics

The dashboards focus on these critical KPIs:

* **Total Bookings**
* **Average Daily Rate (ADR)**
* **Total Revenue**
* **Occupancy Rate**
* **Cancellations by Segment**
* **Guest Type Distribution (Repeat vs. New)**
* **Special Requests by Customer Type**
* **Top Guest Countries**
* **Lead Time vs ADR Trends**

---

### 📈 Chart Types Chosen

| Insight                           | Chart Type     | Reason                                           |
| --------------------------------- | -------------- | ------------------------------------------------ |
| Bookings by Hotel Type            | Bar Chart      | Easy comparison of booking volume                |
| Cancellation Distribution         | Pie Chart      | Visual proportion of cancelled vs. confirmed     |
| Monthly ADR Trend                 | Line Chart     | Shows seasonal pricing behavior                  |
| Customer Type Distribution        | Doughnut Chart | Compare repeat vs new guests visually            |
| Cancellations by Market Segment   | Grouped Bar    | Highlights differences in behavior by segment    |
| ADR vs Lead Time                  | Scatter Plot   | Detect correlation between price and lead time   |
| Revenue by Distribution Channel   | Pie Chart      | Identify top revenue sources                     |
| Special Requests by Customer Type | Stacked Bar    | Understand service expectations by customer type |
| Top 5 Guest Countries             | Doughnut Chart | Geographic trend analysis                        |

---

### 📚 Storytelling Approach

This dashboard tells the **data story from two key perspectives**:

1. **Booking Trends Overview**
   * How bookings, revenue, and cancellations vary across hotel types and time periods
   * What kind of guests are being served and how customer behavior evolves
   * Which KPIs matter most to monitor hotel performance

2. **Revenue & Guest Behavior**
   * Which market segments are driving or losing revenue
   * How guest behavior (lead time, special requests, repeat guests) affects revenue
   * How distribution channels and geographies influence performance

---

### 🧭 Dashboard Type

* **Booking Trends** → **Analytical Dashboard**  
  Focus: KPIs, time trends, categorical analysis.

* **Revenue & Guest Behavior** → **Operational Dashboard**  
  Focus: behavioral insights, booking patterns, channel and guest segmentation.

---

### 📄 Deliverable

✅ A detailed dashboard plan has been outlined above, describing:

* Key features per dashboard  
* End user focus  
* Selected visualizations and chart justifications  
* The story each dashboard is designed to tell

## Dashboard 1: Booking Trends Overview

### Purpose
Monitor key booking metrics and trends to understand overall hotel performance.

### Components
1. **KPI Cards**
   - Total Bookings
   - Total Revenue
   - Active Bookings
   - Average Daily Rate

2. **Visualizations**
   - Bookings by Hotel Type (bar)
   - Cancellation Distribution (pie)
   - Monthly ADR Trend (line)
   - Customer Type Distribution (bar)

### Filters
- Hotel Type
- Year
- Month

## Dashboard 2: Revenue & Guest Behavior

### Purpose
Analyze revenue patterns and guest behavior to optimize business strategies.

### Components
1. **Visualizations**
   - Bookings by Market Segment (bar)
   - ADR vs Lead Time (scatter)
   - Revenue by Distribution Channel (pie)
   - Special Requests by Customer Type (bar)
   - Top 10 Guest Countries (bar)
   - New vs Repeat Guests (pie)

### Filters
- Hotel Type
- Year
- Month

## Technical Implementation
- Streamlit for interactive dashboard
- Plotly for visualizations
- Pandas for data processing
- SQLite for data storage
- Caching for performance

## User Experience
- Intuitive sidebar navigation
- Responsive layout
- Interactive charts
- Real-time filter updates 

import sqlite3
import pandas as pd
import streamlit as st

# Cached database connection
@st.cache_resource
def get_connection():
    return sqlite3.connect("data/hotel_booking.db", check_same_thread=False)

# Query helper
def run_query(query):
    conn = get_connection()
    return pd.read_sql_query(query, conn)

# Example: Total bookings by hotel
query = """
SELECT hotel, COUNT(*) AS total_bookings
FROM bookings
GROUP BY hotel
"""
df = run_query(query)

st.subheader("Total Bookings by Hotel")
st.bar_chart(df.set_index("hotel"))

hotel = st.selectbox("Select Hotel", ["City Hotel", "Resort Hotel"])
year = st.selectbox("Select Year", [2016, 2017])
month = st.selectbox("Select Month", ["January", "February", "March"])

query = f"""
SELECT arrival_date_month, AVG(adr) as avg_adr
FROM bookings
WHERE hotel = '{hotel}'
  AND arrival_date_year = {year}
  AND arrival_date_month = '{month}'
GROUP BY arrival_date_month
"""

df = run_query(query)
st.line_chart(df.set_index("arrival_date_month"))

def test_db_connection():
    try:
        conn = sqlite3.connect("data/hotel_booking.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables
    except Exception as e:
        return str(e)

with st.sidebar.expander("🔎 Database Connection Test"):
    tables = test_db_connection()
    if isinstance(tables, list):
        if "bookings" in tables:
            st.success("✅ Connected to SQLite! Table 'bookings' exists.")
        else:
            st.warning(f"Connected, but 'bookings' table not found. Tables: {tables}")
    else:
        st.error(f"Connection error: {tables}") 