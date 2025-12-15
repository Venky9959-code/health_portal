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

    # ---------- SAFETY NORMALIZATION ----------
    if "risk" in df.columns and "Risk" not in df.columns:
        df.rename(columns={"risk": "Risk"}, inplace=True)

    if "timestamp" in df.columns and "date" not in df.columns:
        df["date"] = df["timestamp"]

    if "Disease" in df.columns and "disease" not in df.columns:
        df["disease"] = df["Disease"]

    # ---------- FILTER HIGH RISK ----------
    if "Risk" not in df.columns:
        st.info("No risk data available.")
        return

    alerts = df[df["Risk"].str.lower() == "high"]

    if alerts.empty:
        st.success("✅ No High-Risk alerts detected")
        return

    st.error(f"🚨 {len(alerts)} HIGH-RISK ALERTS FOUND")

    # ---------- SAFE DISPLAY (ONLY EXISTING COLUMNS) ----------
    display_cols = []
    for col in ["location", "disease", "Risk", "date"]:
        if col in alerts.columns:
            display_cols.append(col)

    st.dataframe(
        alerts[display_cols],
        use_container_width=True
    )
