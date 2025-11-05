"""
Echolon AI Dashboard — Neon-Styled Analytics
Three-column layout with Sales Analytics, Inventory Optimization, and Workflow Efficiency
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# ================= CSV PIPELINE UPLOADER ==================
st.sidebar.header('CSV Data Pipeline Tester')
uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file to test the data pipeline:",
    type=["csv"],
    key="uploader"
)
run_pipeline = st.sidebar.button('Run Pipeline', key="run_csv_pipeline")

data_error = None
preview_data = None
user_data = None

def create_sample_data():
    """Generate sample data for each module"""
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    # Sales data
    sales = {
        'Date': dates,
        'Revenue': np.random.uniform(800, 1500, 30).round(2),
        'Orders': np.random.randint(15, 50, 30),
        'Customers': np.random.randint(10, 40, 30)
    }
    # Inventory data
    inventory = {
        'Product': ['Widget A', 'Gadget B', 'Tool C', 'Device D', 'Item E'],
        'Stock': [85, 42, 150, 68, 23],
        'Reorder': [50, 30, 100, 40, 20],
        'Sales_30d': [125, 78, 90, 95, 112]
    }
    # Workflow data
    workflow = {
        'Date': dates[-7:],
        'Tasks': np.random.randint(20, 45, 7),
        'Completed': np.random.randint(15, 40, 7),
        'Efficiency': np.random.uniform(70, 95, 7).round(1)
    }
    return sales, inventory, workflow

# --- Load user-uploaded CSV if available ---
if uploaded_file and run_pipeline:
    try:
        user_data = pd.read_csv(uploaded_file)
        preview_data = user_data.head()
    except Exception as e:
        data_error = f"Error reading CSV: {e}"
elif uploaded_file and not run_pipeline:
    # Just show preview, wait for Run
    try:
        preview_data = pd.read_csv(uploaded_file).head()
    except Exception as e:
        data_error = f"Error previewing CSV: {e}"

# ========== Main Dashboard Data Source Selection ==========
def get_dashboard_data():
    if user_data is not None:
        # This is a simplistic stub, assuming uploaded CSV is like sales data
        # For a production dashboard, detect table type
        try:
            if set(['Date','Revenue','Orders','Customers']).issubset(user_data.columns):
                sales = user_data.copy()
                if pd.api.types.is_datetime64_any_dtype(sales['Date'])==False:
                    sales['Date'] = pd.to_datetime(sales['Date'])
                # Use demo data for inventory and workflow
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
            # If unknown schema, just return sample
            return create_sample_data()
        except Exception as e:
            st.warning(f"Pipeline error: {e}. Showing sample data instead.")
            return create_sample_data()
    else:
        return create_sample_data()

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Echolon AI Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# ===================== CUSTOM CSS =====================
st.markdown(
    '''
    <style>
    .stApp {background-color: #0a0a0a;}
    .neon-card {background: rgba(20,20,40,0.8);border:2px solid #00ffff;border-radius:15px;padding:20px;margin:10px 0;box-shadow:0 0 20px rgba(0,255,255,0.3);}
    .neon-card-pink {background: rgba(40,20,30,0.8);border:2px solid #ff0077;border-radius:15px;padding:20px;margin:10px 0;box-shadow:0 0 20px rgba(255,0,119,0.3);}
    .neon-card-green {background: rgba(20,40,30,0.8);border:2px solid #00ff99;border-radius:15px;padding:20px;margin:10px 0;box-shadow:0 0 20px rgba(0,255,153,0.3);}
    .neon-header {color:#00ffff;font-size:24px;font-weight:bold;text-shadow:0 0 10px #00ffff;margin-bottom:15px;}
    .neon-header-pink {color:#ff0077;font-size:24px;font-weight:bold;text-shadow:0 0 10px #ff0077;margin-bottom:15px;}
    .neon-header-green {color:#00ff99;font-size:24px;font-weight:bold;text-shadow:0 0 10px #00ff99;margin-bottom:15px;}
    .metric-label {font-weight:bold;margin-top:10px;}
    .metric-value {font-size:36px;margin-bottom:10px;}
    </style>
    ''', unsafe_allow_html=True)

# ============ CSV PREVIEW/ERROR ============
if uploaded_file:
    st.sidebar.markdown("### CSV Preview (First 5 rows):")
    if preview_data is not None:
        st.sidebar.dataframe(preview_data, use_container_width=True)
    if data_error:
        st.sidebar.error(data_error)
# ============ DASHBOARD MAIN ===============
sales, inventory, workflow = get_dashboard_data()
# ... (the rest of your original dashboard code follows, from where layout/metrics/charts etc. start)
