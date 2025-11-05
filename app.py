"""
Echolon AI Dashboard — Neon-Styled Analytics
Three-column layout with Sales Analytics, Inventory Optimization, Workflow Efficiency, and Shopify Data
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import requests
import os

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
    .neon-card-shopify {background: rgba(20,20,60,0.9);border:2px solid #95BF47;border-radius:15px;padding:20px;margin:10px 0;box-shadow:0 0 20px rgba(149,191,71,0.3);}
    .neon-header {color:#00ffff;font-size:24px;font-weight:bold;text-shadow:0 0 10px #00ffff;margin-bottom:15px;}
    .neon-header-pink {color:#ff0077;font-size:24px;font-weight:bold;text-shadow:0 0 10px #ff0077;margin-bottom:15px;}
    .neon-header-green {color:#00ff99;font-size:24px;font-weight:bold;text-shadow:0 0 10px #00ff99;margin-bottom:15px;}
    .neon-header-shopify {color:#95BF47;font-size:24px;font-weight:bold;text-shadow:0 0 10px #95BF47;margin-bottom:15px;}
    .metric-label {font-weight:bold;margin-top:10px;}
    .metric-value {font-size:36px;margin-bottom:10px;}
    </style>
    """,
    unsafe_allow_html=True
)

# ===================== SHOPIFY MODULE =====================
SHOP_URL = st.secrets["SHOP_URL"] if "SHOP_URL" in st.secrets else os.getenv("SHOP_URL", "yourshop.myshopify.com")
ACCESS_TOKEN = st.secrets["SHOPIFY_ACCESS_TOKEN"] if "SHOPIFY_ACCESS_TOKEN" in st.secrets else os.getenv("SHOPIFY_ACCESS_TOKEN", "")

def get_shopify_orders(access_token, shop_url, days=180):
    """Fetch last X days order history from Shopify REST API"""
    headers = {"X-Shopify-Access-Token": access_token, 'Content-Type': 'application/json'}
    since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%S')
    url = f"https://{shop_url}/admin/api/2023-10/orders.json?status=any&created_at_min={since_date}&limit=250"
    orders = []
    try:
        with st.spinner("Loading Shopify orders..."):
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                orders = data.get("orders", [])
            else:
                st.error(f"Shopify Orders API Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Order fetch error: {e}")
    return orders

def get_shopify_inventory(access_token, shop_url):
    """Fetch current inventory levels from Shopify REST API"""
    headers = {"X-Shopify-Access-Token": access_token, 'Content-Type': 'application/json'}
    inventory_levels = []
    url = f"https://{shop_url}/admin/api/2023-10/inventory_levels.json?limit=250"
    try:
        with st.spinner("Loading inventory levels..."):
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                inventory_levels = data.get("inventory_levels", [])
            else:
                st.error(f"Shopify Inventory API Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Inventory fetch error: {e}")
    return inventory_levels

# =========== THREE COLUMN DASHBOARD ===========
col1, col2, col3 = st.columns(3)

# Sales & Behavior Analytics Column (Left)
with col1:
    st.markdown('<div class="neon-header">📊 Sales & Behavior Analytics</div>', unsafe_allow_html=True)
    # Example sales metric
    st.markdown('<div class="metric-label" style="color:#00ffff;">Total Sales (Q4)</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value" style="color:#00ffff;">$148,297</div>', unsafe_allow_html=True)
    # Example sales chart
    sales_data = pd.DataFrame({
        'month': ['Jul','Aug','Sep','Oct','Nov'],
        'sales': [29122, 32010, 37788, 40182, 49195]
    })
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sales_data['month'], y=sales_data['sales'], mode='lines+markers', line_color='#00ffff'))
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#00ffff'))
    st.plotly_chart(fig, use_container_width=True)

# Inventory Optimization Column (Middle)
with col2:
    st.markdown('<div class="neon-header-pink">📦 Inventory Optimization</div>', unsafe_allow_html=True)
    # Example inventory metric
    st.markdown('<div class="metric-label" style="color:#ff0077;">Current Stock</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value" style="color:#ff0077;">21,404 units</div>', unsafe_allow_html=True)
    # Example stock trend
    inventory_data = pd.DataFrame({
        'date': pd.date_range(end=datetime.today(), periods=5).strftime('%b %d'),
        'stock': [21240, 22000, 24950, 24110, 21404]
    })
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=inventory_data['date'], y=inventory_data['stock'], marker_color='#ff0077'))
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#ff0077'))
    st.plotly_chart(fig2, use_container_width=True)

# Workflow Efficiency Column (Right)
with col3:
    st.markdown('<div class="neon-header-green">⚡ Workflow Efficiency</div>', unsafe_allow_html=True)
    fig3 = go.Figure(data=[go.Pie(labels=['Completed','In Progress','Pending'],values=[68,22,10], hole=0.6, marker=dict(colors=['#00ff99','#00ffff','#ff0077']), textfont=dict(color='#ffffff'))])
    fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#00ff99'), height=200, margin=dict(l=0,r=0,t=0,b=0), showlegend=True, legend=dict(font=dict(size=10)))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('<div class="metric-label" style="color:#00ff99;">Overall Efficiency</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value" style="color:#00ff99;">87.4%</div>', unsafe_allow_html=True)
    st.markdown('''<div style="color:#00ff99;font-size:14px;margin:15px 0;">🤖 AI Optimizing Workflows...</div>''', unsafe_allow_html=True)

# =========== SHOPIFY DATA MODULE ===========
st.markdown('<div class="neon-header-shopify">🛒 Shopify Data</div>', unsafe_allow_html=True)
if ACCESS_TOKEN:
    shopify_tab1, shopify_tab2 = st.tabs(["Orders (Last 180 Days)", "Current Inventory"])
    with shopify_tab1:
        orders = get_shopify_orders(ACCESS_TOKEN, SHOP_URL)
        if orders:
            df_orders = pd.DataFrame([
                {
                    'Order #': o.get('order_number'),
                    'Date': o.get('created_at', '')[:10],
                    'Total': o.get('total_price'),
                    'Status': o.get('financial_status')
                } for o in orders
            ])
            order_count = len(df_orders)
            st.metric("Total Orders", order_count)
            df_orders['Date'] = pd.to_datetime(df_orders['Date'])
            orders_monthly = df_orders.groupby(df_orders['Date'].dt.strftime('%b %Y')).size()
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=list(orders_monthly.index),
                y=orders_monthly.values,
                marker_color='#95BF47'
            ))
            fig.update_layout(title="Order Trends (Monthly)", plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#95BF47'))
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df_orders.head(10), use_container_width=True)
        else:
            st.info("No orders found.")
    with shopify_tab2:
        inventory = get_shopify_inventory(ACCESS_TOKEN, SHOP_URL)
        if inventory:
            df_inv = pd.DataFrame(inventory)
            st.metric("Inventory Record Count", len(df_inv))
            st.dataframe(df_inv.head(10), use_container_width=True)
        else:
            st.info("No inventory records found.")
else:
    st.warning("Shopify ACCESS_TOKEN not set. Please configure your API token.")

# =========== FOOTER: TOTAL SAVINGS ===========
st.markdown('''<div class="footer-savings">
    <div style="color:#ffffff;font-size:20px;margin-bottom:10px;">💰 TOTAL AI-DRIVEN SAVINGS THIS QUARTER</div>
    <div class="savings-amount">$847,392</div>
    <div style="color:#00ffff;font-size:16px;margin-top:10px;">🚀 42% increase from Q3 | 🎯 Projected: $1.2M by year end</div>
</div>''', unsafe_allow_html=True)
