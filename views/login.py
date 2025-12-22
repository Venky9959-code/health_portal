import streamlit as st
import time
from utils.auth_utils import login_user
import requests

def send_password_reset(email):
    api_key = "YOUR_FIREBASE_WEB_API_KEY"

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}"
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": email
    }
    r = requests.post(url, json=payload)
    return r.status_code == 200


def show_login():

    role = st.session_state.get("user_role") or "User"

    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {display:none;}

    .stApp {
        background-color: #f9fafb;
    }

    .register-box {
        max-width: 480px;
        margin: 60px auto 40px auto;
        padding: 40px;
        border-radius: 20px;
        background: #ffffff;
        box-shadow: 0 30px 60px rgba(0,0,0,0.08);
        text-align: center;
        animation: fadeUp .6s ease;
    }

    @keyframes fadeUp {
        from {opacity:0; transform:translateY(20px);}
        to {opacity:1; transform:translateY(0);}
    }

    .title {
        font-size: 26px;
        font-weight: 700;
        color: #065f46;
        margin-bottom: 6px;
    }

    .subtitle {
        color: #475569;
        margin-bottom: 24px;
        font-size: 15px;
    }

    /* DARK INPUT FIELDS */
    input {
        background: #1f2937 !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        padding: 12px !important;
        border: none !important;
    }

    input::placeholder {
        color: #9ca3af !important;
    }

    /* HEALTH BUTTONS */
    button {
        background: #16a34a !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 12px 0 !important;
        border: none !important;
        transition: all 0.3s ease;
    }

    button:hover {
        background: #15803d !important;
        box-shadow: 0 10px 25px rgba(22,163,74,0.4);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="register-box">
        <div class="title">🔐 Login ({role.upper()})</div>
        <div class="subtitle">Access your dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 2, 1])

    with center:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):

            if not username or not password:
                st.warning("Please enter username and password")
                return

            with st.spinner("Logging in..."):
                time.sleep(0.6)
                try:
                    uid, role, uname, email = login_user(username, password)
                except Exception:
                    st.error("Invalid username or password")
                    return

            # ✅ SESSION SETUP
            st.session_state.logged_in = True
            st.session_state.user_id = uid
            st.session_state.user_role = role
            st.session_state.username = uname
            st.session_state.email = email

            st.success("Login successful!")
            time.sleep(0.4)
            st.session_state.page = "dashboard"
            st.rerun()

        if st.button("← Back to Register", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()

        if st.button("Forgot Password?"):
            if not username:
                st.warning("Enter your username first")
                return

            from utils.auth_utils import get_email_by_username
            email = get_email_by_username(username)

            if not email:
                st.error("User not found")
                return

            if send_password_reset(email):
                st.success("Password reset email sent")
            else:
                st.error("Failed to send reset email")

