import streamlit as st




# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="🩺 Epidemiological Analysis & Forecasting",
    page_icon="🩺",
    layout="wide"
)

# ---------------- SESSION FLAGS ----------------
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = True

# ---------------- HIDE STREAMLIT NAV ----------------
st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- GLOBAL HEALTH DASHBOARD THEME ----------------
st.markdown("""
<style>

/* ---------- APP BACKGROUND ---------- */
.stApp {
    background-color: #f8f9fb;
}

/* ---------- MAIN CONTENT ---------- */
section.main > div {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 10px;
}

/* ---------- HEADINGS ---------- */
h1, h2, h3, h4 {
    color: #065f46 !important;
    font-weight: 700;
}

/* ---------- NORMAL TEXT ---------- */
p, span, label {
    color: #111827 !important;
}

/* Markdown + metrics */
[data-testid="stMarkdownContainer"] *,
[data-testid="metric-container"] * {
    color: #111827 !important;
}

/* ---------- METRICS ---------- */
[data-testid="metric-container"] {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 15px;
}

/* ---------- INPUTS / SELECTS / TEXTAREA ---------- */
div[data-baseweb="input"] input,
div[data-baseweb="select"] > div,
textarea {
    background-color: #f3f4f6 !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
    color: #111827 !important;
}

/* Focus border (matches your screenshot) */
div[data-baseweb="input"] input:focus,
div[data-baseweb="select"]:has(:focus),
textarea:focus {
    border-color: #ef4444 !important;
    box-shadow: none !important;
}

/* ---------- BUTTONS (NEUTRAL, HEALTH UI) ---------- */
.stButton > button {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
    font-weight: 500;
}

.stButton > button:hover {
    background-color: #f3f4f6 !important;
}

/* ---------- ALERTS / INFO BOX ---------- */
[data-testid="stAlert"] {
    background-color: #e0f2fe !important;
    border-radius: 10px !important;
    color: #111827 !important;
}

/* ---------- FILE UPLOADER (DASHBOARD) ---------- */
[data-testid="stFileUploader"] {
    background-color: #1f2937 !important;
    border-radius: 10px !important;
    padding: 14px !important;
}

[data-testid="stFileUploader"] * {
    color: #ffffff !important;
}

/* ================================================= */
/* =============== WHITE TABLE THEME =============== */
/* ================================================= */

[data-testid="stDataFrame"] {
    background-color: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 10px !important;
}

/* AG Grid base */
.ag-root-wrapper {
    background-color: #ffffff !important;
    border-radius: 10px !important;
}

/* Table header */
.ag-header {
    background-color: #f9fafb !important;
    border-bottom: 1px solid #e5e7eb !important;
}

.ag-header-cell-label {
    color: #111827 !important;
    font-weight: 600 !important;
}

/* Rows */
.ag-row {
    background-color: #ffffff !important;
    border-bottom: 1px solid #f1f5f9 !important;
}

.ag-row-even {
    background-color: #f9fafb !important;
}

/* Cells */
.ag-cell {
    color: #111827 !important;
    font-size: 14px !important;
}

/* Hover */
.ag-row-hover {
    background-color: #eef2ff !important;
}

/* Remove focus outline */
.ag-cell-focus {
    border: none !important;
}

/* Scrollbar */
.ag-body-viewport::-webkit-scrollbar {
    height: 8px;
    width: 8px;
}

.ag-body-viewport::-webkit-scrollbar-thumb {
    background-color: #cbd5e1;
    border-radius: 8px;
}

.ag-body-viewport::-webkit-scrollbar-track {
    background-color: #f1f5f9;
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background-color: #f9fafb;
    border-right: 1px solid #e5e7eb;
}

section[data-testid="stSidebar"] * {
    color: #111827 !important;
}

/* ---------- REMOVE STREAMLIT HEADER/FOOTER ---------- */
header, footer {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR VISIBILITY ----------------
if not st.session_state.show_sidebar:
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- HIDE SIDEBAR OUTSIDE DASHBOARD ----------------
if st.session_state.get("page") != "dashboard":
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
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

elif st.session_state.page == "dashboard":
    from views.dashboard import show_dashboard
    show_dashboard()

elif st.session_state.page == "info":
    from views.info import show_info
    show_info()

else:
    st.session_state.page = "landing"
    st.rerun()
