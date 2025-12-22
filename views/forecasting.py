import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.express as px
from utils.page_refresh import page_refresh_button
from datetime import datetime


# ---------------- SESSION STATE INIT ----------------
if "last_forecast" not in st.session_state:
    st.session_state.last_forecast = None

if "last_forecast_meta" not in st.session_state:
    st.session_state.last_forecast_meta = None


def show_forecasting():

    # ---------- UI ALIGNMENT (WHITE HEALTH LAYOUT) ----------
    st.markdown("""
<style>

/* ========== FILE UPLOADER – FULL LIGHT THEME ========== */


/* ===== FILE UPLOADER BROWSE BUTTON (LIGHT WHITE) ===== */

/* Target the Browse files button specifically */
[data-testid="stFileUploader"] button {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    box-shadow: none !important;
}

/* Hover state */
[data-testid="stFileUploader"] button:hover {
    background-color: #f3f4f6 !important;
    border-color: #cbd5e1 !important;
}

/* Remove dark focus ring */
[data-testid="stFileUploader"] button:focus {
    outline: none !important;
    box-shadow: none !important;
}



/* Outer uploader box */
[data-testid="stFileUploader"] {
    background-color: #f9fafb !important;
    border: 1px dashed #d1d5db !important;
    border-radius: 10px !important;
    padding: 16px !important;
}

/* Inner drag & drop area */
[data-testid="stFileUploader"] section {
    background-color: #ffffff !important;
    border-radius: 8px !important;
}

/* Drag-drop instruction container */
[data-testid="stFileUploader"] div {
    background-color: #ffffff !important;
}

/* Cloud icon + text */
[data-testid="stFileUploader"] * {
    color: #111827 !important;
}

/* Remove dark overlay on hover */
[data-testid="stFileUploader"]:hover {
    background-color: #f9fafb !important;
}

/* Info message below uploader */
[data-testid="stAlert"] {
    background-color: #e0f2fe !important;
    color: #111827 !important;
}

</style>
""", unsafe_allow_html=True)


    # ---------------- HEADER ----------------
    st.header("📈 Disease Forecasting (File Upload Only)")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=["csv", "xlsx"]
    )

    if not uploaded_file:
        st.info("Upload a file to continue")
        return

    page_refresh_button("🔄 Refresh Forecast")

    # ---------------- READ FILE ----------------
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📄 Uploaded Data Preview")
    st.dataframe(df.head())

    # ---------------- VALIDATION ----------------
    if not {"date", "cases"}.issubset(df.columns):
        st.error("❌ File must contain columns: date, cases")
        return

    # ---------------- PREPARE DATA ----------------
    df = df.rename(columns={"date": "ds", "cases": "y"})
    df["ds"] = pd.to_datetime(df["ds"])

    # ---------------- RUN FORECAST ----------------
    if st.button("▶ Run Forecast"):
        with st.spinner("Running Prophet model..."):
            model = Prophet()
            model.fit(df)

            future = model.make_future_dataframe(periods=30)
            forecast = model.predict(future)

        # Save forecast in session
        st.session_state.last_forecast = forecast
        st.session_state.last_forecast_meta = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rows": len(forecast)
        }

        st.success("✅ Forecast completed")

    # ---------------- SHOW RECENT FORECAST ----------------
    if st.session_state.last_forecast is not None:
        forecast = st.session_state.last_forecast

        st.subheader("📉 Recent Forecast Trend")

        # ---------- BLUE PLOT (UNCHANGED) ----------
        fig = px.line(
            forecast,
            x="ds",
            y="yhat",
            markers=True
        )

        fig.update_traces(
            line=dict(color="#1f77b4", width=4),
            marker=dict(size=7)
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_title="Date",
            yaxis_title="Cases",
            title_font_size=18
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------- FORECAST SUMMARY ----------------
        latest_value = int(forecast["yhat"].iloc[-1])
        avg_next = int(forecast["yhat"].tail(3).mean())

        if avg_next > 25:
            risk = "High"
            risk_color = "#dc2626"
        elif avg_next > 10:
            risk = "Medium"
            risk_color = "#f59e0b"
        else:
            risk = "Low"
            risk_color = "#16a34a"

        st.markdown(
            f"""
            <div style="
                padding:16px;
                border-radius:10px;
                background:#f8fafc;
                border:1px solid #e5e7eb">
                <h4>Forecast Summary</h4>
                <span style="
                    background:{risk_color};
                    color:white;
                    padding:6px 14px;
                    border-radius:6px;
                    font-weight:600">
                    Risk: {risk}
                </span>
                <p style="margin-top:12px">
                    Predicted cases in next 3 months (average):
                    <b>{avg_next}</b>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ---------------- TABLE ----------------
        st.subheader("📊 Forecast Values (Latest)")
        st.dataframe(
            forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(10),
            use_container_width=True
        )

        # ---------------- GEO METADATA ----------------
        st.subheader("🗺️ Forecast Metadata (Stored for Geo Analysis)")
        st.json(st.session_state.last_forecast_meta)
