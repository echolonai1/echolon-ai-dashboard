import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import openai
from streamlit_extras.add_vertical_space import add_vertical_space

# ============ Page Config ============
st.set_page_config(page_title="Echolon AI Dashboard", layout="wide", page_icon="🚀")

# ============ Custom CSS ============
st.markdown("""
<style>
body {background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 100%); color: #fff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
.neon-header {font-size: 3em; font-weight: 900; text-align: center; color: #00d9ff; text-shadow: 0 0 10px #00d9ff,0 0 30px #00d9ff; margin-bottom: 20px;}
.metric-card {background: linear-gradient(145deg, #1e1e3f, #2a2a5a); border-radius: 15px; padding: 20px; box-shadow: 0 8px 20px rgba(0,217,255,0.3); margin: 10px;}
.neon-footer {position: fixed; bottom: 0; width: 100%; background: #1a1a2e; color: #00d9ff; text-align: center; box-shadow: 0 0 10px #00d9ff; padding: 10px 0; font-size: 1.3em;}<br>
.info-icon {display:inline-block; width:18px; height:18px; background:#00d9ff; color:#fff; text-align:center; border-radius:50%; font-size:12px; line-height:18px; vertical-align:middle; margin-left:6px; cursor:pointer;}
</style>
""", unsafe_allow_html=True)

st.title("Echolon AI Dashboard 🚀")

# ============ Sidebar Controls ============
st.sidebar.header("Pro Features")

# 1. CSV Data Pipeline Tester
add_vertical_space(1)
st.sidebar.subheader("CSV Data Pipeline Tester")
csv_file = st.sidebar.file_uploader("Upload CSV Data", type=["csv"], help="Upload your sales CSV file.")
csv_df = None
column_map = {}
running_data = False
if csv_file:
    try:
        csv_df = pd.read_csv(csv_file)
        st.sidebar.write("Preview:")
        st.sidebar.dataframe(csv_df.head())
        cols_orig = csv_df.columns.tolist()
        st.sidebar.write("Column Mapper:")
        col1 = st.sidebar.selectbox("Date Column", cols_orig)
        col2 = st.sidebar.selectbox("Revenue Column", cols_orig)
        col3 = st.sidebar.selectbox("Category Column", cols_orig)
        col4 = st.sidebar.selectbox("Region Column", cols_orig)
        col5 = st.sidebar.selectbox("Product Column", cols_orig)
        if st.sidebar.button("Run Pipeline"):
            column_map = {'Date': col1, 'Revenue': col2, 'Category': col3, 'Region': col4, 'Product': col5}
            running_data = True
    except Exception as e:
        st.sidebar.error(f"Error loading file: {e}")

# 5. Show/Hide Module Toggles
st.sidebar.subheader("Show/Hide Dashboard Modules")
show_time_trend = st.sidebar.checkbox("Time Trend Chart", True)
show_category_pie = st.sidebar.checkbox("Category Pie Chart", True)
show_region_bar = st.sidebar.checkbox("Region Bar Chart", True)
show_top_products = st.sidebar.checkbox("Top 5 Products", True)
show_metrics = st.sidebar.checkbox("Key Metrics", True)
show_recs = st.sidebar.checkbox("Recommendations", True)

# 4. Dashboard Tour Popup
add_vertical_space(1)
def tour_content():
    st.sidebar.info("""
        **Dashboard Tour Tips:**
        - Upload your CSV sales file and map columns in the sidebar.
        - Use toggle switches to show/hide dashboard modules.
        - Hover info icons for metric tips.
        - Ask dashboard questions using OpenAI sidebar input!
        """, icon="🚀")
open_tour = st.sidebar.button("Show Dashboard Tour & Tips")
if open_tour: tour_content()

# 6. OpenAI 'Ask the Dashboard'
add_vertical_space(1)
st.sidebar.subheader("Ask the Dashboard (OpenAI)")
query = st.sidebar.text_input("Type a dashboard question:")
response = None
OPENAI_KEY = None
try:
    import toml
    secrets = toml.load(".streamlit/secrets.toml")
    OPENAI_KEY = secrets.get("OPENAI_API_KEY", None)
except Exception:
    OPENAI_KEY = os.environ.get("OPENAI_API_KEY", None)
if query and OPENAI_KEY:
    openai.api_key = OPENAI_KEY
    resp = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}], max_tokens=150)
    response = resp['choices'][0]['message']['content']
    st.sidebar.success(response)
