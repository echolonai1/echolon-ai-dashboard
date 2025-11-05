"""
Echolon AI Dashboard MVP (Streamlit)
Modular MVP covering Phases 1 & 2:
 1. CSV/Google Sheets upload
 2. Real-time KPI charts/graphs
 3. Basic user authentication
 4. Database storage: Firebase/Supabase
 5. Manual data refresh
 6. Export/share to PDF/PNG
 7. Phase 2: Live connectors, auto-refresh, multiple source/data status log
"""
# ===================== Imports =====================
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import firebase_admin
from firebase_admin import credentials, firestore
from supabase import create_client, Client
import io
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import threading
import time
# Phase 2 imports (placeholders for now)
# Stripe, Shopify, QuickBooks connectors (to be configured)
# import stripe
# import shopify
# import quickbooks

# =================== PHASE 2 SCAFFOLDING ===================
# --- Data source connection functions ---
def fetch_google_sheet(sheet_url, creds_json):
    """Fetch data from Google Sheet."""
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(eval(creds_json), scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)
# Placeholders for other connectors:
def fetch_stripe_data():
    """Fetch data from Stripe API (placeholder function)."""
    # TODO: implement auth and fetch from Stripe
    return pd.DataFrame()
def fetch_shopify_data():
    """Fetch data from Shopify API (placeholder function)."""
    # TODO: implement auth and fetch from Shopify
    return pd.DataFrame()
def fetch_quickbooks_data():
    """Fetch data from QuickBooks API (placeholder function)."""
    # TODO: implement auth and fetch from QuickBooks
    return pd.DataFrame()

def notification_log(messages):
    """Display notifications/logs in sidebar."""
    st.sidebar.markdown("## Data Update Log")
    for m in messages[-10:]:
        st.sidebar.info(m)

