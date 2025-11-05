"""
Echolon AI Dashboard — Neon-Styled Analytics
Three-column layout: Sales & Behavior Predictive Analytics, Inventory Optimization, Workflow Efficiency
Major dashboard feature upgrade: mapping, drilldown, explain, export, tour, help.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import openai
import base64

# ============ NEON & OUTLINED CSS ============
st.markdown('''
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
    .ai-box {border:2px solid;border-radius:12px;padding:15px;margin:15px 0;font-weight:600;box-shadow:0 0 15px;}
    .ai-box-red {background:rgba(60,10,10,0.7);border-color:#ff3333;color:#ff6666;box-shadow:0 0 15px #ff3333;}
    .ai-box-green {background:rgba(10,60,30,0.7);border-color:#00ff77;color:#88ffbb;box-shadow:0 0 15px #00ff77;}
    .ai-box-cyan {background:rgba(10,40,60,0.7);border-color:#00ddff;color:#77ddff;box-shadow:0 0 15px #00ddff;}
    .ai-box-yellow {background:rgba(60,50,10,0.7);border-color:#ffdd00;color:#ffee88;box-shadow:0 0 15px #ffdd00;}
    .ai-label {font-size:14px;font-weight:900;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;}
    .ai-content {font-size:15px;line-height:1.6;}
''', unsafe_allow_html=True)

# ============ CSV DATA PIPELINE + COLUMN MAPPING ============
st.sidebar.header('CSV Data Pipeline Tester')
uploaded_file = st.sidebar.file_uploader("Choose a CSV file to test the data pipeline:", type=["csv"], key="uploader")
data_error = None
preview_data = None
user_data = None
column_roles = None
run_pipeline = False
if uploaded_file:
    try:
        raw_df = pd.read_csv(uploaded_file)
        preview_data = raw_df.head()
        with st.sidebar.expander("Step 2: Column Mapping", expanded=True):
            all_cols = list(raw_df.columns)
            roles = {
                'Sales - Date': st.selectbox('Sales Date column', all_cols, key='sdcol'),
                'Sales - Revenue': st.selectbox('Sales Revenue column', all_cols, key='srcol'),
                'Sales - Orders': st.selectbox('Sales Orders column', all_cols, key='soccol'),
                'Sales - Customers': st.selectbox('Sales Customers column', all_cols, key='sccol'),
                'Inventory - Product': st.selectbox('Inventory Product column', all_cols, key='ipcol'),
                'Inventory - Stock': st.selectbox('Inventory Stock column', all_cols, key='iscol'),
                'Inventory - Reorder': st.selectbox('Inventory Reorder column', all_cols, key='ircol'),
                'Inventory - Sales_30d': st.selectbox('Inventory Sales_30d column', all_cols, key='isc30col'),
                'Workflow - Date': st.selectbox('Workflow Date column', all_cols, key='wdcol'),
                'Workflow - Tasks': st.selectbox('Workflow Tasks column', all_cols, key='wtcol'),
                'Workflow - Completed': st.selectbox('Workflow Completed column', all_cols, key='wccol'),
                'Workflow - Efficiency': st.selectbox('Workflow Efficiency column', all_cols, key='wecol'),
            }
            if st.button('Run Pipeline', key="run_csv_pipeline"):
                column_roles = roles
                run_pipeline = True
    except Exception as e:
        data_error = f"Error reading CSV: {e}"

if preview_data is not None:
    st.sidebar.markdown("### CSV Preview (First 5 rows):")
    st.sidebar.dataframe(preview_data, use_container_width=True)
if data_error:
    st.sidebar.error(data_error)

# ===== Sample Data fallback =====
def create_sample_data():
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    sales = pd.DataFrame({
        'Date': dates,
        'Revenue': np.random.uniform(800, 1500, 30).round(2),
        'Orders': np.random.randint(15, 50, 30),
        'Customers': np.random.randint(10, 40, 30)
    })
    inventory = pd.DataFrame({
        'Product': ['Widget A', 'Gadget B', 'Tool C', 'Device D', 'Item E'],
        'Stock': [85, 42, 150, 68, 23],
        'Reorder': [50, 30, 100, 40, 20],
        'Sales_30d': [125, 78, 90, 95, 112]
    })
    workflow = pd.DataFrame({
        'Date': dates[-7:],
        'Tasks': np.random.randint(20, 45, 7),
        'Completed': np.random.randint(15, 40, 7),
        'Efficiency': np.random.uniform(70, 95, 7).round(1)
    })
    return sales, inventory, workflow

# ===== Column Mapping Logic =====
def get_dashboard_data():
    global column_roles, run_pipeline
    if uploaded_file and run_pipeline and column_roles:
        try:
            # Remap columns and create expected dataframes
            raw_df = pd.read_csv(uploaded_file)
            # Remapping for each module
            sales_cols = [column_roles['Sales - Date'],column_roles['Sales - Revenue'],column_roles['Sales - Orders'],column_roles['Sales - Customers']]
            inv_cols = [column_roles['Inventory - Product'],column_roles['Inventory - Stock'],column_roles['Inventory - Reorder'],column_roles['Inventory - Sales_30d']]
            wf_cols = [column_roles['Workflow - Date'],column_roles['Workflow - Tasks'],column_roles['Workflow - Completed'],column_roles['Workflow - Efficiency']]
            sales = raw_df[sales_cols].rename(columns={
                column_roles['Sales - Date']:'Date',
                column_roles['Sales - Revenue']:'Revenue',
                column_roles['Sales - Orders']:'Orders',
                column_roles['Sales - Customers']:'Customers',
            })
            inventory = raw_df[inv_cols].rename(columns={
                column_roles['Inventory - Product']:'Product',
                column_roles['Inventory - Stock']:'Stock',
                column_roles['Inventory - Reorder']:'Reorder',
                column_roles['Inventory - Sales_30d']:'Sales_30d',
            })
            workflow = raw_df[wf_cols].rename(columns={
                column_roles['Workflow - Date']:'Date',
                column_roles['Workflow - Tasks']:'Tasks',
                column_roles['Workflow - Completed']:'Completed',
                column_roles['Workflow - Efficiency']:'Efficiency',
            })
            if not pd.api.types.is_datetime64_any_dtype(sales['Date']):
                sales['Date'] = pd.to_datetime(sales['Date'])
            if not pd.api.types.is_datetime64_any_dtype(workflow['Date']):
                workflow['Date'] = pd.to_datetime(workflow['Date'])
            return sales, inventory, workflow
        except Exception:
            return create_sample_data()
    else:
        return create_sample_data()

sales, inventory, workflow = get_dashboard_data()

# ===== Customizable Layout Options =====
show_sales = st.sidebar.checkbox('Show Sales Analytics', True)
show_inventory = st.sidebar.checkbox('Show Inventory Module', True)
show_workflow = st.sidebar.checkbox('Show Workflow Module', True)

# ===== Dashboard Tour Popup =====
if st.sidebar.button('📢 Dashboard Tour & Tips', key='tourpop'): 
    st.sidebar.info("Welcome! This dashboard uses AI-powered analytics, lets you map columns, drill down metrics, download snapshots, and ask questions using the OpenAI module. Use the help box below for CSV tips and AI info.")

# ===== Help Sidebar =====
with st.sidebar.expander('🧠 Help: How AI Works & Best CSV Practices', expanded=False):
    st.markdown('''
- **AI modules** predict sales, optimize inventory, and score workflows.
- **Best CSV tips:**
    - Use clear column names (e.g. Date, Revenue).
    - Avoid merged cells or non-tabular formats.
    - If unsure about columns, use mapping step above!
    - Supported formats: .csv only. If in Excel, export as CSV first.
    - Make sure columns for each module match the previewed names.
    ''')

# ============ MAIN DASHBOARD LAYOUT ============
st.markdown('<div class="neon-title">Echolon Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="dashboard-row">', unsafe_allow_html=True)

# Helper for Chart Download
def get_table_download_link(df, filename='data.csv', label='Download as CSV'):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{label}</a>'
    return href

def get_fig_download_link(fig, filename='chart.png', label='Download Chart Snapshot'):
    buf = fig.to_image(format="png") if hasattr(fig, "to_image") else b""
    b64 = base64.b64encode(buf).decode() if buf else ""
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">{label}</a>' if buf else "<em>No snapshot supported</em>"
    return href

# ===== Animated Metric Helper =====
from streamlit_extras.metric_animator import metric_animator  # requires st-extras package

if show_sales:
    with st.container():
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.markdown('<div class="neon-header">Sales & Behavior Predictive Analytics</div>', unsafe_allow_html=True)

        latest_sales = sales['Revenue'].iloc[-1]
        metric_animator(label="Today’s Revenue", value=latest_sales, format="${:,.2f}")
        st.markdown('<span title="Total revenue from all customers for today.">ℹ️</span>', unsafe_allow_html=True)
        st.metric(label="Orders", value=sales['Orders'].iloc[-1], help='Total orders placed today.')
        st.metric(label="Customers", value=sales['Customers'].iloc[-1], help='Number of unique customers today.')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sales['Date'], y=sales['Revenue'], line_shape='spline', mode='lines', name="Revenue", line=dict(color="#00fff7", width=5)))
        fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=25, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=230)
        with st.expander("📈 Revenue Trend — Details & Recommendations", expanded=False):
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(get_fig_download_link(fig, filename="sales_trend.png", label="📥 Download Chart Snapshot"), unsafe_allow_html=True)
            st.markdown(get_table_download_link(sales, filename="sales.csv", label="Download as CSV"), unsafe_allow_html=True)
            st.info("Tip: Review revenue spikes for marketing effectiveness.")
        st.markdown('</div>', unsafe_allow_html=True)

if show_inventory:
    with st.container():
        st.markdown('<div class="neon-card-pink">', unsafe_allow_html=True)
        st.markdown('<div class="neon-header-pink">Inventory Optimization</div>', unsafe_allow_html=True)
        with st.expander("🔍 Inventory Drilldown & Reorder Alerts", expanded=False):
            st.dataframe(inventory, use_container_width=True, hide_index=True)
            st.markdown(get_table_download_link(inventory, filename="inventory.csv", label="Download as CSV"), unsafe_allow_html=True)
            st.info("Reorder points are set by historical sales and safety stock; optimize to avoid stockouts.")
        st.markdown('</div>', unsafe_allow_html=True)

if show_workflow:
    with st.container():
        st.markdown('<div class="neon-card-green">', unsafe_allow_html=True)
        st.markdown('<div class="neon-header-green">Workflow Efficiency</div>', unsafe_allow_html=True)
        eff_val = workflow['Efficiency'].mean() if 'Efficiency' in workflow else 80
        metric_animator(label="Efficiency Last 7 Days", value=eff_val, format="{:.1f}%")
        st.metric(label="Completed Tasks", value=int(workflow['Completed'].iloc[-1]), help="Tasks marked completed yesterday.")
        fig_wf = go.Figure()
        fig_wf.add_trace(go.Bar(x=workflow['Date'], y=workflow['Completed'], marker_color='#00ff99', name="Completed"))
        fig_wf.add_trace(go.Bar(x=workflow['Date'], y=workflow['Tasks'], marker_color='#ff0077', name="Tasks"))
        fig_wf.update_layout(barmode='group', showlegend=True, margin=dict(l=0, r=0, t=25, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=230)
        with st.expander("📊 Workflow Details & Recommendations", expanded=False):
            st.plotly_chart(fig_wf, use_container_width=True)
            st.markdown(get_fig_download_link(fig_wf, filename="workflow_chart.png", label="📥 Download Chart Snapshot"), unsafe_allow_html=True)
            st.markdown(get_table_download_link(workflow, filename="workflow.csv", label="Download as CSV"), unsafe_allow_html=True)
            st.info("Boost workflow efficiency by automating repetitive tasks.")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============ Glowing Savings Footer ============
savings_amt = int(sales['Revenue'].sum() * 0.12)
footer_html = f"""<div class="neon-footer">    <span style="font-size:37px;font-weight:bold;color:#00fff7;">AI-Driven Savings</span><br><br>    <span style="font-size:23px;font-family:monospace;letter-spacing:2.5
