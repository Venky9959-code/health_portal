import streamlit as st

def show_home():
    # Hide sidebar
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {display:none;}
    </style>
    """, unsafe_allow_html=True)

    # ---------- PAGE HEADING ----------
    st.markdown("""
    <div class="fade home-header">
        <h1 class="home-title">
            🩺 Epidemiological Analysis & Forecasting
        </h1>
        <p class="home-subtitle">
            Area-specific disease forecasting & early health alerts
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    # ---------- PUBLIC USER ----------
    with col1:
        st.markdown("""
        <div class="home-card">
            <div class="home-icon">👥</div>
            <h2>Public User</h2>
            <p>
                View disease trends, reports and geo heatmaps for awareness
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Continue as Public", use_container_width=True):
            st.session_state.user_role = "public"
            st.session_state.page = "login"
            st.rerun()

    # ---------- ASHA USER ----------
    with col2:
        st.markdown("""
        <div class="home-card">
            <div class="home-icon">🧑‍⚕️</div>
            <h2>ASHA Worker</h2>
            <p>
                Submit symptoms, access forecasts and receive health alerts
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Continue as ASHA", use_container_width=True):
            st.session_state.user_role = "asha"
            st.session_state.page = "login"
            st.rerun()

    # ---------- HEALTH THEME STYLES ----------
    st.markdown("""
    <style>
    .stApp {
        background-color: #f9fafb;
    }

    .fade {
        animation: fadeIn 0.7s ease;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .home-header {
        text-align: center;
        margin-bottom: 60px;
    }

    .home-title {
        font-size: 38px;
        font-weight: 800;
        color: #065f46;
        margin-bottom: 10px;
    }

    .home-subtitle {
        font-size: 16px;
        color: #475569;
    }

    .home-card {
        background: #ffffff;
        padding: 55px 45px;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        text-align: center;
        box-shadow: 0 18px 35px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        height: 100%;
    }

    .home-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 28px 55px rgba(0,0,0,0.12);
    }

    .home-icon {
        font-size: 48px;
        margin-bottom: 18px;
    }

    .home-card h2 {
        color: #0f766e;
        font-size: 24px;
        margin-bottom: 10px;
        font-weight: 700;
    }

    .home-card p {
        color: #475569;
        font-size: 15px;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)
