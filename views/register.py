import streamlit as st
import time

def show_register():

    # --------- SESSION SAFETY ----------
    role = st.session_state.get("user_role") or "User"

    # --------- STYLES ----------
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {display:none;}

    .register-box {
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
    <div class="register-box">
        <div class="title">
            📝 Register ({role.upper()})
        </div>
        <div class="subtitle">
            Create your account to continue
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --------- CENTERED FORM ----------
    _, center, _ = st.columns([1, 2, 1])

    with center:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Create Account", use_container_width=True):

            if not username or not password or not confirm:
                st.warning("Please fill all fields")
                return

            if password != confirm:
                st.error("Passwords do not match")
                return

            with st.spinner("Creating account..."):
                time.sleep(1.2)

            st.success("Account created successfully!")
            time.sleep(0.5)

            st.session_state.page = "login"
            st.experimental_rerun()

        if st.button("← Back to Login", use_container_width=True):
            st.session_state.page = "login"
            st.experimental_rerun()
