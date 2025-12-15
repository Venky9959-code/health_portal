import streamlit as st
import time

def show_login():

    # --------- SESSION SAFETY ----------
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    role = st.session_state.get("user_role") or "User"
    is_login = st.session_state.auth_mode == "login"

    # --------- STYLES ----------
    st.markdown("""
    <style>
    .login-box {
        max-width: 420px;
        margin: 70px auto 20px auto;
        padding: 40px;
        border-radius: 18px;
        background: linear-gradient(145deg,#0f172a,#020617);
        box-shadow: 0 25px 60px rgba(0,0,0,.5);
        animation: fadeUp .6s ease;
    }

    @keyframes fadeUp {
        from {opacity:0; transform:translateY(20px);}
        to {opacity:1; transform:translateY(0);}
    }

    .title {
        text-align:center;
        font-size:26px;
        font-weight:700;
        margin-bottom:6px;
    }

    .subtitle {
        text-align:center;
        opacity:.8;
        margin-bottom:10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # --------- CARD ----------
    st.markdown(f"""
    <div class="login-box">
        <div class="title">
            {'🔐 Login' if is_login else '📝 Register'} ({role.upper()})
        </div>
        <div class="subtitle">
            {'Sign in to continue' if is_login else 'Create your account'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --------- CENTERED FORM ----------
    _, center, _ = st.columns([1, 2, 1])

    with center:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if not is_login:
            confirm = st.text_input("Confirm Password", type="password")

        if st.button("Login" if is_login else "Register", use_container_width=True):

            if not username or not password:
                st.warning("Please fill all fields")
                return

            if not is_login and password != confirm:
                st.error("Passwords do not match")
                return

            with st.spinner("Authenticating..."):
                time.sleep(1.2)

            # ✅ SUCCESS
            st.session_state.logged_in = True
            st.session_state.page = "dashboard"

            st.success("Login successful")
            time.sleep(0.4)
            st.experimental_rerun()

        # --------- SWITCH ----------
        if is_login:
            if st.button("Create an account", use_container_width=True):
                st.session_state.auth_mode = "register"
                st.rerun()
        else:
            if st.button("← Back to Login", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()

