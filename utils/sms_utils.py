from twilio.rest import Client
import streamlit as st


def send_sms(phone_numbers, message):
    """
    Sends WhatsApp alert using Twilio WhatsApp Sandbox
    phone_numbers: list of numbers in +91XXXXXXXXXX format
    message: string
    """

    try:
        account_sid = st.secrets["TWILIO"]["ACCOUNT_SID"]
        auth_token = st.secrets["TWILIO"]["AUTH_TOKEN"]
    except KeyError:
        return [{"error": "Twilio credentials missing in secrets.toml"}]

    client = Client(account_sid, auth_token)

    results = []

    for number in phone_numbers:
        try:
            msg = client.messages.create(
                body=message,
                from_="whatsapp:+14155238886",   # Twilio WhatsApp Sandbox
                to=f"whatsapp:{number}"
            )
            results.append({"to": number, "sid": msg.sid})

        except Exception as e:
            results.append({"to": number, "error": str(e)})

    return results
