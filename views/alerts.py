import streamlit as st
import pandas as pd
from utils.firebase_utils import load_reports
from utils.page_refresh import page_refresh_button


def show_alerts():
    st.header("🚨 Health Alerts")
    page_refresh_button("🔄 Refresh Alerts")

    reports = load_reports()

    if not reports:
        st.info("No alerts available.")
        return

    df = pd.DataFrame(reports)

    # ---------- STEP 1: NORMALIZE COLUMN NAMES ----------
    rename_map = {
        "Risk": "risk",
        "Disease": "disease",
        "Location": "location",
        "Date": "timestamp",
        "date": "timestamp"
    }
    df.rename(columns=rename_map, inplace=True)

    # ---------- STEP 2: REMOVE DUPLICATE COLUMNS (CRITICAL FIX) ----------
    df = df.loc[:, ~df.columns.duplicated()]

    # ---------- STEP 3: ENSURE REQUIRED COLUMNS ----------
    for col in ["location", "disease", "risk", "timestamp"]:
        if col not in df.columns:
            df[col] = None

    # ---------- STEP 4: CLEAN DATA ----------
    df["risk"] = df["risk"].astype(str).str.lower()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # ---------- STEP 5: FILTER HIGH RISK ----------
    alerts = df[df["risk"] == "high"]

    if alerts.empty:
        st.success("✅ No High-Risk alerts detected")
        return

    # ---------- STEP 6: SORT BY LATEST ----------
    alerts = alerts.sort_values("timestamp", ascending=False)

    st.error(f"🚨 {len(alerts)} HIGH-RISK ALERTS FOUND")

    # ---------- STEP 7: FINAL DISPLAY ----------
    st.dataframe(
        alerts[["location", "disease", "risk", "timestamp"]],
        use_container_width=True
    )
