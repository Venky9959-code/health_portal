import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from utils.firebase_utils import load_reports, delete_old_reports
from utils.auth_guard import require_login
require_login()



# ---------- RISK DISPLAY ----------
def risk_color(risk):
    if isinstance(risk, str):
        if risk.lower() == "high":
            return "🔴 High"
        elif risk.lower() == "medium":
            return "🟠 Medium"
    return "🟢 Low"


# ---------- CLEAN & NORMALIZE ----------
def clean_report_data(df):

    rename_map = {
        "Risk": "risk",
        "Disease": "disease",
        "Location": "location",
        "Date": "date",
        "Timestamp": "date",
        "timestamp": "date"
    }

    df = df.rename(columns=rename_map)

    # Remove duplicate columns safely
    df = df.loc[:, ~df.columns.duplicated()]

    for col in ["location", "disease", "risk"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    if "population" in df.columns:
        df["population"] = pd.to_numeric(df["population"], errors="coerce").fillna(1)
        df["normalized_cases"] = 1 / df["population"]

    return df


# ---------- PDF EXPORT ----------
def export_pdf(df):
    file_path = "reports.pdf"
    c = canvas.Canvas(file_path)
    y = 800

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Health Reports")
    y -= 30
    c.setFont("Helvetica", 10)

    for _, row in df.iterrows():
        text = (
            f"{row.get('date','')} | "
            f"{row.get('location','')} | "
            f"{row.get('disease','')} | "
            f"{row.get('risk','')}"
        )
        c.drawString(40, y, text)
        y -= 18

        if y < 50:
            c.showPage()
            y = 800

    c.save()
    return file_path


# ---------- MAIN VIEW ----------
def show_reports():
    st.header("📊 Reports")

    reports = load_reports()

    if not reports:
        st.info("No reports available yet.")
        return

    df = pd.DataFrame(reports)

    # ---------- SAFETY DEFAULTS ----------
    for col in ["risk", "date", "location", "disease"]:
        if col not in df.columns:
            df[col] = ""

    # ---------- CLEAN ----------
    df = clean_report_data(df)

    # ---------- SORT (LATEST FIRST) ----------
    if "date" in df.columns:
        df = df.sort_values("date", ascending=False)

    # ---------- RISK ICONS ----------
    df["risk"] = df["risk"].apply(risk_color)

    # ---------- DISPLAY ----------
    st.dataframe(df, use_container_width=True)

    # ---------- EXPORT CSV ----------
    st.download_button(
        "📥 Download CSV",
        df.to_csv(index=False),
        file_name="health_reports.csv",
        mime="text/csv"
    )

    # ---------- EXPORT PDF ----------
    if st.button("📥 Download PDF"):
        pdf = export_pdf(df)
        with open(pdf, "rb") as f:
            st.download_button(
                "Click to download PDF",
                f,
                file_name="health_reports.pdf",
                mime="application/pdf"
            )

    # ---------- CLEAR OLD DATA ----------
    if st.session_state.get("user_role") == "asha":
        if st.button("🗑️ Clear reports older than 30 days"):
            delete_old_reports(30)
            st.success("Old data cleared")
            st.rerun()

    # ---------- TREND CHART ----------
    st.subheader("📈 Disease Trend Over Time")

    trend_df = df.dropna(subset=["date", "disease"])

    if not trend_df.empty:
        trend = (
            trend_df
            .groupby([trend_df["date"].dt.date, "disease"])
            .size()
            .reset_index(name="Cases")
        )

        st.line_chart(
            trend.pivot(index="date", columns="disease", values="Cases").fillna(0)
        )
    else:
        st.info("Not enough data to show trend.")
