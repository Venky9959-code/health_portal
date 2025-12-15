import streamlit as st

def page_refresh_button(label="🔄 Refresh Page"):
    if st.button(label):
        st.rerun()
