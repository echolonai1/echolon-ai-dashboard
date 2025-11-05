import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ============ Page Config ============
st.set_page_config(page_title="Echolon AI Dashboard", layout="wide", page_icon="🚀")

# ============ Custom CSS ============
st.markdown("""
<style>
/* Global Styles */
body {
  background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 100%);
  color: #fff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Neon Header */
.neon-header {
  font-size: 3em;
  font-weight: 900;
  text-align: center;
  color: #00d9ff;
  text-shadow: 0 0 10px #00d9ff, 0 0 20px #00d9ff, 0 0 30px #00d9ff, 0 0 40px #00d9ff;
  margin-bottom: 20px;
  animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
  from { text-shadow: 0 0 10px #00d9ff, 0 0 20px #00d9ff, 0 0 30px #00d9ff, 0 0 40px #00d9ff; }
  to { text-shadow: 0 0 20px #00d9ff, 0 0 30px #00d9ff, 0 0 40px #00d9ff, 0 0 50px #00d9ff; }
}

/* Card Styling */
.metric-card {
  background: linear-gradient(145deg, #1e1e3f, #2a2a5a);
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 8px 20px rgba(0, 217, 255, 0.3);
  border: 1px solid rgba(0, 217, 255, 0.5);
  margin: 10px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 30px rgba(0, 217, 255, 0.5);
}

/* Dashboard Row */
.dashboard-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: space-around;
}

/* Neon Footer */
.neon-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background: linear-gradient(90deg, #0a0e27 0%, #1a1a2e 50%, #0a0e27 100%);
  color: #00ff88;
  text-align: center;
  padding: 15px;
  font-size: 1.2em;
  font-weight: 700;
  text-shadow: 0 0 10px #00ff88, 0 0 20px #00ff88;
  border-top: 2px solid #00ff88;
  z-index: 9999;
  animation: pulse 3s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

/* Sidebar */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
  border-right: 2px solid #00d9ff;
}

/* Buttons */
.stButton>button {
  background: linear-gradient(145deg, #00d9ff, #0077ff);
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  font-weight: 700;
  box-shadow: 0 4px 10px rgba(0, 217, 255, 0.5);
  transition: all 0.3s ease;
}

.stButton>button:hover {
  background: linear-gradient(145deg, #0077ff, #00d9ff);
  box-shadow: 0 6px 15px rgba(0, 217, 255, 0.7);
  transform: scale(1.05);
}

/* Streamlit native elements */
div[data-testid="stMetricValue"] {
  font-size: 2em;
  font-weight: 900;
  color: #00d9ff;
  text-shadow: 0 0 10px #00d9ff;
}

/* Plotly charts */
.js-plotly-plot {
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0, 217, 255, 0.3);
}
</style>
""", unsafe_allow_html=True)

# ============ Data Pipeline ============
# Check if CSV exists; if not, use sample data
csv_path = "echolon_ai_data.csv"

# Column mapping for flexibility
column_mapping = {
    "Date": ["Date", "date", "DATE", "Order Date", "Transaction Date"],
    "Product": ["Product", "product", "PRODUCT", "Item", "Product Name"],
    "Category": ["Category", "category", "CATEGORY", "Type"],
    "Revenue": ["Revenue", "revenue", "REVENUE", "Sales", "Amount"],
    "Units": ["Units", "units", "UNITS", "Quantity", "Qty"],
    "Region": ["Region", "region", "REGION", "Location", "Territory"]
}

def map_columns(df, mapping):
    """Map various column name variations to standard names"""
    for standard, variations in mapping.items():
        for col in df.columns:
            if col in variations:
                df = df.rename(columns={col: standard})
                break
    return df

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    df = map_columns(df, column_mapping)
else:
    # Sample data
    dates = pd.date_range(end=datetime.now(), periods=180, freq='D')
    products = ["Widget A", "Widget B", "Gadget X", "Tool Z", "Device Q"]
    categories = ["Electronics", "Hardware", "Software", "Accessories"]
    regions = ["North", "South", "East", "West"]
    
    df = pd.DataFrame({
        "Date": [dates[i % len(dates)] for i in range(500)],
        "Product": [products[i % len(products)] for i in range(500)],
        "Category": [categories[i % len(categories)] for i in range(500)],
        "Revenue": [round(1000 + (i * 137) % 5000, 2) for i in range(500)],
        "Units": [(10 + (i * 7) % 50) for i in range(500)],
        "Region": [regions[i % len(regions)] for i in range(500)]
    })

