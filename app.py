import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# ============ Page Config ============
st.set_page_config(page_title="Echolon AI Dashboard", layout="wide", page_icon="🚀")

# ============ Custom CSS ============
st.markdown("""
<style>
body {background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 100%); color: #fff; font-family: 'Segoe UI', Tahoma, sans-serif;}
.neon-header {font-size: 3em; font-weight: 900; text-align: center; color: #00d9ff; text-shadow: 0 0 10px #00d9ff, 0 0 20px #00d9ff;}
.metric-card {background: linear-gradient(145deg, #1e1e3f, #2a2a5a); border-radius: 15px; padding: 20px; box-shadow: 0 0 20px rgba(0, 217, 255, 0.3); border: 2px solid #00d9ff; margin-bottom: 20px;}
.neon-footer {position: fixed; bottom: 0; width: 100%; background: #1a1a2e; color: #00d9ff; text-align: center; padding: 15px; font-size: 1.5em; box-shadow: 0 0 20px rgba(0,255,153,0.5); border-top: 3px solid #00ff99;}
.info-icon {display:inline-block; width:18px; height:18px; background:#00d9ff; color:#fff; text-align:center; border-radius:50%;}
.ai-box {background: rgba(255,0,119,0.1); border: 2px solid #ff0077; border-radius: 10px; padding: 15px; margin: 10px 0;}
.inv-box {background: rgba(0,255,153,0.1); border: 2px solid #00ff99; border-radius: 10px; padding: 15px; margin: 10px 0;}
.wf-box {background: rgba(0,217,255,0.1); border: 2px solid #00d9ff; border-radius: 10px; padding: 15px; margin: 10px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='neon-header'>🚀 Echolon AI Dashboard</h1>", unsafe_allow_html=True)

# ============ Sidebar Controls ============
st.sidebar.header("Pro Features")

# 1. CSV Data Pipeline Tester
st.sidebar.subheader("CSV Data Pipeline Tester")
csv_file = st.sidebar.file_uploader("Upload CSV Data", type=["csv"], help="Upload your sales CSV file.")
csv_df = None
if csv_file is not None:
    csv_df = pd.read_csv(csv_file)
    st.sidebar.success("CSV uploaded!")
    st.sidebar.dataframe(csv_df.head())

# 2. Module Toggles
st.sidebar.subheader("Toggle Modules")
show_sales = st.sidebar.checkbox("Show Sales & Behavior", value=True)
show_inventory = st.sidebar.checkbox("Show Inventory Optimization", value=True)
show_workflow = st.sidebar.checkbox("Show Workflow Efficiency", value=True)

# 3. Dashboard Tour
if st.sidebar.button("Show Dashboard Tour & Tips"):
    st.sidebar.info("""\n    **Dashboard Features:**\n    - Upload CSV for dynamic data\n    - Toggle modules on/off\n    - AI insights in each section\n    - Glowing savings footer\n    """)

# 4. Ask the Dashboard (OpenAI)
st.sidebar.subheader("Ask the Dashboard")
user_question = st.sidebar.text_input("Ask a business question...")
if user_question:
    st.sidebar.write("💡 AI Response: Your question has been received. Connect OpenAI API for live answers.")

# ============ Sample/Demo Data ============
def create_sample_data():
    dates = pd.date_range(end=datetime.now(), periods=180, freq='D')
    sales = pd.DataFrame({
        'Date': dates,
        'Revenue': np.random.randint(8000, 12000, 180),
        'Orders': np.random.randint(80, 120, 180)
    })
    inventory = pd.DataFrame({
        'SKU': ['Item A', 'Item B', 'Item C', 'Item D', 'Item E'],
        'Stock': [450, 230, 89, 567, 12],
        'Status': ['Healthy', 'Low', 'Critical', 'Healthy', 'Stockout']
    })
    workflow = pd.DataFrame({
        'Task': ['Data Processing', 'Reporting', 'Customer Outreach', 'Inventory Sync'],
        'Time_Saved_Hours': [45, 32, 28, 19]
    })
    return sales, inventory, workflow

sales_df, inventory_df, workflow_df = create_sample_data()

# Use CSV if uploaded and has expected columns
if csv_df is not None:
    if 'Date' in csv_df.columns and 'Revenue' in csv_df.columns:
        sales_df = csv_df

# ============ Three-Column Neon Grid Layout ============
col1, col2, col3 = st.columns(3)

# ----------- COLUMN 1: Sales & Behavior Predictive Analytics -----------
if show_sales:
    with col1:
        st.markdown("<div class='metric-card'><h2 style='color:#ff0077;'>📊 Sales & Behavior Predictive Analytics</h2></div>", unsafe_allow_html=True)
        
        # Chart
        fig1 = go.Figure()
        monthly = sales_df.groupby(pd.Grouper(key='Date', freq='M'))['Revenue'].sum().reset_index()
        fig1.add_trace(go.Scatter(x=monthly['Date'], y=monthly['Revenue'], mode='lines+markers', 
                                  line=dict(color='#ff0077', width=3), marker=dict(size=8)))
        fig1.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           title="Monthly Revenue Trend", height=250)
        st.plotly_chart(fig1, use_container_width=True)
        
        # AI Directives
        st.markdown("<div class='ai-box'><b>🤖 AI Directive:</b> Increase up-sell campaigns for high-value customers in Q4. Predicted +18% conversion.</div>", unsafe_allow_html=True)
        st.markdown("<div class='ai-box'><b>⚠️ Churn Alert:</b> 3 customers at high risk. Immediate outreach recommended to retain $45K ARR.</div>", unsafe_allow_html=True)
        
        # Metrics
        total_revenue = sales_df['Revenue'].sum()
        churn_risk_score = 67
        active_users = 1847
        st.metric("Total Revenue (180d)", f"${total_revenue:,}")
        st.metric("Churn Risk Score", f"{churn_risk_score}%", delta="-5%")
        st.metric("Active Users", f"{active_users:,}")

# ----------- COLUMN 2: Inventory Optimization -----------
if show_inventory:
    with col2:
        st.markdown("<div class='metric-card'><h2 style='color:#00ff99;'>📦 Inventory Optimization</h2></div>", unsafe_allow_html=True)
        
        # Chart
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=inventory_df['SKU'], y=inventory_df['Stock'], marker=dict(color='#00ff99')))
        fig2.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                           title="Current Stock Levels", height=250)
        st.plotly_chart(fig2, use_container_width=True)
        
        # AI Insights
        st.markdown("<div class='inv-box'><b>✓ Optimization Tip:</b> Item E will stockout in 3 days. Auto-reorder triggered for 500 units.</div>", unsafe_allow_html=True)
        st.markdown("<div class='inv-box'><b>💡 AI Insight:</b> Item A is overstocked by 22%. Suggest promotional discount to clear inventory.</div>", unsafe_allow_html=True)
        
        # Inventory Table
        st.dataframe(inventory_df, use_container_width=True)

# ----------- COLUMN 3: Workflow Efficiency -----------
if show_workflow:
    with col3:
        st.markdown("<div class='metric-card'><h2 style='color:#00d9ff;'>⚡ Workflow Efficiency</h2></div>", unsafe_allow_html=True)
        
        # Chart
        fig3 = go.Figure()
        fig3.add_trace(go.Pie(labels=workflow_df['Task'], values=workflow_df['Time_Saved_Hours'], 
                              marker=dict(colors=['#00d9ff', '#ff0077', '#00ff99', '#ffaa00'])))
        fig3.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', height=250, showlegend=True)
        st.plotly_chart(fig3, use_container_width=True)
        
        # AI Recommendations
        st.markdown("<div class='wf-box'><b>📋 Active Tasks:</b> AI suggests automating 'Customer Outreach' next. Est. 40hrs/month saved.</div>", unsafe_allow_html=True)
        st.markdown("<div class='wf-box'><b>⚡ Optimization:</b> Workflow efficiency up 34% this month. Reallocate resources to high-priority tasks.</div>", unsafe_allow_html=True)
        
        # Metrics
        total_time_saved = workflow_df['Time_Saved_Hours'].sum()
        efficiency_pct = 87
        st.metric("Total Time Saved (hrs)", f"{total_time_saved}")
        st.metric("Overall Efficiency", f"{efficiency_pct}%", delta="+12%")

# ============ Glowing Savings Footer ============
savings_amt = 205890
footer_html = f"""
<div class='neon-footer'>
    ✨ <b>AI-Driven Savings:</b> ${savings_amt:,} projected from workflow & analytics automation
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
