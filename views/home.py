import streamlit as st

def show_home():
    # Hide sidebar
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {display:none;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="fade">
        <h1 style="text-align:center; margin-bottom:50px;">
            🌍 Climate Sensitive Disease Detection System
        </h1>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="card ripple">
            <h2>👥 Public User</h2>
            <p>View reports and geo heatmaps</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Continue as Public", use_container_width=True):
            st.session_state.user_role = "public"
            st.session_state.page = "login"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="card ripple">
            <h2>🧑‍⚕️ ASHA Worker</h2>
            <p>Submit symptoms, forecasting & alerts</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Continue as ASHA", use_container_width=True):
            st.session_state.user_role = "asha"
            st.session_state.page = "login"
            st.rerun()

    st.markdown("""
    <style>
    .fade {animation: fadeIn 0.7s ease;}
    @keyframes fadeIn {
        from {opacity:0; transform:translateY(10px);}
        to {opacity:1;}
    }

    .card {
        background: linear-gradient(145deg,#0f172a,#020617);
        padding:50px;
        border-radius:20px;
        text-align:center;
        box-shadow:0 20px 40px rgba(0,0,0,0.4);
        transition:0.3s;
    }

    .card:hover {
        transform:scale(1.04);
        box-shadow:0 30px 60px rgba(0,0,0,0.6);
    }

    .ripple:active {
        animation: ripple 0.4s ease;
    }

    @keyframes ripple {
        0% {transform:scale(1);}
        50% {transform:scale(0.95);}
        100% {transform:scale(1);}
    }
    </style>
    """, unsafe_allow_html=True)