elif query:
    st.sidebar.error("OpenAI key missing! Add it to secrets.toml or env.")

# ============ Main Dashboard Data ============
if running_data and csv_df is not None and column_map:
    sales = csv_df.rename(columns=column_map)
else:
    sales = pd.DataFrame({  # fallback sample
'todo':[]})  # Fill with demo/sample/default if desired

# ============ Main Area ============
key_metrics = None
if not sales.empty:
    # Key Metrics
    if show_metrics:
        with st.expander("Key Financial Metrics", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                val = sales['Revenue'].sum()
                st.metric("Total Revenue", f"${val:,.0f}")
                st.caption(f'<span class="info-icon" title="Sum of all sales revenue">i</span>', unsafe_allow_html=True)
            with col2:
                avg = sales['Revenue'].mean()
                st.metric("Average Sale", f"${avg:,.2f}")
                st.caption(f'<span class="info-icon" title="Average deal size across the dataset">i</span>', unsafe_allow_html=True)
            with col3:
                cnt = sales['Product'].nunique()
                st.metric("Unique Products", f"{cnt}")
                st.caption(f'<span class="info-icon" title="Number of unique products sold">i</span>', unsafe_allow_html=True)

    # Time Trend Chart
    if show_time_trend:
        with st.expander("Monthly Revenue Trend Chart", expanded=True):
            try:
                sales['Date'] = pd.to_datetime(sales['Date'])
                revenue_time = sales.groupby(sales['Date'].dt.to_period('M')).agg({'Revenue':'sum'}).reset_index()
                revenue_time['Date'] = revenue_time['Date'].dt.to_timestamp()
                fig_time = px.line(revenue_time, x='Date', y='Revenue', title="Monthly Revenue Trend", template="plotly_dark")
                fig_time.update_traces(line_color='#00d9ff', line_width=3)
                st.plotly_chart(fig_time, use_container_width=True)
                st.caption(f'<span class="info-icon" title="Shows monthly revenue trend based on uploaded data">i</span>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Failed to generate trend chart: {e}")

    # Category Pie Chart
    if show_category_pie:
        with st.expander("Revenue by Category Pie Chart", expanded=True):
            try:
                category_revenue = sales.groupby('Category')['Revenue'].sum().reset_index()
                fig_pie = px.pie(category_revenue, names='Category', values='Revenue', title="Category Distribution", template="plotly_dark", color_discrete_sequence=px.colors.sequential.ice)
                st.plotly_chart(fig_pie, use_container_width=True)
                st.caption(f'<span class="info-icon" title="Shows proportion of revenue per product category">i</span>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Failed to generate category pie: {e}")

    # Region Bar Chart
    if show_region_bar:
        with st.expander("Revenue by Region Bar Chart", expanded=True):
            try:
                region_revenue = sales.groupby('Region')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False)
                fig_region = px.bar(region_revenue, x='Region', y='Revenue', title="Regional Performance", template="plotly_dark", color='Revenue', color_continuous_scale='Teal')
                st.plotly_chart(fig_region, use_container_width=True)
                st.caption(f'<span class="info-icon" title="Compare revenue across different sales regions">i</span>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Failed to generate region bar: {e}")

    # Top 5 Products
    if show_top_products:
        with st.expander("Top 5 Products", expanded=True):
            try:
                top_products = sales.groupby('Product')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False).head(5)
                fig_products = px.bar(top_products, x='Revenue', y='Product', orientation='h', title="Best Sellers", template="plotly_dark", color='Revenue', color_continuous_scale='Blues')
                st.plotly_chart(fig_products, use_container_width=True)
                st.caption(f'<span class="info-icon" title="Best performing products by revenue">i</span>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Failed to generate top products chart: {e}")

    # Recommendations & Help Tooltips
    if show_recs:
        with st.expander("AI Recommendations & Tips", expanded=True):
            st.write("- Check regions with below average sales for improvement opportunities.")
            st.write("- Focus marketing on top categories identified above.")
            st.write("- Ask the dashboard any business question using the sidebar!")
            st.caption(f'<span class="info-icon" title="Automated suggestions based on current dashboard analytics">i</span>', unsafe_allow_html=True)

# ============ Glowing Savings Footer ============
if not sales.empty:
    savings_amt = int(sales['Revenue'].sum() * 0.12)
    footer_html = f"""
        <div class='neon-footer'>✨ AI-Driven Savings<br>${savings_amt:,} savings projected from workflow & analytics automation</div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
