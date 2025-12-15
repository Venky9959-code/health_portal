import streamlit as st
from utils.firebase_utils import load_reports
from utils.page_refresh import page_refresh_button


def show_dashboard():
    role = st.session_state.user_role

    # 🔹 CSS (DEFINED ONCE – SAME STYLES)
    st.markdown("""
    <style>
    .fade-in {
        animation: fadeSlide 0.9s ease-out;
    }

    @keyframes fadeSlide {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .glass {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 18px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 10px 40px rgba(0,0,0,0.35);
    }

    /* Ripple button effect */
    button {
        position: relative;
        overflow: hidden;
    }

    button::after {
        content: "";
        position: absolute;
        width: 120%;
        height: 120%;
        top: 50%;
        left: 50%;
        background: rgba(255,255,255,0.25);
        transform: translate(-50%, -50%) scale(0);
        border-radius: 50%;
        transition: transform 0.5s ease;
    }

    button:active::after {
        transform: translate(-50%, -50%) scale(1);
    }

    .page-container {
        animation: fadeSlide 0.5s ease-in-out;
    }
    </style>
    """, unsafe_allow_html=True)

    # ✅ FIXED CLASS NAME (fade → fade-in)
    st.markdown(f"""
    <div class="fade-in">
        <h3>👋 Welcome, {role.upper()} user</h3>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- SIDEBAR (UNCHANGED) ----------------
    with st.sidebar:
        st.title("📌 Navigation")

        menu = ["Home", "Reports", "Geo Heatmaps", "Alerts"]

        if role == "asha":
            menu.insert(1, "Forecasting")
            menu.insert(2, "Symptom Based")

        choice = st.radio(
            "Select Page",
            menu,
            key="dashboard_menu"
        )

        st.markdown("---")
        st.write(f"👤 Logged in as: **{role.upper()}**")

        # LOGOUT (UNCHANGED LOGIC)
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "home"
            st.rerun()

    # ---------------- PAGE CONTENT WRAPPER ----------------
    st.markdown("<div class='page-container'>", unsafe_allow_html=True)

    # ---------------- HOME ----------------
    if choice == "Home":
        st.title(f"Welcome {role.upper()} 👋")
        page_refresh_button()

        reports = load_reports()

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Reports", len(reports))

        with col2:
            high_risk = sum(1 for r in reports if r.get("Risk") == "High")
            st.metric("High Risk Reports", high_risk)

        st.info(
            "📊 Use the sidebar to navigate.\n\n"
            "• Public users can **view reports & maps**\n"
            "• ASHA users can **submit symptoms & run forecasts**"
        )

    # ---------------- FORECASTING ----------------
    elif choice == "Forecasting":
        if role != "asha":
            st.error("⛔ Access denied. ASHA users only.")
            return

        from views.forecasting import show_forecasting
        show_forecasting()

    # ---------------- SYMPTOM BASED ----------------
    elif choice == "Symptom Based":
        if role != "asha":
            st.error("⛔ Access denied. ASHA users only.")
            return

        from views.symptom_report import show_symptom_report
        show_symptom_report()

    # ---------------- REPORTS ----------------
    elif choice == "Reports":
        from views.reports import show_reports
        show_reports()

    # ---------------- GEO HEATMAPS ----------------
    elif choice == "Geo Heatmaps":
        from views.geo_heatmaps import show_geo_heatmaps
        show_geo_heatmaps()
    
    elif choice == "Alerts":
        from views.alerts import show_alerts
        show_alerts()


    st.markdown("</div>", unsafe_allow_html=True)
