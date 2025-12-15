import streamlit as st
from utils.firebase_utils import save_report
from utils.geocode_utils import get_lat_lon
from utils.page_refresh import page_refresh_button
from utils.sms_utils import send_sms
from datetime import datetime
from geopy.geocoders import Nominatim
import time


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

    # ---------- SYMPTOMS ----------
    symptoms = st.multiselect(
        "Select Symptoms",
        ["Fever", "Diarrhea", "Vomiting", "Rash", "Body pain"]
    )

    population = st.number_input("Affected Population", min_value=1, step=1)

    # ---------- SUBMIT ----------
    if st.button("🔮 Predict Disease Risk"):
        if not location or not symptoms:
            st.warning("Please select location and symptoms.")
            return

        disease, risk = predict_disease(symptoms)

        st.success(f"🦠 Most Likely Disease: **{disease}**")
        st.warning(f"⚠ Risk Level: **{risk}**")

        lat, lon = get_lat_lon(location)

        save_report(
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            location=location,
            disease=disease,
            risk=risk,
            symptoms=symptoms,
            lat=lat,
            lon=lon
        )
        # ---------- SMS ALERT ----------
        if risk == "High":
            send_sms(
                ["919959826841"],
                f"🚨 HIGH RISK ALERT\nDisease: {disease}\nLocation: {location}"
            )
            st.error("🚨 High risk detected – SMS alert sent")

        st.success("✅ Report saved and reflected in Reports & Geo Heatmap")
        page_refresh_button("🔄 Refresh Form")
