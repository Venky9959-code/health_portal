import streamlit as st

def require_login():
    if not st.session_state.get("logged_in"):
        st.session_state.page = "login"
        st.rerun()
