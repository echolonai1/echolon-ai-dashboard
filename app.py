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

# ===================== MAIN APP =====================
st.markdown('<h1 style="color:#00ffff;text-align:center;text-shadow:0 0 15px #00ffff;">🚀 ECHOLON AI DASHBOARD</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#aaa;">Real-Time Analytics | Powered by AI</p>', unsafe_allow_html=True)

df_sales, df_inventory, df_workflow = create_sample_data()

# Three-column layout
col1, col2, col3 = st.columns(3)

# =================== COLUMN 1: SALES & BEHAVIOR ANALYTICS ===================
with col1:
    st.markdown('<div class="neon-card"><div class="neon-header">📊 SALES & BEHAVIOR ANALYTICS</div>', unsafe_allow_html=True)
    
    # Metrics
    revenue = df_sales['Revenue'].sum()
    orders = df_sales['Orders'].sum()
    customers = df_sales['Customers'].sum()
    
    st.metric(label="💰 Total Revenue (30d)", value=f"${revenue:,.0f}")
    st.metric(label="📦 Total Orders", value=f"{orders}")
    st.metric(label="👥 Unique Customers", value=f"{customers}")
    
    # Revenue trend chart
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df_sales['Date'],
        y=df_sales['Revenue'],
        mode='lines+markers',
        line=dict(color='#00ffff', width=3),
        marker=dict(size=6, color='#00ffff')
    ))
    fig1.update_layout(
        title='Revenue Trend (30 Days)',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(20,20,40,0.5)',
        font=dict(color='#00ffff'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,255,255,0.2)')
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # AI Insight
    st.markdown('<p style="color:#00ffff;font-weight:bold;margin-top:20px;">🤖 AI Insight:</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#aaa;font-size:14px;">Peak sales occur on weekends. Consider targeted promotions Thursday-Friday to boost conversions by 15%.</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# =================== COLUMN 2: INVENTORY OPTIMIZATION ===================
with col2:
    st.markdown('<div class="neon-card-pink"><div class="neon-header-pink">📦 INVENTORY OPTIMIZATION</div>', unsafe_allow_html=True)
    
    # Top metric
    low_stock_count = (df_inventory['Stock'] < df_inventory['Reorder']).sum()
    st.metric(label="⚠️ Low Stock Items", value=f"{low_stock_count}")
    
    # Inventory bar chart
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=df_inventory['Product'],
        y=df_inventory['Stock'],
        marker=dict(color='#ff0077'),
        name='Current Stock'
    ))
    fig2.add_trace(go.Bar(
        x=df_inventory['Product'],
        y=df_inventory['Reorder'],
        marker=dict(color='#ffaa00'),
        name='Reorder Level'
    ))
    fig2.update_layout(
        title='Stock Levels vs Reorder Points',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(40,20,30,0.5)',
        font=dict(color='#ff0077'),
        barmode='group',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,0,119,0.2)')
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # AI Directive
    st.markdown('<p style="color:#ff0077;font-weight:bold;margin-top:20px;">🎯 AI Directive:</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#aaa;font-size:14px;">Reorder Product D (+60 units) and Product B (+80 units) by Friday. Projected stockout risk: 85%.</p>', unsafe_allow_html=True)
    
    # Alert box
    st.markdown('<div style="background:rgba(255,0,119,0.2);border:1px solid #ff0077;border-radius:8px;padding:10px;margin-top:15px;"><p style="color:#ff0077;font-size:13px;margin:0;">🚨 <strong>ALERT:</strong> Item E critical stock level (23 units). Auto-reorder triggered.</p></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# =================== COLUMN 3: WORKFLOW EFFICIENCY ===================
with col3:
    st.markdown('<div class="neon-card-green"><div class="neon-header-green">⚙️ WORKFLOW EFFICIENCY</div>', unsafe_allow_html=True)
    
    # Metrics
    avg_efficiency = df_workflow['Efficiency'].mean()
    total_tasks = df_workflow['Tasks'].sum()
    completed_tasks = df_workflow['Completed'].sum()
    
    st.metric(label="📈 Avg Efficiency (7d)", value=f"{avg_efficiency:.1f}%")
    st.metric(label="✅ Tasks Completed", value=f"{completed_tasks}/{total_tasks}")
    
    # Donut chart for task completion
    fig3 = go.Figure(data=[go.Pie(
        labels=['Completed', 'Pending'],
        values=[completed_tasks, total_tasks - completed_tasks],
        hole=0.5,
        marker=dict(colors=['#00ff99', '#333333'])
    )])
    fig3.update_layout(
        title='Task Completion Rate',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00ff99'),
        showlegend=True
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    # Efficiency trend
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=df_workflow['Date'],
        y=df_workflow['Efficiency'],
        mode='lines+markers',
        line=dict(color='#00ff99', width=3),
        marker=dict(size=8, color='#00ff99'),
        fill='tozeroy',
        fillcolor='rgba(0,255,153,0.2)'
    ))
    fig4.update_layout(
        title='Efficiency Trend (7 Days)',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(20,40,30,0.5)',
        font=dict(color='#00ff99'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,255,153,0.2)')
    )
    st.plotly_chart(fig4, use_container_width=True)
    
    # AI Recommendation
    st.markdown('<p style="color:#00ff99;font-weight:bold;margin-top:20px;">💡 AI Recommendation:</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#aaa;font-size:14px;">Automate recurring tasks on Mondays to improve efficiency by 12%. Implement batch processing for orders.</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# =================== FOOTER WITH TOTAL SAVINGS ===================
st.markdown('<hr style="border:1px solid #333;margin-top:40px;">', unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align:center;padding:30px;background:rgba(20,20,40,0.6);border-radius:15px;margin-top:20px;border:2px solid #00ffff;box-shadow:0 0 30px rgba(0,255,255,0.4);">
        <h1 style="color:#00ffff;font-size:48px;margin:0;text-shadow:0 0 20px #00ffff;">$847,392</h1>
        <p style="color:#aaa;font-size:18px;margin-top:10px;">💎 TOTAL AI-DRIVEN SAVINGS THIS QUARTER</p>
        <p style="color:#666;font-size:14px;margin-top:15px;">Powered by Echolon AI | Last Updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    unsafe_allow_html=True
)
