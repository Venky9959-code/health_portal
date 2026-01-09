import streamlit as st
from utils.auth_guard import require_login
require_login()


def show_info():

    st.title("ℹ️ Application Information")

    st.subheader("🩺 Epidemiological Analysis & Forecasting")
    st.write(
        "This application provides **area-specific disease surveillance** "
        "and **early warning alerts** for climate-sensitive diseases."
    )

    st.divider()

    st.subheader("🎯 Purpose")
    st.markdown("""
    - Monitor disease outbreaks  
    - Support public health decisions  
    - Enable early risk identification  
    """)

    st.divider()

    st.subheader("✨ Features")
    st.markdown("""
    - Symptom-based prediction (ASHA workers)  
    - Disease forecasting using Prophet  
    - Geo risk heatmaps  
    - Automated alerts for high-risk areas  
    """)

    st.divider()

    st.subheader("👥 User Roles")
    st.markdown("""
    - **Public Users** – View reports and maps  
    - **ASHA Workers** – Submit symptoms & run forecasts  
    """)

    st.divider()

    st.subheader("🛠️ Technologies Used")
    st.markdown("""
    - Streamlit (User Interface)  
    - Firebase (Realtime Database)  
    - Facebook Prophet (Forecasting)  
    - Plotly (Charts & Visualizations)  
    - Geopy (Location Services)  
    """)

    st.caption("© 2025 | Climate-Sensitive Disease Forecasting System")
