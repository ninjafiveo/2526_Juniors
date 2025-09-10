#!/usr/bin/env python3
"""
Simple NWS 7-day forecast CLI
- Input: ZIP code or "city, state"
- Output: Text 7-day forecast from api.weather.gov

Dependencies: requests, geopy
  pip install requests geopy
"""

import sys
import time
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable, GeocoderServiceError, GeocoderTimedOut

# IMPORTANT: Set a real contact address per NWS API policy:
CONTACT_EMAIL = "you@example.com"   # <-- put your contact email here
USER_AGENT = f"nws-7day-cli/1.0 ({CONTACT_EMAIL})"

REQ_TIMEOUT = 12  # seconds

def geocode(query: str):
    """Return (lat, lon, display_name) using Nominatim."""
    geolocator = Nominatim(user_agent="nws_7day_cli_geocoder")
    try:
        # Try as given first
        loc = geolocator.geocode(query, addressdetails=True, timeout=REQ_TIMEOUT)
        # If that failed, try appending 'USA'
        if not loc:
            loc = geolocator.geocode(f"{query}, USA", addressdetails=True, timeout=REQ_TIMEOUT)
        if not loc:
            return None
        return (loc.latitude, loc.longitude, loc.address)
    except (GeocoderUnavailable, GeocoderServiceError, GeocoderTimedOut):
        return None


def get_points_metadata(lat: float, lon: float):
    """Call api.weather.gov/points/{lat},{lon} and return JSON or None."""
    url = f"https://api.weather.gov/points/{lat:.4f},{lon:.4f}"
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT, "Accept": "application/geo+json"},
                         timeout=REQ_TIMEOUT)
        if r.status_code == 429:
            # Rate limit—brief backoff and retry once
            time.sleep(1.0)
            r = requests.get(url, headers={"User-Agent": USER_AGENT, "Accept": "application/geo+json"},
                             timeout=REQ_TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return None


def get_forecast(forecast_url: str):
    """Fetch the 7-day forecast periods JSON from the provided forecast URL."""
    try:
        r = requests.get(forecast_url, headers={"User-Agent": USER_AGENT, "Accept": "application/geo+json"},
                         timeout=REQ_TIMEOUT)
        if r.status_code == 429:
            time.sleep(1.0)
            r = requests.get(forecast_url, headers={"User-Agent": USER_AGENT, "Accept": "application/geo+json"},
                             timeout=REQ_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        periods = data.get("properties", {}).get("periods", [])
        return periods
    except requests.RequestException:
        return None


def pretty_location(points_json, fallback_display: str) -> str:
    """Try to produce a nice 'City, ST' from NWS points JSON; fallback to geocoder display."""
    try:
        rel = points_json["properties"]["relativeLocation"]["properties"]
        city = rel.get("city")
        state = rel.get("state")
        if city and state:
            return f"{city}, {state}"
    except Exception:
        pass
    return fallback_display


def print_forecast(location_label: str, periods):
    """Print a readable forecast table."""
    if not periods:
        print("No forecast data available.")
        return

    print(f"\n7-Day Forecast for {location_label}")
    print("-" * (len(location_label) + 22))

    # NWS usually provides ~14 half-day periods (day/night). We'll show all provided.
    for p in periods:
        name = p.get("name", "Period")
        detailed = p.get("detailedForecast") or p.get("shortForecast") or ""
        temp = p.get("temperature")
        unit = p.get("temperatureUnit", "")
        wind = f"{p.get('windDirection','')}".strip()
        wind_speed = p.get("windSpeed", "")
        wind_str = f"{wind} {wind_speed}".strip()

        bits = []
        if temp is not None and unit:
            bits.append(f"{temp}°{unit}")
        if wind_str:
            bits.append(f"Wind: {wind_str}")
        header = f"{name} — " + " | ".join(bits) if bits else name

        print(f"\n{header}")
        print(detailed)


def main():
    print("NWS 7-Day Forecast")
    print("------------------")
    query = input("Enter ZIP code or 'city, state' (e.g., 44512 or 'Youngstown, OH'): ").strip()
    if not query:
        print("No input provided. Exiting.")
        sys.exit(1)

    # 1) Geocode
    geocoded = geocode(query)
    if not geocoded:
        print("Sorry, I couldn't determine that location. Please try a different ZIP or 'city, state'.")
        sys.exit(2)

    lat, lon, display = geocoded

    # 2) Get NWS 'points' metadata (contains forecast URL and a nice location label)
    points = get_points_metadata(lat, lon)
    if not points:
        print("Couldn't reach NWS 'points' service. Check your internet connection and try again.")
        sys.exit(3)

    forecast_url = points.get("properties", {}).get("forecast")
    if not forecast_url:
        print("NWS did not provide a forecast URL for this location.")
        sys.exit(4)

    # 3) Fetch forecast
    periods = get_forecast(forecast_url)
    if periods is None:
        print("Couldn't fetch the forecast from NWS. Try again shortly.")
        sys.exit(5)

    # 4) Print
    loc_label = pretty_location(points, display)
    print_forecast(loc_label, periods)


if __name__ == "__main__":
    main()
