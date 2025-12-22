from utils.sms_utils import send_sms
import streamlit as st

res = send_sms(
    ["+919959826841"],
    "✅ WhatsApp alert test from EPICS"
)

st.write(res)
