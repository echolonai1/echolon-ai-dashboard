import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import firebase_admin
from firebase_admin import credentials, firestore
import supabase
from supabase import create_client, Client
import io
import matplotlib.pyplot as plt
from datetime import datetime

# ---------- AUTHENTICATION -----------
# Replace with your user management/auth as needed
user_logged_in = st.sidebar.checkbox("Login (mock)")   # MVP: Just a checkbox for auth prototype

# ---------- DATA UPLOAD (CSV & Google Sheets) -----------

def read_csv(uploaded_file):
    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success("CSV uploaded!")
            return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
    return None

def read_google_sheet(sheet_url, creds_json):
    try:
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_url(sheet_url).sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        st.success("Google Sheet loaded!")
        return df
    except Exception as e:
        st.error(f"Google Sheets error: {e}")
    return None

# ----------- DB STORAGE (Firebase/Supabase) --------------
# MVP: Store Data in Firebase/Supabase (Mock example)
def store_to_firebase(data):
    st.info("Storing data to Firebase (demo)")
    # Real implementation would require credentials & initialization
    # creds = credentials.Certificate('firebase-creds.json')
    # firebase_admin.initialize_app(creds)
    # db = firestore.client()
    # db.collection('uploaded_data').add({'data':data.to_dict()})

def store_to_supabase(data):
    st.info("Storing data to Supabase (demo)")
    # url = "<YOUR_SUPABASE_URL>"
    # key = "<YOUR_SUPABASE_KEY>"
    # supabase: Client = create_client(url, key)
    # supabase.table('uploaded_data').insert(data.to_dict()).execute()

# -------- MANUAL DATA REFRESH ---------
refresh = st.sidebar.button("Refresh Data")

# ----------- MAIN DASHBOARD -------------

st.title("Echolon AI Dashboard MVP")
st.write("Upload CSV/Google Sheets to see KPIs. Basic auth, DB, export & refresh included.")

uploaded_file = st.file_uploader("Upload CSV", type="csv")
sheet_url = st.text_input("Google Sheet URL")
creds_json = st.text_area("Google API credentials (JSON)", "{}")  # MVP Demo: Paste as text

if uploaded_file:
    df = read_csv(uploaded_file)
    if df is not None and user_logged_in:
        store_to_firebase(df)
        store_to_supabase(df)
elif sheet_url and creds_json and user_logged_in:
    try:
        creds_data = eval(creds_json)
        df = read_google_sheet(sheet_url, creds_data)
        if df is not None:
            store_to_firebase(df)
            store_to_supabase(df)
    except Exception as e:
        st.error(f"Invalid credentials: {e}")
else:
    df = None

# ----- DISPLAY KPIs & GRAPHS ------
if df is not None:
    st.subheader("KPIs")
    st.write(f"Rows: {len(df)}")
    st.write(f"Columns: {len(df.columns)}")
    st.write(f"Last Upload: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.dataframe(df.head())

    st.subheader("Column Summary")
    st.write(df.describe())

    st.subheader("Charts & Graphs")
    col = st.selectbox("Select column to visualize", df.columns)
    chart_type = st.radio("Chart Type", ["Histogram", "Line"])
    fig, ax = plt.subplots()
    if chart_type == "Histogram":
        df[col].hist(ax=ax)
    else:
        ax.plot(df[col])
    st.pyplot(fig)

    # ------- EXPORT TO PDF/PNG -------
    st.subheader("Export")
    export_format = st.radio("Export format", ["PDF", "PNG"])
    if st.button("Export Current Chart"):
        buf = io.BytesIO()
        plt.savefig(buf, format="pdf" if export_format == "PDF" else "png")
        st.download_button(
            label=f"Download {export_format}",
            data=buf.getvalue(),
            file_name=f"dashboard_chart.{export_format.lower()}",
            mime="application/pdf" if export_format == "PDF" else "image/png"
        )
else:
    st.info("Please login and upload a CSV or Google Sheet.")