# Ensure Date is datetime
df['Date'] = pd.to_datetime(df['Date'])

# ============ Header ============
st.markdown('<div class="neon-header">🚀 Echolon AI Dashboard</div>', unsafe_allow_html=True)
st.markdown("---")

# ============ Sidebar ============
st.sidebar.title("🎛️ Filters & Options")

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['Date'].min().date(), df['Date'].max().date()),
    min_value=df['Date'].min().date(),
    max_value=df['Date'].max().date()
)

selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

selected_regions = st.sidebar.multiselect(
    "Select Regions",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

# Filter data
if len(date_range) == 2:
    start_date, end_date = date_range
    mask = (
        (df['Date'].dt.date >= start_date) &
        (df['Date'].dt.date <= end_date) &
        (df['Category'].isin(selected_categories)) &
        (df['Region'].isin(selected_regions))
    )
    sales = df[mask].copy()
else:
    sales = df.copy()

# ============ Main Dashboard ============
st.markdown('<div class="dashboard-row">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Revenue",
        value=f"${sales['Revenue'].sum():,.0f}",
        delta=f"{(sales['Revenue'].sum() / df['Revenue'].sum() * 100):.1f}% of total"
    )

with col2:
    st.metric(
        label="📦 Units Sold",
        value=f"{sales['Units'].sum():,}",
        delta=f"+{sales['Units'].sum() - sales['Units'].mean():.0f}"
    )

with col3:
    avg_order = sales['Revenue'].sum() / len(sales) if len(sales) > 0 else 0
    st.metric(
        label="📊 Avg Order Value",
        value=f"${avg_order:,.2f}",
        delta="+5.2%"
    )

with col4:
    st.metric(
        label="🌍 Active Regions",
        value=len(sales['Region'].unique()),
        delta=f"{len(sales['Region'].unique())} regions"
    )

st.markdown("---")

# ============ Charts Section ============
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📈 Revenue Over Time")
    revenue_time = sales.groupby(sales['Date'].dt.to_period('M'))['Revenue'].sum().reset_index()
    revenue_time['Date'] = revenue_time['Date'].dt.to_timestamp()
    fig_time = px.line(
        revenue_time,
        x='Date',
        y='Revenue',
        title="Monthly Revenue Trend",
        template="plotly_dark"
    )
    fig_time.update_traces(line_color='#00d9ff', line_width=3)
    st.plotly_chart(fig_time, use_container_width=True)

with col_chart2:
    st.subheader("🥧 Revenue by Category")
    category_revenue = sales.groupby('Category')['Revenue'].sum().reset_index()
    fig_pie = px.pie(
        category_revenue,
        names='Category',
        values='Revenue',
        title="Category Distribution",
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.ice
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    st.subheader("🌍 Revenue by Region")
    region_revenue = sales.groupby('Region')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False)
    fig_region = px.bar(
        region_revenue,
        x='Region',
        y='Revenue',
        title="Regional Performance",
        template="plotly_dark",
        color='Revenue',
        color_continuous_scale='Teal'
    )
    st.plotly_chart(fig_region, use_container_width=True)

with col_chart4:
    st.subheader("🏆 Top 5 Products")
    top_products = sales.groupby('Product')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False).head(5)
    fig_products = px.bar(
        top_products,
        x='Revenue',
        y='Product',
        orientation='h',
        title="Best Sellers",
        template="plotly_dark",
        color='Revenue',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_products, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============ Glowing Savings Footer ============
# Calculate savings amount AFTER all dashboard variables are defined
savings_amt = int(sales['Revenue'].sum() * 0.12)
footer_html = f"""<div class="neon-footer">✨ AI-Driven Savings<br>${savings_amt:,} savings projected from workflow & analytics automation</div>"""
st.markdown(footer_html, unsafe_allow_html=True)
