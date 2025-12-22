import streamlit as st
from utils.firebase_utils import load_reports
from utils.page_refresh import page_refresh_button
from datetime import datetime
from utils.auth_guard import require_login
require_login()



def show_dashboard():

    # ---------------- GREETING ----------------
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "🌅 Good Morning"
    elif current_hour < 17:
        greeting = "🌤️ Good Afternoon"
    else:
        greeting = "🌙 Good Evening"

    # ---------------- SESSION SAFETY ----------------
    if "sidebar_open" not in st.session_state:
        st.session_state.sidebar_open = True

    if "quick_nav" not in st.session_state:
        st.session_state.quick_nav = None

    role = st.session_state.user_role
    choice = st.session_state.get("current_page", "Home")

    # ---------------- OPEN SIDEBAR BUTTON ----------------
    if not st.session_state.sidebar_open:
        if st.button("≫", help="Open Navigation"):
            st.session_state.sidebar_open = True
            st.rerun()

    # ---------------- STYLES ----------------
    st.markdown("""
    <style>
    .fade-in {
        animation: fadeSlide 0.9s ease-out;
    }

    @keyframes fadeSlide {
        from {opacity: 0; transform: translateY(15px);}
        to {opacity: 1; transform: translateY(0);}
    }

    .quick-tabs {
        display: flex;
        gap: 12px;
        margin: 18px 0 25px 0;
        flex-wrap: wrap;
    }

    .quick-tabs button {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        color: #111827 !important;
        padding: 10px 18px !important;
        border-radius: 999px !important;
        font-weight: 500 !important;
    }

    .quick-tabs button:hover {
        background-color: #f3f4f6 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- WELCOME ----------------
    st.markdown(f"""
    <div class="fade-in">
        <h3>{greeting} </h3>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- SIDEBAR ----------------
    if st.session_state.sidebar_open:
        with st.sidebar:
            st.title("📌 Navigation")

            if role == "asha":
                menu = ["Home", "Forecasting", "Symptom Based", "Reports", "Geo Heatmaps", "Alerts", "info"]
            else:
                menu = ["Home", "Reports", "Geo Heatmaps", "Alerts", "info"]

            choice = st.radio("Go to", menu, key="nav_choice")

            # APPLY QUICK NAV AFTER RADIO
            if st.session_state.quick_nav:
                choice = st.session_state.quick_nav
                st.session_state.quick_nav = None

            st.markdown("---")

            if st.button("❌ Close Menu"):
                st.session_state.sidebar_open = False
                st.rerun()

            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.session_state.page = "landing"
                st.rerun()

    # ---------------- HOME ----------------
    if choice == "Home":
        st.title(f"Welcome {role.upper()} 👋")
        

        reports = load_reports()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Reports", len(reports))
        with col2:
            high_risk = sum(1 for r in reports if r.get("Risk") == "High")
            st.metric("High Risk Reports", high_risk)

        st.info(
            "📊 Use the sidebar to navigate.\n\n"
            "• Public users can view reports & maps\n\n"
            "• ASHA users can submit symptoms & run forecasts"
        )

        # ---------- QUICK ACCESS ----------
        st.markdown("""
        <div style="
            margin-top: 25px;
            margin-bottom: 10px;
            font-weight: 600;
            font-size: 16px;
            color: #111827;">
            ⚡ Quick Access
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='quick-tabs'>", unsafe_allow_html=True)

        if role == "asha":
            c1, c2, c3, c4 = st.columns(4)

            with c1:
                if st.button("📈 Forecasting"):
                    st.session_state.quick_nav = "Forecasting"
                    st.rerun()

            with c2:
                if st.button("🩺 Symptom Based"):
                    st.session_state.quick_nav = "Symptom Based"
                    st.rerun()

            with c3:
                if st.button("📊 Reports"):
                    st.session_state.quick_nav = "Reports"
                    st.rerun()

            with c4:
                if st.button("🗺️ Geo Heatmaps"):
                    st.session_state.quick_nav = "Geo Heatmaps"
                    st.rerun()
        else:
            c1, c2 = st.columns(2)

            with c1:
                if st.button("📊 Reports"):
                    st.session_state.quick_nav = "Reports"
                    st.rerun()

            with c2:
                if st.button("🗺️ Geo Heatmaps"):
                    st.session_state.quick_nav = "Geo Heatmaps"
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- ROUTES ----------------
    elif choice == "Forecasting":
        if role != "asha":
            st.error("⛔ Access denied.")
            return
        from views.forecasting import show_forecasting
        show_forecasting()

    elif choice == "Symptom Based":
        if role != "asha":
            st.error("⛔ Access denied.")
            return
        from views.symptom_report import show_symptom_report
        show_symptom_report()

    elif choice == "Reports":
        from views.reports import show_reports
        show_reports()

    elif choice == "Geo Heatmaps":
        from views.geo_heatmaps import show_geo_heatmaps
        show_geo_heatmaps()

    elif choice == "Alerts":
        from views.alerts import show_alerts
        show_alerts()

    elif choice == "info":
        from views.info import show_info
        show_info()
    page_refresh_button()
