"""
Echolon AI Dashboard — Neon-Styled Analytics
Three-column layout: Sales & Behavior Predictive Analytics, Inventory Optimization, Workflow Efficiency
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# ============ NEON & OUTLINED CSS ============
st.markdown(
    '''<style>
    .stApp {background-color: #0a0a0a;}
    .neon-title {color:#00fff7;font-size:40px;font-weight:bolder;text-shadow:0 0 40px #00fff7,0 0 10px #00fff7;} 
    .neon-footer {background:rgba(40,20,40,0.88);border:3px solid #00fff7;border-radius:22px;padding:28px;text-align:center;box-shadow:0 0 50px #00fff7;}
    .dashboard-row {display:flex;gap:22px;margin-top:22px;}
    .neon-card {background:rgba(20,20,40,0.94);border:3px solid #00fff7;border-radius:17px;padding:22px;box-shadow:0 0 24px #00fff7;flex:1;min-width:320px;}
    .neon-card-pink {background:rgba(40,20,30,0.97);border:3px solid #ff0077;box-shadow:0 0 24px #ff0077;border-radius:17px;padding:22px;flex:1;min-width:320px;}
    .neon-card-green {background:rgba(20,40,30,0.97);border:3px solid #00ff99;box-shadow:0 0 24px #00ff99;border-radius:17px;padding:22px;flex:1;min-width:320px;}
    .neon-header, .neon-header-pink, .neon-header-green {font-size:25px;font-weight:800;margin-bottom:12px;}
    .neon-header {color:#00fff7;text-shadow:0 0 8px #00fff7;}
    .neon-header-pink {color:#ff0077;text-shadow:0 0 10px #ff0077;}
    .neon-header-green {color:#00ff99;text-shadow:0 0 10px #00ff99;}
    .metric-label {font-weight:bold;margin-top:10px;}
    .metric-value {font-size:36px;margin-bottom:5px;}
    </style>''', unsafe_allow_html=True)

# ============ CSV DATA PIPELINE ============
st.sidebar.header('CSV Data Pipeline Tester')
uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file to test the data pipeline:", type=["csv"], key="uploader")
run_pipeline = st.sidebar.button('Run Pipeline', key="run_csv_pipeline")
data_error = None
preview_data = None
user_data = None

def create_sample_data():
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    sales = {
        'Date': dates,
        'Revenue': np.random.uniform(800, 1500, 30).round(2),
        'Orders': np.random.randint(15, 50, 30),
        'Customers': np.random.randint(10, 40, 30)
    }
    inventory = {
        'Product': ['Widget A', 'Gadget B', 'Tool C', 'Device D', 'Item E'],
        'Stock': [85, 42, 150, 68, 23],
        'Reorder': [50, 30, 100, 40, 20],
        'Sales_30d': [125, 78, 90, 95, 112]
    }
    workflow = {
        'Date': dates[-7:],
        'Tasks': np.random.randint(20, 45, 7),
        'Completed': np.random.randint(15, 40, 7),
        'Efficiency': np.random.uniform(70, 95, 7).round(1)
    }
    return sales, inventory, workflow

if uploaded_file and run_pipeline:
    try:
        user_data = pd.read_csv(uploaded_file)
        preview_data = user_data.head()
    except Exception as e:
        data_error = f"Error reading CSV: {e}"
elif uploaded_file and not run_pipeline:
    try:
        preview_data = pd.read_csv(uploaded_file).head()
    except Exception as e:
        data_error = f"Error previewing CSV: {e}"

st.sidebar.markdown("### CSV Preview (First 5 rows):")
if preview_data is not None:
    st.sidebar.dataframe(preview_data, use_container_width=True)
if data_error:
    st.sidebar.error(data_error)

def get_dashboard_data():
    if user_data is not None:
        try:
            if set(['Date','Revenue','Orders','Customers']).issubset(user_data.columns):
                sales = user_data.copy()
                if not pd.api.types.is_datetime64_any_dtype(sales['Date']):
                    sales['Date'] = pd.to_datetime(sales['Date'])
                _, inventory, workflow = create_sample_data()
                return sales, inventory, workflow
            if set(['Product','Stock','Reorder','Sales_30d']).issubset(user_data.columns):
                inventory = user_data.copy()
                sales, _, workflow = create_sample_data()
                return sales, inventory, workflow
            if set(['Date','Tasks','Completed','Efficiency']).issubset(user_data.columns):
                workflow = user_data.copy()
                sales, inventory, _ = create_sample_data()
                return sales, inventory, workflow
            return create_sample_data()
        except Exception as e:
            st.warning(f"Pipeline error: {e}. Showing sample data instead.")
            return create_sample_data()
    else:
        return create_sample_data()

sales, inventory, workflow = get_dashboard_data()

# ============ MAIN DASHBOARD LAYOUT ============
st.markdown('<div class="neon-title">Echolon Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="dashboard-row">', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="neon-card">', unsafe_allow_html=True)
    st.markdown('<div class="neon-header">Sales & Behavior Predictive Analytics</div>', unsafe_allow_html=True)
    latest_sales = sales['Revenue'][-1]
    st.metric(label="Today’s Revenue", value=f"${latest_sales:,.2f}")
    st.metric(label="Orders", value=sales['Orders'][-1])
    st.metric(label="Customers", value=sales['Customers'][-1])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sales['Date'], y=sales['Revenue'], line_shape='spline', mode='lines', name="Revenue", line=dict(color="#00fff7", width=5)))
    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=25, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=230)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="neon-card-pink">', unsafe_allow_html=True)
    st.markdown('<div class="neon-header-pink">Inventory Optimization</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(inventory), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="neon-card-green">', unsafe_allow_html=True)
    st.markdown('<div class="neon-header-green">Workflow Efficiency</div>', unsafe_allow_html=True)
    st.metric(label="Efficiency Last 7 Days", value=f"{workflow['Efficiency'].mean():.1f}%")
    fig_wf = go.Figure()
    fig_wf.add_trace(go.Bar(x=workflow['Date'], y=workflow['Completed'], marker_color='#00ff99', name="Completed"))
    fig_wf.add_trace(go.Bar(x=workflow['Date'], y=workflow['Tasks'], marker_color='#ff0077', name="Tasks"))
    fig_wf.update_layout(barmode='group', showlegend=True, margin=dict(l=0, r=0, t=25, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=230)
    st.plotly_chart(fig_wf, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============ Glowing Savings Footer ============
savings_amt = int(sales['Revenue'].sum() * 0.12)
footer_html = f"""
<div class='neon-footer'>
    <span style='font-size:37px;font-weight:bold;color:#00fff7;'>AI-Driven Savings</span><br>
    <span style='font-size:23px;font-family:monospace;letter-spacing:2.5px;color:#fff;'>${savings_amt:,} savings projected from workflow & analytics automation</span>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
