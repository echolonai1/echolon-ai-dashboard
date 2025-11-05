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
st.set_page_config(page_title="Echolon AI Dashboard", layout="wide", initial_sidebar_state="collapsed")

# ===================== CUSTOM CSS =====================
st.markdown("""
<style>
    /* Dark background and neon theme */
    .stApp {
        background-color: #0a0a0a;
    }
    
    /* Neon card styling */
    .neon-card {
        background: rgba(20, 20, 40, 0.8);
        border: 2px solid #00ffff;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }
    
    .neon-card-pink {
        background: rgba(40, 20, 30, 0.8);
        border: 2px solid #ff0077;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 20px rgba(255, 0, 119, 0.3);
    }
    
    .neon-card-green {
        background: rgba(20, 40, 30, 0.8);
        border: 2px solid #00ff99;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 20px rgba(0, 255, 153, 0.3);
    }
    
    /* Neon text */
    .neon-header {
        color: #00ffff;
        font-size: 24px;
        font-weight: bold;
        text-shadow: 0 0 10px #00ffff;
        margin-bottom: 15px;
    }
    
    .neon-header-pink {
        color: #ff0077;
        font-size: 24px;
        font-weight: bold;
        text-shadow: 0 0 10px #ff0077;
        margin-bottom: 15px;
    }
    
    .neon-header-green {
        color: #00ff99;
        font-size: 24px;
        font-weight: bold;
        text-shadow: 0 0 10px #00ff99;
        margin-bottom: 15px;
    }
    
    .metric-value {
        font-size: 48px;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 14px;
        opacity: 0.8;
        margin-bottom: 5px;
    }
    
    .ai-badge {
        display: inline-block;
        background: rgba(0, 255, 255, 0.2);
        border: 1px solid #00ffff;
        border-radius: 20px;
        padding: 5px 15px;
        font-size: 12px;
        color: #00ffff;
        margin: 5px 0;
    }
    
    .alert-box {
        background: rgba(255, 0, 119, 0.1);
        border-left: 4px solid #ff0077;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }
    
    .checklist-item {
        padding: 8px;
        margin: 5px 0;
        border-left: 3px solid #00ff99;
        background: rgba(0, 255, 153, 0.1);
    }
    
    .footer-savings {
        background: linear-gradient(90deg, rgba(0,255,255,0.2), rgba(255,0,119,0.2), rgba(0,255,153,0.2));
        border: 3px solid #00ffff;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin-top: 30px;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
    }
    
    .savings-amount {
        font-size: 64px;
        font-weight: bold;
        background: linear-gradient(90deg, #00ffff, #ff0077, #00ff99);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0, 255, 255, 0.8);
    }
    
    h1 {
        color: #ffffff !important;
        text-align: center;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ===================== SAMPLE DATA =====================
# Sales trend data
dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
sales_data = pd.DataFrame({
    'Date': dates,
    'Sales': 5000 + np.cumsum(np.random.randn(30) * 200) + np.arange(30) * 100
})

# Inventory data
inventory_categories = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
inventory_current = [450, 320, 580, 290, 410]
inventory_optimal = [500, 400, 600, 350, 450]

# ===================== MAIN DASHBOARD =====================
st.title("🚀 Echolon AI Dashboard")

# Three-column layout
col1, col2, col3 = st.columns(3)

# ==================== COLUMN 1: SALES & BEHAVIOR ====================
with col1:
    st.markdown('<div class="neon-card">', unsafe_allow_html=True)
    st.markdown('<div class="neon-header">📊 Sales & Behavior Predictive Analytics</div>', unsafe_allow_html=True)
    
    # Sales trend chart
    fig_sales = go.Figure()
    fig_sales.add_trace(go.Scatter(
        x=sales_data['Date'],
        y=sales_data['Sales'],
        mode='lines',
        line=dict(color='#00ffff', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 255, 0.1)'
    ))
    fig_sales.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00ffff'),
        xaxis=dict(showgrid=True, gridcolor='rgba(0,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,255,255,0.1)'),
        height=250,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig_sales, use_container_width=True)
    
    # Metrics
    st.markdown('<div class="metric-label" style="color: #00ffff;">Churn Risk Score</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value" style="color: #00ffff;">12.3%</div>', unsafe_allow_html=True)
    st.markdown('<span class="ai-badge">🤖 AI Predicted</span>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-label" style="color: #00ffff; margin-top: 20px;">Active AI Users</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value" style="color: #00ffff;">2,847</div>', unsafe_allow_html=True)
    st.markdown('<span style="color: #00ff99; font-size: 14px;">↑ 18% from last month</span>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== COLUMN 2: INVENTORY OPTIMIZATION ====================
with col2:
    st.markdown('<div class="neon-card-pink">', unsafe_allow_html=True)
    st.markdown('<div class="neon-header-pink">📦 Inventory Optimization</div>', unsafe_allow_html=True)
    
    # Inventory bar chart
    fig_inventory = go.Figure()
    fig_inventory.add_trace(go.Bar(
        x=inventory_categories,
        y=inventory_current,
        name='Current Stock',
        marker=dict(color='#ff0077')
    ))
    fig_inventory.add_trace(go.Scatter(
        x=inventory_categories,
        y=inventory_optimal,
        name='Optimal Level',
        mode='lines+markers',
        line=dict(color='#00ff99', width=2, dash='dash')
    ))
    fig_inventory.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ff0077'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,0,119,0.1)'),
        height=250,
        margin=dict(l=0, r=0, t=20, b=0),
        showlegend=True,
        legend=dict(font=dict(size=10))
    )
    st.plotly_chart(fig_inventory, use_container_width=True)
    
    # AI Directive
    st.markdown('''
    <div class="ai-badge" style="width: 100%; text-align: center; background: rgba(255,0,119,0.2); border-color: #ff0077; color: #ff0077;">
        🤖 AI DIRECTIVE
    </div>
    <div style="color: #ffffff; margin: 10px 0; font-size: 14px;">
        Reorder Product D (+60 units) and Product B (+80 units) by Friday to avoid stockout.
    </div>
    ''', unsafe_allow_html=True)
    
    # Stockout alert
    st.markdown('''
    <div class="alert-box">
        <div style="color: #ff0077; font-weight: bold;">⚠️ STOCKOUT ALERT</div>
        <div style="color: #ffffff; font-size: 12px; margin-top: 5px;">
            Product D: Critical level (29% below optimal)
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== COLUMN 3: WORKFLOW EFFICIENCY ====================
with col3:
    st.markdown('<div class="neon-card-green">', unsafe_allow_html=True)
    st.markdown('<div class="neon-header-green">⚡ Workflow Efficiency</div>', unsafe_allow_html=True)
    
    # Donut chart for efficiency
    fig_donut = go.Figure(data=[go.Pie(
        labels=['Completed', 'In Progress', 'Pending'],
        values=[68, 22, 10],
        hole=0.6,
        marker=dict(colors=['#00ff99', '#00ffff', '#ff0077']),
        textfont=dict(color='#ffffff')
    )])
    fig_donut.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00ff99'),
        height=200,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(font=dict(size=10))
    )
    st.plotly_chart(fig_donut, use_container_width=True)
    
    st.markdown('<div class="metric-label" style="color: #00ff99;">Overall Efficiency</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value" style="color: #00ff99; font-size: 36px;">87.4%</div>', unsafe_allow_html=True)
    
    # AI Optimizing status
    st.markdown('''
    <div style="color: #00ff99; font-size: 14px; margin: 15px 0;">
        🤖 AI Optimizing Workflows...
    </div>
    ''', unsafe_allow_html=True)
    
    # Checklist
    st.markdown('<div style="font-weight: bold; color: #00ff99; margin-top: 15px;">Active Tasks</div>', unsafe_allow_html=True)
    st.markdown('''
    <div class="checklist-item">
        <div style="color: #ffffff; font-size: 13px;">✓ Automate inventory sync</div>
    </div>
    <div class="checklist-item">
        <div style="color: #ffffff; font-size: 13px;">✓ Update sales forecasts</div>
    </div>
    <div class="checklist-item">
        <div style="color: #ffffff; font-size: 13px;">⏳ Generate weekly reports</div>
    </div>
    <div class="checklist-item">
        <div style="color: #ffffff; font-size: 13px;">⏳ Optimize delivery routes</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== FOOTER: TOTAL SAVINGS ====================
st.markdown('''
<div class="footer-savings">
    <div style="color: #ffffff; font-size: 20px; margin-bottom: 10px;">
        💰 TOTAL AI-DRIVEN SAVINGS THIS QUARTER
    </div>
    <div class="savings-amount">
        $847,392
    </div>
    <div style="color: #00ffff; font-size: 16px; margin-top: 10px;">
        🚀 42% increase from Q3 | 🎯 Projected: $1.2M by year end
    </div>
</div>
''', unsafe_allow_html=True)
