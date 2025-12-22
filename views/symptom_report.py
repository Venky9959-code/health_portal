import streamlit as st
from utils.firebase_utils import save_report, load_reports
from utils.geocode_utils import get_lat_lon
from utils.page_refresh import page_refresh_button
from utils.sms_utils import send_sms
from datetime import datetime
from geopy.geocoders import Nominatim
import time
from utils.auth_guard import require_login

require_login()

# ---------------- DISEASE RULES (UNCHANGED) ----------------
DISEASE_RULES = {
    "Dengue": ["Fever", "Body pain", "Rash"],
    "Malaria": ["Fever", "Vomiting"],
    "Diarrhea": ["Diarrhea", "Vomiting"],
    "Viral Fever": ["Fever"]
}


def predict_disease(symptoms):
    scores = {}

    for disease, rules in DISEASE_RULES.items():
        scores[disease] = len(set(symptoms) & set(rules))

    predicted = max(scores, key=scores.get)

    if scores[predicted] >= 3:
        risk = "High"
    elif scores[predicted] == 2:
        risk = "Medium"
    else:
        risk = "Low"

    return predicted, risk


# ---------------- ONLINE LOCATION SEARCH ----------------
geolocator = Nominatim(user_agent="epics_health_app")


def search_locations(query):
    try:
        results = geolocator.geocode(
            query,
            exactly_one=False,
            limit=6,
            addressdetails=True
        )
        time.sleep(1)
        if results:
            return [r.address for r in results]
    except:
        pass
    return []


# ---------------- MAIN VIEW ----------------
def show_symptom_report():

    # ---------- UI FIX (WHITE HEALTH LAYOUT ONLY) ----------
    st.markdown("""
    <style>

    /* ================= FORCE LIGHT BACKGROUND EVERYWHERE ================= */

    div[data-baseweb="popover"],
    div[role="listbox"],
    div[role="option"] {
        background-color: #ffffff !important;
        color: #111827 !important;
    }

    div[role="option"]:hover {
        background-color: #f1f5f9 !important;
    }

    div[role="presentation"],
    div[data-baseweb="layer"] {
        background: transparent !important;
    }

    .ag-root,
    .ag-root-wrapper,
    .ag-theme-streamlit,
    .ag-body-viewport,
    .ag-center-cols-viewport {
        background-color: #ffffff !important;
    }

    .ag-header {
        background-color: #f9fafb !important;
    }

    .ag-row {
        background-color: #ffffff !important;
    }

    .ag-row-even {
        background-color: #f9fafb !important;
    }

    body, html {
        background-color: #f8f9fb !important;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------- ACCESS CHECK ----------------
    if st.session_state.user_role != "asha":
        st.error("🚫 Access denied. ASHA users only.")
        return

    st.header("🩺 Symptom Based Disease Prediction")

    # ---------- LOCATION ----------
    location_query = st.text_input("🔍 Search Location (Village / City / Area)")

    location_options = []
    if location_query:
        location_options = search_locations(location_query)

    if location_options:
        location = st.selectbox("📍 Select Location", location_options)
    else:
        location = location_query

    # ---------- INPUTS ----------
    age_group = st.selectbox(
        "Age Group",
        ["0–10", "11–20", "21–40", "41–60", "60+"]
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"]
    )

    symptoms = st.multiselect(
        "Select Symptoms",
        ["Fever", "Diarrhea", "Vomiting", "Rash", "Body pain"]
    )

    population = st.number_input(
        "Affected Population",
        min_value=1,
        step=1
    )

    notes = st.text_area("Notes (optional)")

    # ---------- SUBMIT ----------
    if st.button("🔮 Predict Disease Risk"):

        if not location or not symptoms:
            st.warning("Please select location and symptoms.")
            return

        disease, risk = predict_disease(symptoms)

        st.success(f"🦠 Most Likely Disease: **{disease}**")
        st.warning(f"⚠ Risk Level: **{risk}**")

        lat, lon = get_lat_lon(location)

        # ---------- SAVE REPORT ----------
        save_report(
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            location=location,
            disease=disease,
            risk=risk,
            symptoms=symptoms,
            lat=lat,
            lon=lon,
            population=population
        )

        # ---------- SMS ALERT ----------
        if risk == "High":

            alert_message = f"""
🚨 HIGH RISK DISEASE ALERT 🚨

Disease : {disease}
Risk    : HIGH
Location: {location}
Time    : {datetime.now().strftime('%d-%m-%Y %H:%M')}

Immediate attention required.
— Health System
""".strip()

            recipients = [
                "+919959826841"
            ]

            sms_result = send_sms(recipients, alert_message)

            failed = [r for r in sms_result if "error" in r]
            sent = [r for r in sms_result if "sid" in r]

            if sent and not failed:
                st.error("🚨 High risk detected — WhatsApp alert sent successfully")

            elif sent and failed:
                st.warning("⚠ High risk detected — WhatsApp sent to some numbers, failed for others.")

            else:
                st.warning("⚠ High risk detected — WhatsApp alert failed.")


    # ---------- RECENT REPORTS ----------
    st.subheader("🕒 Recent Reports")

    reports = load_reports()
    if reports:
        recent = reports[-5:]
        st.dataframe(recent, use_container_width=True)
    else:
        st.info("No reports submitted yet.")
