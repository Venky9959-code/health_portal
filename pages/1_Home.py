import streamlit as st

def show_home():
    st.title("Community Health Surveillance System")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Public User", use_container_width=True):
            st.session_state.role = "public"
            st.session_state.page = "login"
            st.rerun()

    with col2:
        if st.button("ASHA / Employee", use_container_width=True):
            st.session_state.role = "asha"
            st.session_state.page = "login"
            st.rerun()
