import requests
import streamlit as st

FAST2SMS_API_KEY = st.secrets.get("FAST2SMS_API_KEY")

def send_sms(phone_numbers, message):
    """
    phone_numbers: list of strings
    message: string
    """

    if not FAST2SMS_API_KEY:
        return {"error": "FAST2SMS API key missing"}

    payload = {
        "route": "q",
        "message": message,
        "numbers": ",".join(phone_numbers)
    }

    headers = {
        "authorization": FAST2SMS_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(
            "https://www.fast2sms.com/dev/bulkV2",
            data=payload,
            headers=headers,
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}
