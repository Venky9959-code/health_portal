import streamlit as st
import time
from utils.auth_utils import register_user


def show_register():

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
        <div class="title">📝 Register ({role.upper()})</div>
        <div class="subtitle">Create your account</div>
    </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 2, 1])

    with center:
        username = st.text_input("Username")
        email = st.text_input("Email (for recovery & communication)")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Register", use_container_width=True):

            if not username or not email or not password or not confirm:
                st.warning("Please fill all fields")
                return

            if password != confirm:
                st.error("Passwords do not match")
                return

            with st.spinner("Creating account..."):
                time.sleep(0.8)
                try:
                    register_user(username, email, password, role)
                except Exception as e:
                    st.error(str(e))
                    return

            st.success("Account created successfully!")
            time.sleep(0.5)
            st.session_state.page = "login"
            st.rerun()

        if st.button("← Back to Login", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
