import streamlit as st

st.set_page_config(
    page_title="Climate Sensitive Disease Detection System",
    layout="wide"
)

st.markdown("""
<style>
/* Hide Streamlit default app + page navigation */
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>

/* ---------- PAGE FADE IN ---------- */
.main {
    animation: fadeIn 0.6s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ---------- BUTTON HOVER ---------- */
.stButton > button {
    transition: all 0.25s ease-in-out;
    border-radius: 10px;
}

.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0px 6px 18px rgba(0, 123, 255, 0.35);
}

/* ---------- INPUT FOCUS ---------- */
input, textarea {
    transition: box-shadow 0.2s ease;
}

input:focus, textarea:focus {
    box-shadow: 0 0 0 2px #2563eb;
}

/* ---------- CARD EFFECT ---------- */
.card {
    background: linear-gradient(145deg, #0f172a, #020617);
    padding: 30px;
    border-radius: 20px;
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0px 25px 40px rgba(0,0,0,0.45);
}

/* ---------- SIDEBAR SLIDE ---------- */
section[data-testid="stSidebar"] {
    animation: slideIn 0.35s ease-out;
}

@keyframes slideIn {
    from { transform: translateX(-12px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

</style>
""", unsafe_allow_html=True)



# ---------------- HIDE SIDEBAR OUTSIDE DASHBOARD ----------------
if st.session_state.get("page") != "dashboard":
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)



# ---------------- SESSION DEFAULTS ----------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- ROUTER ----------------
if st.session_state.page == "landing":
    from views.home import show_home
    show_home()

elif st.session_state.page == "login":
    from views.login import show_login
    show_login()

elif st.session_state.page == "register":
    from views.register import show_register
    show_register()

elif st.session_state.page == "dashboard" and st.session_state.logged_in:
    from views.dashboard import show_dashboard
    show_dashboard()

else:
    st.session_state.page = "landing"
    st.experimental_rerun()
