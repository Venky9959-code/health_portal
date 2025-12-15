import streamlit as st
import pandas as pd
from prophet import Prophet
from utils.page_refresh import page_refresh_button

def show_forecasting():
    st.header("Disease Forecasting (File Upload Only)")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=["csv", "xlsx"]
    )

   

    if not uploaded_file:
        st.info("Upload a file to continue")
        return
    
    page_refresh_button("🔄 Refresh Forecast")
    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Uploaded Data Preview")
    st.dataframe(df.head())

    # Validate columns
    if not {"date", "cases"}.issubset(df.columns):
        st.error("File must contain columns: date, cases")
        return

    # Prepare for Prophet
    df = df.rename(columns={"date": "ds", "cases": "y"})
    df["ds"] = pd.to_datetime(df["ds"])

    if st.button("Run Forecast"):
        with st.spinner("Running Prophet model..."):
            model = Prophet()
            model.fit(df)

            future = model.make_future_dataframe(periods=30)
            forecast = model.predict(future)

        st.success("Forecast completed")

        st.subheader("Forecast Trend")
        st.line_chart(forecast.set_index("ds")[["yhat"]])

        st.subheader("Forecast Values")
        st.dataframe(
            forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(10)
        )
