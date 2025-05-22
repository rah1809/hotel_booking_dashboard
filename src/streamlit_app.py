import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sqlite3
import calendar
import io

# --- THEME & COLOR PALETTE ---
COLORS = {
    'primary': '#36a2eb',
    'success': '#2ca02c',
    'warning': '#ffb300',
    'danger': '#d62728',
    'neutral': '#7f7f7f',
    'hotel_colors': ['#36a2eb', '#ffb300'],
    'status_colors': ['#2ca02c', '#d62728'],
    'segment_colors': px.colors.qualitative.Set3,
    'sequential': px.colors.sequential.Viridis
}

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Hotel Booking Dashboard",
    page_icon="hotel",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR DARK/LIGHT MODE & SPACING ---
st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        background-color: #23272f !important;
        color: #f0f2f6 !important;
    }
    .stMetric {
        background-color: #18191a;
        color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .stMetricLabel, .stMetricValue {
        font-size: 1.1rem !important;
    }
    .chart-container {
        background-color: #18191a;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #36a2eb;
    }
    .stSelectbox, .stRadio {
        background-color: #23272f !important;
        color: #f0f2f6 !important;
        border-radius: 0.5rem;
    }
    label, .stRadio label {
        color: #f0f2f6 !important;
    }
    hr {
        border: 1px solid #23272f;
        margin: 1.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA LOADING & CACHING ---
BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / "data" / "hotel_bookings.csv"
DB_PATH = BASE_DIR / "data" / "hotel_bookings.db"

@st.cache_data(show_spinner="Loading data...")
def load_data():
    if DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql("SELECT * FROM bookings", conn)
        conn.close()
        return df
    if not DATA_PATH.exists():
        st.error(f"Data file not found at {DATA_PATH.absolute()}")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    try:
        conn = sqlite3.connect(DB_PATH)
        df.to_sql("bookings", conn, if_exists="replace", index=False)
        conn.close()
    except Exception:
        pass
    return df

def get_filtered_data(df, hotel, year, month):
    mask = pd.Series(True, index=df.index)
    if hotel and hotel != "All Hotels":
        mask &= df["hotel"] == hotel
    if year and year != "All Years":
        mask &= df["arrival_date_year"] == int(year)
    if month and month != "All Months":
        mask &= df["arrival_date_month"] == month
    return df[mask]

# --- LOAD DATA ---
df = load_data()

# --- SIDEBAR: NAVIGATION & FILTERS ---
st.sidebar.title("Hotel Booking Dashboard")
st.sidebar.header("Filters")
hotel = st.sidebar.selectbox(
    "Hotel",
    ["All Hotels"] + sorted(df["hotel"].unique())
)
year = st.sidebar.selectbox(
    "Year",
    ["All Years"] + sorted(df["arrival_date_year"].unique())
)
month = st.sidebar.selectbox(
    "Month",
    ["All Months"] + list(calendar.month_name)[1:]
)

# --- FILTERED DATA ---
filtered_df = get_filtered_data(df, hotel, year, month)

# --- EXPORT BUTTON ---
buffer = io.BytesIO()
filtered_df.to_csv(buffer, index=False)
st.sidebar.download_button(
    label="⬇️ Download Filtered Data (CSV)",
    data=buffer.getvalue(),
    file_name="filtered_hotel_bookings.csv",
    mime="text/csv"
)

# --- KPI CARDS ---
def kpi_cards(df):
    total_bookings = len(df)
    total_revenue = (df["adr"] * (df["stays_in_weekend_nights"] + df["stays_in_week_nights"])).sum()
    avg_adr = df["adr"].mean()
    total_nights = (df["stays_in_weekend_nights"] + df["stays_in_week_nights"]).sum()
    occupancy_rate = (total_nights / (len(df) * 7) * 100) if len(df) > 0 else 0
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Bookings", f"{total_bookings:,}")
    with col2:
        st.metric("Total Revenue", f"${total_revenue:,.2f}")
    with col3:
        st.metric("Avg. Daily Rate", f"${avg_adr:.2f}")
    with col4:
        st.metric("Occupancy Rate", f"{occupancy_rate:.1f}%")

# --- DASHBOARD 1: BOOKING TRENDS OVERVIEW ---
def dashboard1(df):
    st.title("Booking Trends Overview")
    st.markdown("""
    Analyze booking patterns, cancellations, and customer types. Use the filters to drill down by hotel, year, or month.
    """)
    kpi_cards(df)
    st.markdown("---")
    # Charts
    col1, col2 = st.columns(2)
    with col1:
        # Bookings by Hotel Type
        hotel_bookings = df["hotel"].value_counts().reset_index()
        hotel_bookings.columns = ["hotel", "count"]
        fig = px.bar(
            hotel_bookings, x="hotel", y="count",
            title="Bookings by Hotel Type",
            color="hotel", color_discrete_sequence=COLORS['hotel_colors'],
            template="plotly_white"
        )
        fig.update_layout(title_x=0.5, xaxis_title="Hotel Type", yaxis_title="Number of Bookings")
        st.plotly_chart(fig, use_container_width=True)
        st.info("City Hotel (blue) consistently receives more bookings than Resort Hotel (yellow/orange), especially during peak months.")
    with col2:
        # Cancellation Distribution
        cancel_dist = df["is_canceled"].value_counts().reset_index()
        cancel_dist.columns = ["status", "count"]
        cancel_dist["status"] = cancel_dist["status"].map({0: "Not Canceled", 1: "Canceled"})
        fig = px.pie(
            cancel_dist, values="count", names="status",
            title="Cancellation Distribution",
            color="status", color_discrete_map={"Not Canceled": COLORS['success'], "Canceled": COLORS['danger']},
            template="plotly_white"
        )
        fig.update_layout(title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)
        st.info("Most bookings are not canceled (green), but a significant portion are canceled (red), impacting revenue and planning.")
    col3, col4 = st.columns(2)
    with col3:
        # Monthly ADR Trend
        monthly_adr = df.groupby("arrival_date_month")["adr"].mean().reset_index()
        # Ensure months are in order
        monthly_adr["month_num"] = monthly_adr["arrival_date_month"].apply(lambda x: list(calendar.month_name).index(x))
        monthly_adr = monthly_adr.sort_values("month_num")
        fig = px.line(
            monthly_adr, x="arrival_date_month", y="adr",
            title="Monthly ADR Trend", markers=True,
            template="plotly_white", color_discrete_sequence=[COLORS['primary']]
        )
        fig.update_layout(title_x=0.5, xaxis_title="Month", yaxis_title="Average Daily Rate ($)")
        st.plotly_chart(fig, use_container_width=True)
        st.info("ADR (average daily rate) peaks in summer, indicating higher pricing during high-demand months.")
    with col4:
        # Customer Type Distribution
        customer_dist = df["customer_type"].value_counts().reset_index()
        customer_dist.columns = ["type", "count"]
        fig = px.bar(
            customer_dist, x="type", y="count",
            title="Customer Type Distribution",
            color="type", color_discrete_sequence=COLORS['segment_colors'],
            template="plotly_white"
        )
        fig.update_layout(title_x=0.5, xaxis_title="Customer Type", yaxis_title="Number of Bookings")
        st.plotly_chart(fig, use_container_width=True)
        st.info("Transient and Contract customers make up the majority of bookings, with Group and Corporate segments being smaller.")
    st.markdown("---")
    st.subheader("Key Takeaways")
    st.markdown("""
    - **City Hotel dominates bookings, especially in summer.**
    - **Cancellations are significant and should be monitored for revenue impact.**
    - **Transient customers are the largest segment, driving most bookings.**
    """)

# --- DASHBOARD 2: REVENUE & GUEST BEHAVIOR ---
def dashboard2(df):
    st.title("Revenue & Guest Behavior")
    st.markdown("""
    Explore revenue sources, guest behavior, and market segmentation. Use the filters to focus your analysis.
    """)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        # Cancellations by Market Segment
        segment_cancel = df.groupby(["market_segment", "is_canceled"]).size().reset_index(name="count")
        segment_cancel["status"] = segment_cancel["is_canceled"].map({0: "Not Canceled", 1: "Canceled"})
        fig = px.bar(
            segment_cancel, x="market_segment", y="count", color="status",
            barmode="stack", title="Cancellations by Market Segment",
            color_discrete_map={"Not Canceled": COLORS['success'], "Canceled": COLORS['danger']},
            template="plotly_white"
        )
        fig.update_layout(title_x=0.5, xaxis_title="Market Segment", yaxis_title="Number of Bookings")
        st.plotly_chart(fig, use_container_width=True)
        st.info("TA/TO (Travel Agent/Tour Operator) segment has the highest cancellation rate (red), while Direct and Corporate are more stable (green).")
    with col2:
        # ADR vs Lead Time
        sample_df = df[(df["adr"] > 0) & (df["lead_time"] > 0)].sample(min(500, len(df)), random_state=42)
        fig = px.scatter(
            sample_df, x="lead_time", y="adr", color="hotel",
            title="ADR vs Lead Time",
            color_discrete_sequence=COLORS['hotel_colors'],
            opacity=0.7, template="plotly_white"
        )
        fig.update_layout(title_x=0.5, xaxis_title="Lead Time (days)", yaxis_title="Average Daily Rate ($)")
        st.plotly_chart(fig, use_container_width=True)
        st.info("Bookings made further in advance (higher lead time) tend to have lower ADR, especially for Resort Hotel (yellow/orange).")
    col3, col4 = st.columns(2)
    with col3:
        # Revenue by Distribution Channel
        df["revenue"] = df["adr"] * (df["stays_in_weekend_nights"] + df["stays_in_week_nights"])
        channel_revenue = df.groupby("distribution_channel")["revenue"].sum().reset_index()
        fig = px.pie(
            channel_revenue, values="revenue", names="distribution_channel",
            title="Revenue by Distribution Channel",
            color_discrete_sequence=COLORS['segment_colors'],
            template="plotly_white"
        )
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)
        st.info("Direct and TA/TO channels generate the most revenue, with Corporate and GDS channels contributing less.")
    with col4:
        # Special Requests by Customer Type
        special_requests = df.groupby("customer_type")["total_of_special_requests"].mean().reset_index()
        fig = px.bar(
            special_requests, x="customer_type", y="total_of_special_requests",
            title="Avg. Special Requests by Customer Type",
            color="customer_type", color_discrete_sequence=COLORS['segment_colors'],
            template="plotly_white"
        )
        fig.update_layout(title_x=0.5, xaxis_title="Customer Type", yaxis_title="Avg. Special Requests")
        st.plotly_chart(fig, use_container_width=True)
        st.info("Transient customers make the most special requests, indicating higher service expectations.")
    st.markdown("---")
    # Top 5 Guest Countries (Doughnut)
    top_countries = df["country"].value_counts().head(5).reset_index()
    top_countries.columns = ["country", "count"]
    fig = px.pie(
        top_countries, values="count", names="country",
        title="Top 5 Guest Countries",
        hole=0.5, color_discrete_sequence=COLORS['sequential'],
        template="plotly_white"
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
    st.info("Most guests come from Portugal, followed by the UK and France, highlighting key international markets.")
    st.markdown("---")
    st.subheader("Key Takeaways")
    st.markdown("""
    - **TA/TO segment has the highest cancellation rate, impacting revenue stability.**
    - **Direct and TA/TO channels are the main revenue drivers.**
    - **Portugal, UK, and France are the top guest origins, suggesting where to focus marketing.**
    """)

# --- TOP NAVIGATION ---
tab1, tab2 = st.tabs([
    "Booking Trends Overview",
    "Revenue & Guest Behavior"
])

# --- MAIN APP LOGIC ---
with st.spinner("Rendering dashboard..."):
    with tab1:
        dashboard1(filtered_df)
    with tab2:
        dashboard2(filtered_df)