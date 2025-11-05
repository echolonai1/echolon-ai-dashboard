"""
Echolon AI Dashboard — Neon-Styled Analytics
Three-column layout with Sales Analytics, Inventory Optimization, and Workflow Efficiency
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Echolon AI Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================== CUSTOM CSS =====================
st.markdown(
    """
    <style>
    /* Dark background and neon theme */
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
    """,
    unsafe_allow_html=True
)

# ===================== HELPER FUNCTIONS =====================
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
    
    return pd.DataFrame(sales), pd.DataFrame(inventory), pd.DataFrame(workflow)

# ===================== MAIN DASHBOARD =====================
st.markdown('<h1 style="text-align:center;color:#00ffff;text-shadow:0 0 15px #00ffff;">⚡ Echolon AI Dashboard ⚡</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#888;">Real-time Business Intelligence & Analytics</p>', unsafe_allow_html=True)

sales_df, inventory_df, workflow_df = create_sample_data()

# ===================== THREE-COLUMN LAYOUT =====================
col1, col2, col3 = st.columns(3, gap="medium")

# ─────────────── COLUMN 1: SALES ANALYTICS (CYAN) ───────────────
with col1:
    st.markdown('<div class="neon-card"><div class="neon-header">💰 Sales Analytics</div>', unsafe_allow_html=True)
    
    # Key Metrics
    total_revenue = sales_df['Revenue'].sum()
    total_orders = sales_df['Orders'].sum()
    avg_order_value = total_revenue / total_orders
    
    st.markdown(f'<div class="metric-label">Total Revenue (30d)</div><div class="metric-value" style="color:#00ffff;">${total_revenue:,.2f}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">Total Orders</div><div class="metric-value" style="color:#00ffff;">{total_orders}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">Avg Order Value</div><div class="metric-value" style="color:#00ffff;">${avg_order_value:,.2f}</div>', unsafe_allow_html=True)
    
    # Revenue Chart
    fig_sales = go.Figure()
    fig_sales.add_trace(go.Scatter(
        x=sales_df['Date'],
        y=sales_df['Revenue'],
        mode='lines+markers',
        line=dict(color='#00ffff', width=2),
        marker=dict(size=6, color='#00ffff'),
        fill='tozeroy',
        fillcolor='rgba(0,255,255,0.1)'
    ))
    fig_sales.update_layout(
        title='Daily Revenue Trend',
        xaxis_title='Date',
        yaxis_title='Revenue ($)',
        template='plotly_dark',
        height=250,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig_sales, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────── COLUMN 2: INVENTORY OPTIMIZATION (PINK) ───────────────
with col2:
    st.markdown('<div class="neon-card-pink"><div class="neon-header-pink">📦 Inventory Optimization</div>', unsafe_allow_html=True)
    
    # Inventory Alerts
    low_stock = inventory_df[inventory_df['Stock'] < inventory_df['Reorder']]
    st.markdown(f'<div class="metric-label">Low Stock Alerts</div><div class="metric-value" style="color:#ff0077;">{len(low_stock)}</div>', unsafe_allow_html=True)
    
    if len(low_stock) > 0:
        st.markdown('<p style="color:#ff0077;font-weight:bold;">⚠️ Reorder Required:</p>', unsafe_allow_html=True)
        for _, row in low_stock.iterrows():
            st.markdown(f'<p style="color:#ff8888;">• {row["Product"]}: {row["Stock"]} units (reorder at {row["Reorder"]})</p>', unsafe_allow_html=True)
    
    # Stock Levels Chart
    fig_inv = go.Figure()
    fig_inv.add_trace(go.Bar(
        x=inventory_df['Product'],
        y=inventory_df['Stock'],
        marker_color='#ff0077',
        name='Current Stock'
    ))
    fig_inv.add_trace(go.Scatter(
        x=inventory_df['Product'],
        y=inventory_df['Reorder'],
        mode='lines+markers',
        line=dict(color='#ffff00', width=2, dash='dash'),
        marker=dict(size=8, color='#ffff00'),
        name='Reorder Level'
    ))
    fig_inv.update_layout(
        title='Stock Levels vs Reorder Points',
        xaxis_title='Product',
        yaxis_title='Units',
        template='plotly_dark',
        height=250,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig_inv, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────── COLUMN 3: WORKFLOW EFFICIENCY (GREEN) ───────────────
with col3:
    st.markdown('<div class="neon-card-green"><div class="neon-header-green">⚙️ Workflow Efficiency</div>', unsafe_allow_html=True)
    
    # Workflow Metrics
    total_tasks = workflow_df['Tasks'].sum()
    completed_tasks = workflow_df['Completed'].sum()
    completion_rate = (completed_tasks / total_tasks) * 100
    avg_efficiency = workflow_df['Efficiency'].mean()
    
    st.markdown(f'<div class="metric-label">Tasks This Week</div><div class="metric-value" style="color:#00ff99;">{total_tasks}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">Completed</div><div class="metric-value" style="color:#00ff99;">{completed_tasks}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">Completion Rate</div><div class="metric-value" style="color:#00ff99;">{completion_rate:.1f}%</div>', unsafe_allow_html=True)
    
    # Efficiency Chart
    fig_workflow = go.Figure()
    fig_workflow.add_trace(go.Scatter(
        x=workflow_df['Date'],
        y=workflow_df['Efficiency'],
        mode='lines+markers',
        line=dict(color='#00ff99', width=3),
        marker=dict(size=8, color='#00ff99'),
        fill='tozeroy',
        fillcolor='rgba(0,255,153,0.1)'
    ))
    fig_workflow.update_layout(
        title='Weekly Efficiency Trend',
        xaxis_title='Date',
        yaxis_title='Efficiency (%)',
        template='plotly_dark',
        height=250,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig_workflow, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== FOOTER =====================
st.markdown('<hr style="border-color:#333;">', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#555;font-size:12px;">Powered by Echolon AI | Last Updated: ' + datetime.now().strftime('%Y-%m-%d %H:%M') + '</p>', unsafe_allow_html=True)
