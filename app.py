# -*- coding: utf-8 -*-

import os
import time
import sys
import json      
import requests
from datetime import datetime


import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

import firebase_admin
from firebase_admin import credentials, firestore

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# ================== FORCE UTF-8 ==================
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# ================== STREAMLIT CONFIG ==================
st.set_page_config(
    page_title="Climate Sensitive Disease Forecasting",
    page_icon="🌍",
    layout="wide"
)


# ================== SECRETS ==================
FAST2SMS_API_KEY = st.secrets.get("FAST2SMS_API_KEY")

SMS_ALERT_THRESHOLD = 3
SMS_RECEIVERS = ["919959826841"]


# ================== FIREBASE INIT (FINAL FIX) ==================
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["FIREBASE_KEY"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()


# ================== PWA SUPPORT ==================
st.markdown("""
<link rel="manifest" href="/static/manifest.json">
<meta name="theme-color" content="#0E1117">
<script>
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/service-worker.js');
}
</script>
""", unsafe_allow_html=True)


# ================== LOCAL STORAGE ==================
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

OFFLINE_CACHE_FILE = os.path.join(DATA_DIR, "offline_cache.json")
GEOCODE_CACHE_FILE = os.path.join(DATA_DIR, "geocode_cache.json")


def save_offline_cache(data):
    with open(OFFLINE_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def load_offline_cache():
    if os.path.exists(OFFLINE_CACHE_FILE):
        with open(OFFLINE_CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# ================== GEOCODING ==================
try:
    with open(GEOCODE_CACHE_FILE, "r", encoding="utf-8") as f:
        geocode_cache = json.load(f)
except:
    geocode_cache = {}


def save_geocode_cache():
    with open(GEOCODE_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(geocode_cache, f, ensure_ascii=False)


geolocator = Nominatim(user_agent="epics_app")


def geocode_location(place):
    if not place:
        return None, None

    if place in geocode_cache:
        return geocode_cache[place]

    try:
        loc = geolocator.geocode(place)
        time.sleep(1)
        if loc:
            geocode_cache[place] = [loc.latitude, loc.longitude]
            save_geocode_cache()
            return loc.latitude, loc.longitude
    except:
        pass

    return None, None


# ================== SMS ALERT ==================
def send_sms_alert(phone_numbers, message):
    if not FAST2SMS_API_KEY or not phone_numbers:
        return {"error": "SMS configuration missing"}

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
        r = requests.post(
            "https://www.fast2sms.com/dev/bulkV2",
            data=payload,
            headers=headers,
            timeout=10
        )
        return r.json()
    except Exception as e:
        return {"error": str(e)}


# ================== FIRESTORE HELPERS ==================
def save_symptom_report(data):
    lat, lon = geocode_location(data["location"])
    data["lat"] = lat
    data["lon"] = lon
    db.collection("symptom_reports").add(data)


def load_symptom_reports_safe():
    try:
        reports = [doc.to_dict() for doc in db.collection("symptom_reports").stream()]
        save_offline_cache(reports)
        return reports, False
    except:
        return load_offline_cache(), True


def save_alert(alert):
    db.collection("alerts").add(alert)


def load_alerts_safe():
    try:
        alerts = [doc.to_dict() for doc in db.collection("alerts").stream()]
        return alerts, False
    except:
        return [], True


# ================== PDF EXPORT ==================
def export_alerts_pdf(alerts):
    file_path = "alerts_report.pdf"
    c = canvas.Canvas(file_path, pagesize=A4)

    y = A4[1] - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Health Alerts Report")

    c.setFont("Helvetica", 10)
    y -= 30

    for a in alerts:
        text = f"{a.get('timestamp','')} | {a.get('location','')} | {a.get('message','')}"
        c.drawString(40, y, text[:100])
        y -= 15
        if y < 50:
            c.showPage()
            y = A4[1] - 40

    c.save()
    return file_path


# ================== UI ==================
menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Symptom Report (ASHA)", "Geo-Heatmaps", "Alerts"]
)


if menu == "Home":
    st.header("Dashboard Overview")

    reports, offline = load_symptom_reports_safe()
    alerts, _ = load_alerts_safe()

    if offline:
        st.warning("Offline mode – showing cached data")

    st.metric("Total Reports", len(reports))
    st.metric("Total Alerts", len(alerts))

    st.success("PWA enabled | Offline cache active | SMS alerts enabled")


elif menu == "Symptom Report (ASHA)":
    with st.form("asha_form"):
        location = st.text_input("Location")
        symptoms = st.multiselect(
            "Symptoms",
            ["Fever", "Diarrhea", "Vomiting", "Rash", "Body pain"]
        )
        population = st.number_input("Population", min_value=1)
        submit = st.form_submit_button("Submit")

        if submit:
            record = {
                "location": location,
                "symptoms": symptoms,
                "population": population,
                "timestamp": datetime.now().isoformat()
            }

            save_symptom_report(record)

            reports, _ = load_symptom_reports_safe()
            loc_reports = [r for r in reports if r.get("location") == location]

            if len(loc_reports) >= SMS_ALERT_THRESHOLD:
                message = (
                    "Health Alert\n"
                    f"Location: {location}\n"
                    "Symptoms increasing.\n"
                    "Please take precautions."
                )

                sms_result = send_sms_alert(SMS_RECEIVERS, message)

                save_alert({
                    "location": location,
                    "message": message,
                    "timestamp": datetime.now().isoformat(),
                    "sms_status": sms_result
                })

                st.warning("SMS alert triggered")
                st.write("SMS response:", sms_result)

            st.success("Report saved successfully")


elif menu == "Geo-Heatmaps":
    reports, offline = load_symptom_reports_safe()

    if offline:
        st.warning("Offline mode – cached map")

    if reports:
        df = pd.DataFrame(reports)
        df = df[pd.notna(df["lat"]) & pd.notna(df["lon"])]

        if not df.empty:
            m = folium.Map(
                location=[df["lat"].mean(), df["lon"].mean()],
                zoom_start=10
            )

            for _, r in df.iterrows():
                folium.CircleMarker(
                    [r["lat"], r["lon"]],
                    radius=8,
                    color="red",
                    fill=True
                ).add_to(m)

            st_folium(m, width=1200, height=600)
        else:
            st.info("No valid geographic data available")


elif menu == "Alerts":
    alerts, offline = load_alerts_safe()

    if offline:
        st.warning("Offline mode – cached alerts")

    if alerts:
        st.dataframe(pd.DataFrame(alerts))
        if st.button("Export alerts as PDF"):
            pdf = export_alerts_pdf(alerts)
            with open(pdf, "rb") as f:
                st.download_button(
                    "Download PDF",
                    f,
                    file_name="alerts_report.pdf",
                    mime="application/pdf"
                )
    else:
        st.info("No alerts available")
