import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

def get_db():
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["FIREBASE_KEY"]))
        firebase_admin.initialize_app(cred)

    return firestore.client()

db = get_db()


def save_report(location, disease, risk, symptoms, lat, lon, population=1, timestamp=None, date=None):
    db.collection("symptom_reports").add({
        "Date": date,
        "Location": location,
        "Disease": disease,
        "Risk": risk,
        "Symptoms": symptoms,
        "lat": lat,
        "lon": lon,
        "population": population
    })


def load_reports():
    return [doc.to_dict() for doc in db.collection("symptom_reports").stream()]


def delete_old_reports(days=30):
    cutoff_date = datetime.now() - timedelta(days=days)
    reports_ref = db.collection("reports")

    deleted = 0
    for doc in reports_ref.stream():
        data = doc.to_dict()
        try:
            report_date = datetime.strptime(data.get("date"), "%Y-%m-%d")
            if report_date < cutoff_date:
                reports_ref.document(doc.id).delete()
                deleted += 1
        except:
            continue

    return deleted
