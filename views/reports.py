import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from utils.firebase_utils import load_reports, delete_old_reports



def risk_color(risk):
    if isinstance(risk, str):
        if risk.lower() == "high":
            return "🔴 High"
        elif risk.lower() == "medium":
            return "🟠 Medium"
    return "🟢 Low"

def clean_report_data(df):
    # Normalize text columns
    df["Location"] = df["Location"].astype(str).str.strip().str.title()
    df["Risk"] = df["Risk"].astype(str).str.strip().str.capitalize()
    df["Disease"] = df["Disease"].astype(str).str.strip().str.title()

    # Convert Date
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    return df


def export_pdf(df):
    file_path = "reports.pdf"
    c = canvas.Canvas(file_path)
    y = 800

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Health Reports")
    y -= 30
    c.setFont("Helvetica", 10)

    for _, row in df.iterrows():
        text = f"{row.get('date','')} | {row.get('location','')} | {row.get('disease','')} | {row.get('risk','')}"
        c.drawString(40, y, text)
        y -= 18
        if y < 50:
            c.showPage()
            y = 800

    c.save()
    return file_path


def show_reports():
    st.header("📊 Reports")

    reports = load_reports()

    if not reports:
        st.info("No reports available yet.")
        return

    df = pd.DataFrame(reports)

    # ---------- SAFETY CHECK ----------
    if "risk" not in df.columns:
        df["risk"] = "Low"

    if "date" not in df.columns:
        df["date"] = ""

    if "location" not in df.columns:
        df["location"] = "Unknown"

    if "disease" not in df.columns:
        df["disease"] = "Unknown"

    # ---------- RISK COLORING ----------
    df["risk"] = df["risk"].apply(risk_color)

    # ---------- SHOW TABLE ----------
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
   
    if st.session_state.user_role == "asha":
        if st.button("🗑️ Clear reports older than 30 days"):
            delete_old_reports(30)
            st.success("Old data cleared")
            st.experimental_rerun()

    # ---------- DISTRICT ANALYTICS ----------
    st.subheader("🗺️ District-wise Risk Summary")

    df = clean_report_data(df)

    district_summary = (
    df.groupby(["Location", "Risk"]).size().unstack(fill_value=0).reset_index())

    st.dataframe(district_summary, use_container_width=True)




    # ---------- TREND CHART ----------
    st.subheader("📈 Disease Trend Over Time")

    trend_df = df.dropna(subset=["Date", "Disease"])

    if not trend_df.empty:
        trend = (
        trend_df.groupby([trend_df["Date"].dt.date, "Disease"])
        .size()
        .reset_index(name="Cases"))

        st.line_chart(
        trend.pivot(index="Date", columns="Disease", values="Cases").fillna(0) )
    else:
        st.info("Not enough data to show trend.")

