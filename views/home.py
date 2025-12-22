import streamlit as st

def show_home():
    # Hide sidebar
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- PAGE HEADING ----------
    st.markdown("""
    <div class="page-wrapper fade">
        <h1 class="main-title">
            🩺 Epidemiological Analysis & Forecasting
        </h1>
        <p class="subtitle">
            Area-specific forecasting and early warning system for climate-sensitive diseases
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    # ---------- PUBLIC USER ----------
    with col1:
        st.markdown("""
        <div class="card">
            <div class="icon">👥</div>
            <h2>Public User</h2>
            <p>View disease reports, trends and geo heatmaps</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Continue as Public", use_container_width=True):
            st.session_state.user_role = "public"
            st.session_state.page = "login"
            st.rerun()

    # ---------- ASHA USER ----------
    with col2:
        st.markdown("""
        <div class="card">
            <div class="icon">🧑‍⚕️</div>
            <h2>ASHA Worker</h2>
            <p>Submit symptoms, access forecasts and alerts</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Continue as ASHA", use_container_width=True):
            st.session_state.user_role = "asha"
            st.session_state.page = "login"
            st.rerun()

    # ---------- UPDATED STYLES ----------
    st.markdown("""
    <style>
    /* Page background */
    .stApp {
        background: #f8fafc;
    }

    .page-wrapper {
        text-align: center;
        margin-bottom: 60px;
    }

    .main-title {
        color: #1e3a8a;
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .subtitle {
        color: #64748b;
        font-size: 16px;
    }

    .fade {
        animation: fadeIn 0.7s ease;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .card {
        background: #ffffff;
        padding: 55px 45px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        height: 100%;
    }

    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.12);
    }

    .icon {
        font-size: 48px;
        margin-bottom: 15px;
    }

    .card h2 {
        color: #1e40af;
        font-size: 26px;
        margin-bottom: 10px;
    }

    .card p {
        color: #475569;
        font-size: 15px;
        margin-bottom: 25px;
    }

    /* Buttons */
    button {
        background: linear-gradient(135deg, #2563eb, #1e40af) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px 0 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }

    button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(37,99,235,0.4);
    }
    </style>
    """, unsafe_allow_html=True)
