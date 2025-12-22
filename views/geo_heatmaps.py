import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from utils.firebase_utils import load_reports
from utils.page_refresh import page_refresh_button


# ---------------- AUTO FOCUS LOGIC ----------------
def get_focus_location(df):
    high = df[df["Risk"].str.lower() == "high"]
    medium = df[df["Risk"].str.lower() == "medium"]

    if not high.empty:
        return high["lat"].mean(), high["lon"].mean(), 9
    elif not medium.empty:
        return medium["lat"].mean(), medium["lon"].mean(), 8
    else:
        return df["lat"].mean(), df["lon"].mean(), 7


# ---------------- RISK → COLOR ----------------
def risk_color(risk):
    risk = str(risk).lower()
    if risk == "high":
        return "red"
    elif risk == "medium":
        return "orange"
    return "green"


# ---------------- POPULATION NORMALIZED RADIUS ----------------
def risk_radius(risk, population=1):
    risk = str(risk).lower()
    base = 7

    if risk == "high":
        base = 14
    elif risk == "medium":
        base = 10

    # population normalization (log safe)
    try:
        population = max(int(population), 1)
        return min(base + (population ** 0.5), 25)
    except:
        return base


def show_geo_heatmaps():
    st.header("🗺️ Geo Risk Map")
    page_refresh_button("🔄 Refresh Map")

    # ---------------- BLINK CSS ----------------
    st.markdown("""
    <style>
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.3; }
        100% { opacity: 1; }
    }
    .blink-marker {
        animation: blink 1s infinite;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- LOAD REPORTS ----------------
    reports = load_reports()

    # include forecasted data if exists
    if "last_forecast" in st.session_state and st.session_state.last_forecast is not None:
        forecast_df = st.session_state.last_forecast.copy()
        forecast_df["Risk"] = "Medium"
        forecast_df["location"] = "Forecasted Region"
        forecast_df["lat"] = None
        forecast_df["lon"] = None
        forecast_df["population"] = 1
        forecast_df["timestamp"] = "Forecast"
        reports += forecast_df.to_dict("records")

    if not reports:
        st.info("No reports available yet.")
        return

    df = pd.DataFrame(reports)

    # ---------------- SESSION ALERT FLAG ----------------
    if "high_alert_shown" not in st.session_state:
        st.session_state.high_alert_shown = False

    # ---------------- SAFETY CHECKS ----------------
    for col in ["lat", "lon"]:
        if col not in df.columns:
            st.warning("Geographic data not available.")
            return

    df = df.dropna(subset=["lat", "lon"])

    if "risk" in df.columns and "Risk" not in df.columns:
        df.rename(columns={"risk": "Risk"}, inplace=True)

    if "Risk" not in df.columns:
        df["Risk"] = "Low"

    if "population" not in df.columns:
        df["population"] = 1

    if "date" in df.columns and "timestamp" not in df.columns:
        df.rename(columns={"date": "timestamp"}, inplace=True)

    if "timestamp" not in df.columns:
        df["timestamp"] = "-"

    # ---------------- AUTO HIGH RISK ALERT ----------------
    high_count = df[df["Risk"].str.lower() == "high"].shape[0]

    if high_count > 0 and not st.session_state.high_alert_shown:
        st.session_state.high_alert_shown = True
        st.error(f"🚨 ALERT: {high_count} HIGH RISK locations detected!")

    # ---------------- AUTO FOCUS ----------------
    focus_lat, focus_lon, zoom = get_focus_location(df)

    m = folium.Map(
        location=[focus_lat, focus_lon],
        zoom_start=zoom,
        tiles="OpenStreetMap"
    )

    # ---------------- MARKERS ----------------
    for _, row in df.iterrows():
        risk = str(row["Risk"]).lower()
        color = risk_color(risk)
        css_class = "blink-marker" if risk == "high" else ""

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=risk_radius(row["Risk"], row.get("population", 1)),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=(
                f"<b>Location:</b> {row.get('location','-')}<br>"
                f"<b>Disease:</b> {row.get('disease','-')}<br>"
                f"<b>Risk:</b> {row.get('Risk','-')}<br>"
                f"<b>Population:</b> {row.get('population','-')}<br>"
                f"<b>Time:</b> {row.get('timestamp','-')}"
            ),
            class_name=css_class
        ).add_to(m)

    # ---------------- RENDER MAP ----------------
    st_folium(m, width=1200, height=600)

    # ---------------- LEGEND ----------------
    st.markdown("""
    ### 🗺️ Risk Legend
    - 🟢 **Low Risk**
    - 🟠 **Medium Risk**
    - 🔴 **High Risk (Blinking)**
    """)