# --- Auto-refresh/ingestion logic ---
class AutoDataIngestor:
    """Class to handle periodic data refresh from multiple sources."""
    def __init__(self, refresh_interval=600):
        self.refresh_interval = refresh_interval  # seconds (default: 10 min)
        self.last_refresh = None
        self.messages = []
        self.running = False
        self.data_sources = {}
        self.thread = None
    def add_source(self, key, fetch_function, params=None):
        self.data_sources[key] = (fetch_function, params or {})
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.refresh_loop, daemon=True)
        self.thread.start()
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
    def refresh_loop(self):
        while self.running:
            self.refresh_all()
            time.sleep(self.refresh_interval)
    def refresh_all(self):
        self.messages.append(f"Refreshing all sources at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        for key, (func, params) in self.data_sources.items():
            try:
                df = func(**params)
                self.messages.append(f"{key}: Success ({len(df)} rows)")
                st.session_state[f"source_{key}"] = df
            except Exception as e:
                self.messages.append(f"{key}: Error {e}")
        self.last_refresh = datetime.now()

# =============== 1. Basic User Authentication ===============
def login_module():
    st.sidebar.title('User Login')
    # For MVP: simple checkbox as mock auth
    login_status = st.sidebar.checkbox("Login (mock)")
    return login_status

# ============== 2. Data Upload Module ==============
def upload_module():
    st.header("Data Upload")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    sheet_url = st.text_input("Google Sheet URL")
    creds_json = st.text_area("Paste Google API credentials (JSON)", "{}")
    df = None
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("CSV uploaded!")
        except Exception as e:
            st.error(f"CSV error: {e}")
    elif sheet_url and creds_json:
        try:
            df = fetch_google_sheet(sheet_url, creds_json)
            st.success("Google Sheet loaded!")
        except Exception as e:
            st.error(f"Google Sheets error: {e}")
    return df

# ========= Multiple Data Source Selection =========
def data_source_selector():
    st.sidebar.markdown("## Data Source Selector")
    options = []
    if "source_GoogleSheet" in st.session_state:
        options.append("Google Sheet")
    # Add for placeholder APIs
    if "source_Stripe" in st.session_state:
        options.append("Stripe")
    if "source_Shopify" in st.session_state:
        options.append("Shopify")
    if "source_QuickBooks" in st.session_state:
        options.append("QuickBooks")
    selected = st.sidebar.selectbox("Active data source", options) if options else None
    return selected

# ============= 3. KPI Chart/Graph Module =============
def kpi_module(df):
    st.header("KPIs and Visualization")
    st.write(f"Rows: {len(df)} | Columns: {len(df.columns)}")
    st.dataframe(df.head())
    st.subheader("Summary Statistics")
    st.write(df.describe())
    st.subheader("Charts & Graphs")
    col = st.selectbox("Choose column to plot", df.columns)
    chart_type = st.radio("Choose chart type", ["Histogram", "Line"])
    fig, ax = plt.subplots()
    if chart_type == "Histogram":
        df[col].hist(ax=ax)
    else:
        ax.plot(df[col])
    st.pyplot(fig)
    return fig

# ============ 4. Database Storage Module ============
def database_module(df):
    """Store to Firebase and Supabase (MVP/mock)"""
    st.info("Saving to DBs (demo mode)")
    # ...firebase/supabase logic as above...

# ======= 5. Manual Data Refresh & App State Handling ========
def refresh_module():
    return st.sidebar.button("Refresh Data")

# =========== 6. Export/Share Module ===========
def export_module(fig):
    st.subheader("Export/Share")
    export_format = st.radio("Export Format", ["PDF", "PNG"])
    if st.button("Export Chart"):
        buf = io.BytesIO()
        export_type = "pdf" if export_format == "PDF" else "png"
        plt.savefig(buf, format=export_type)
        mime = "application/pdf" if export_format == "PDF" else "image/png"
        st.download_button(
            label=f"Download {export_format}",
            data=buf.getvalue(),
            file_name=f"dashboard_chart.{export_type}",
            mime=mime
        )

# ===================== MAIN LAYOUT =====================
st.set_page_config(page_title="Echolon AI Dashboard MVP", layout="wide")
st.title("Echolon AI Dashboard — MVP + Live Data Sync Scaffold (Phases 1 & 2)")
st.markdown("""Modular Streamlit dashboard for upload, KPIs, DB sync, live data, and export.""")

# 1. User Login Module
user_logged_in = login_module()

# 2. Instantiate AutoDataIngestor singleton and register sources
if "auto_ingestor" not in st.session_state:
    ingestor = AutoDataIngestor(refresh_interval=600)  # 10 min by default
    st.session_state["auto_ingestor"] = ingestor
else:
    ingestor = st.session_state["auto_ingestor"]
# Always update sources in the ingestor (for demo, allow Google Sheet with supplied URL/creds)
if "google_sheet_url" not in st.session_state:
    st.session_state["google_sheet_url"] = ""
if "google_creds_json" not in st.session_state:
    st.session_state["google_creds_json"] = "{}"
# User can input them and enable auto-ingest from Google Sheets
sheet_url = st.sidebar.text_input("Auto-Ingest: Google Sheet URL", st.session_state["google_sheet_url"])
creds_json = st.sidebar.text_area("Auto-Ingest: Google API credentials", st.session_state["google_creds_json"])
auto_ingest_enabled = st.sidebar.checkbox("Enable auto Google Sheet ingest (demo)")
if auto_ingest_enabled and sheet_url and creds_json:
    st.session_state["google_sheet_url"] = sheet_url
    st.session_state["google_creds_json"] = creds_json
    ingestor.add_source("GoogleSheet", fetch_google_sheet, params={"sheet_url":sheet_url,"creds_json":creds_json})
    if not ingestor.running:
        ingestor.start()
# Demo: register placeholder sources
# ingestor.add_source("Stripe", fetch_stripe_data)
# ingestor.add_source("Shopify", fetch_shopify_data)
# ingestor.add_source("QuickBooks", fetch_quickbooks_data)

# 3. Data manual upload & refresh
refresh = refresh_module()
if user_logged_in:
    if refresh or "_app_df" not in st.session_state:
        st.session_state["_app_df"] = upload_module()
    df = st.session_state.get("_app_df", None)
    # Show Phase 2 notification/logging
    notification_log(ingestor.messages if ingestor else [])
    # Data source selection
    active_source = data_source_selector()
    used_df = None
    if active_source == "Google Sheet":
        used_df = st.session_state.get("source_GoogleSheet", None)
    elif active_source == "Stripe":
        used_df = st.session_state.get("source_Stripe", None)
    elif active_source == "Shopify":
        used_df = st.session_state.get("source_Shopify", None)
    elif active_source == "QuickBooks":
        used_df = st.session_state.get("source_QuickBooks", None)
    # Default to manual upload if nothing else
    if used_df is None:
        used_df = df
    # 4. Show KPIs if data is present
    if isinstance(used_df, pd.DataFrame) and not used_df.empty:
        fig = kpi_module(used_df)
        # 5. DB Storage
        database_module(used_df)
        # 6. Export/Share Section
        export_module(fig)
    else:
        st.info("Upload or auto-ingest data (CSV, Google Sheet, other sources) to see dashboard features.")
else:
    st.warning("Log in to access dashboard features.")
