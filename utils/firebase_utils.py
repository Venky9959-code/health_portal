import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["FIREBASE_KEY"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()


def save_report(date, location, disease, risk, symptoms, lat=None, lon=None):
    db.collection("symptom_reports").add({
        "Date": date,
        "Location": location,
        "Disease": disease,
        "Risk": risk,
        "Symptoms": symptoms,
        "lat": lat,
        "lon": lon
    })


def load_reports():
    return [doc.to_dict() for doc in db.collection("symptom_reports").stream()]



def delete_old_reports(days=30):
    cutoff_date = datetime.now() - timedelta(days=days)

    reports_ref = db.collection("reports")
    docs = reports_ref.stream()

    deleted = 0

    for doc in docs:
        data = doc.to_dict()
        try:
            report_date = datetime.strptime(data.get("date"), "%Y-%m-%d")
            if report_date < cutoff_date:
                reports_ref.document(doc.id).delete()
                deleted += 1
        except:
            continue

    return deleted

