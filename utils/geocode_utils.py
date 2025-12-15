import os
import json
import time
from geopy.geocoders import Nominatim

# ---------------- CACHE SETUP ----------------
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

GEOCODE_CACHE_FILE = os.path.join(DATA_DIR, "geocode_cache.json")

try:
    with open(GEOCODE_CACHE_FILE, "r", encoding="utf-8") as f:
        geocode_cache = json.load(f)
except:
    geocode_cache = {}

geolocator = Nominatim(user_agent="epics_app")


def save_cache():
    with open(GEOCODE_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(geocode_cache, f, ensure_ascii=False)


# ---------------- MAIN FUNCTION ----------------
def geocode_location(place):
    """
    Returns (lat, lon)
    Never returns NaN values
    """

    if not place or not isinstance(place, str):
        return None, None

    # Use cache if available
    if place in geocode_cache:
        lat, lon = geocode_cache[place]
        return lat, lon

    try:
        loc = geolocator.geocode(place, timeout=10)
        time.sleep(1)

        if loc and loc.latitude and loc.longitude:
            lat, lon = float(loc.latitude), float(loc.longitude)
            geocode_cache[place] = [lat, lon]
            save_cache()
            return lat, lon

    except Exception:
        pass

    return None, None


# ---------------- ALIAS (DO NOT REMOVE) ----------------
# This avoids breaking any existing code
def get_lat_lon(place):
    return geocode_location(place)
