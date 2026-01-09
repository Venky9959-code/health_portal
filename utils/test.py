import streamlit as st
from twilio.rest import Client

ACCOUNT_SID = st.secrets["TWILIO_ACCOUNT_SID"]
AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
FROM_NUMBER = st.secrets["TWILIO_PHONE_NUMBER"]

client = Client(ACCOUNT_SID, AUTH_TOKEN)

st.title("📩 Twilio Manual Test")

phone = st.text_input("Enter your phone number (with +91)")

if st.button("Send Test SMS"):
    try:
        msg = client.messages.create(
            body="✅ Twilio test successful from EPICS project",
            from_=FROM_NUMBER,
            to=phone
        )
        st.success(f"SMS sent! SID: {msg.sid}")
    except Exception as e:
        st.error(f"Failed: {e}")
