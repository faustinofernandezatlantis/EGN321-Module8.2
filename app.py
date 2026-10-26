import os
import sqlite3
import logging
from datetime import datetime
import pandas as pd
import streamlit as st

# ==========================================
# 1. CONFIGURATION & DIRECTORIES
# ==========================================
LOG_DIR = "logs"
DATA_DIR = "data"
LOG_FILE = os.path.join(LOG_DIR, "app.log")
DB_FILE = os.path.join(DATA_DIR, "history.db")

for folder in [LOG_DIR, DATA_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Setup Logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def log_event(level: str, message: str):
    """Logs system events to app.log file."""
    if level == "INFO":
        logging.info(message)
    elif level == "WARNING":
        logging.warning(message)
    elif level == "ERROR":
        logging.error(message)

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processing_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            filename TEXT,
            record_count INTEGER,
            avg_temp REAL,
            avg_pressure REAL,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_to_history(filename: str, count: int, avg_temp: float, avg_press: float, status: str):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO processing_history (timestamp, filename, record_count, avg_temp, avg_pressure, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filename, count, avg_temp, avg_press, status))
        conn.commit()
        conn.close()
    except Exception as e:
        log_event("ERROR", f"Database error: {str(e)}")

# Initialize Session State
if "health_status" not in st.session_state:
    st.session_state.health_status = "HEALTHY"
    log_event("INFO", "Capstone Application initialized with status: HEALTHY")

# ==========================================
# 2. PAGE UI CONFIGURATION
# ==========================================
st.set_page_config(page_title="Capstone: Engineering Data Processor", page_icon="⚙️", layout="wide")

st.title("⚙️ Engineering Data Processor — Capstone Application")
st.caption("Module 8.2 — From Workbook to Working Application")

# Health Status Banner
health = st.session_state.health_status
if health == "HEALTHY":
    st.success("🟢 System Health: HEALTHY — Fully operational.")
elif health == "DEGRADED":
    st.warning("🟡 System Health: DEGRADED — Warnings encountered during processing.")
elif health == "FAILED":
    st.error("🔴 System Health: FAILED — Operation refused or error occurred. Inspect logs.")

st.markdown("---")

# Navigation Tabs
tab_app, tab_history, tab_logs = st.tabs(["🚀 Application & Calculations", "📜 SQLite Execution History", "📋 Diagnostic Logs"])

# ==========================================
# TAB 1: MAIN APPLICATION
# ==========================================
with tab_app:
    st.sidebar.header("📥 Input Panel")
    st.sidebar.markdown("**Expected CSV Headers:** `timestamp`, `temperature`, `pressure`")
    
    uploaded_file = st.sidebar.file_uploader("Upload CSV Dataset", type=["csv"])
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📐 Engineering Safety Bounds")
    st.sidebar.info(
        "• **Temperature Range:** -40.0 °C to 120.0 °C\n"
        "• **Pressure Range:** 0.0 kPa to 500.0 kPa"
    )

    if uploaded_file is not None:
        log_event("INFO", f"Dataset uploaded for processing: {uploaded_file.name}")
        
        try:
            df = pd.read_csv(uploaded_file)
            
            # Validation 1: Required Columns Check
            required_cols = {"timestamp", "temperature", "pressure"}
            if not required_cols.issubset(df.columns):
                st.session_state.health_status = "FAILED"
                err_msg = f"Refusal: CSV missing required columns. Expected: {list(required_cols)}"
                st.error(f"❌ **Data Refused:** {err_msg}")
                log_event("ERROR", err_msg)
                save_to_history(uploaded_file.name, 0, 0.0, 0.0, "FAILED_MISSING_COLUMNS")
                st.stop()
                
            # Validation 2: Engineering Safety Range Check
            temp_out = df[(df["temperature"] < -40.0) | (df["temperature"] > 120.0)]
            press_out = df[(df["pressure"] < 0.0) | (df["pressure"] > 500.0)]
            
            if not temp_out.empty or not press_out.empty:
                st.session_state.health_status = "FAILED"
                refusal_msg = "Out-of-range sensor readings detected. Execution refused for system safety."
                st.error(f"🚫 **Tool Refusal:** {refusal_msg}")
                st.warning("Safety Limits: Temperature [-40.0°C, 120.0°C] | Pressure [0.0, 500.0 kPa]")
                log_event("ERROR", refusal_msg)
                save_to_history(uploaded_file.name, len(df), 0.0, 0.0, "FAILED_OUT_OF_BOUNDS")
                st.stop()
                
            # Process Valid Calculation
            st.session_state.health_status = "HEALTHY"
            avg_temp = float(df["temperature"].mean())
            avg_press = float(df["pressure"].mean())
            rec_count = len(df)
            
            log_event("INFO", f"Successfully computed metrics for {rec_count} rows from {uploaded_file.name}")
            save_to_history(uploaded_file.name, rec_count, avg_temp, avg_press, "HEALTHY")
            
            # Display Results
            st.subheader("📊 Execution Results & Calculations")
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Records Processed", rec_count)
            c2.metric("Average Temperature (°C)", f"{avg_temp:.2f}")
            c3.metric("Average Pressure (kPa)", f"{avg_press:.2f}")
            
            st.markdown("### Processed Dataset Preview")
            st.dataframe(df, use_container_width=True)
            
            st.markdown("### Sensor Trends Over Time")
            chart_data = df.set_index("timestamp")[["temperature", "pressure"]]
            st.line_chart(chart_data)
            
        except Exception as e:
            st.session_state.health_status = "FAILED"
            err_details = f"Processing Exception: {str(e)}"
            st.error(f"❌ {err_details}")
            log_event("ERROR", err_details)
    else:
        st.info("👋 Welcome to the Capstone Processor! Please upload a valid CSV file using the sidebar.")

# ==========================================
# TAB 2: SQLITE HISTORY
# ==========================================
with tab_history:
    st.subheader("📜 Historical Execution Log (SQLite Database)")
    st.markdown("All execution attempts and verification states are stored persistently in `data/history.db`.")
    
    if os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        history_df = pd.read_sql_query("SELECT * FROM processing_history ORDER BY id DESC", conn)
        conn.close()
        
        if not history_df.empty:
            st.dataframe(history_df, use_container_width=True)
        else:
            st.write("No historical runs recorded yet.")
    else:
        st.write("Database file not found.")

# ==========================================
# TAB 3: DIAGNOSTIC LOGS
# ==========================================
with tab_logs:
    st.subheader("📋 System Diagnostic Logs (`logs/app.log`)")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            log_data = f.read()
        st.text_area("Log Output", log_data, height=300)
    else:
        st.write("No log file found.")