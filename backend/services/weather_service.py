import re

import requests
from decouple import config
from utils.cache import cache

from .destination_mapper import get_all_destinations

OPENWEATHER_API_KEY = config("OPENWEATHER_API_KEY")  # Store in .env for prod


@cache(ttl=3600)
def get_weather_forecast(location_name: str, units: str = "metric"):
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"

    def geocode(query):
        res = requests.get(
            geo_url,
            params={
                "q": query,
                "limit": 1,
                "appid": OPENWEATHER_API_KEY,
            },
        )
        data = res.json()
        return data[0] if data else None

    try:
        # Step 1: Try destination name
        geo = geocode(location_name)

        # Step 2: If fails, try fallback country (from mapping)
        if not geo:
            country_raw = get_country_for_destination(location_name)
            if country_raw:
                for country_part in re.split(r"[/,]", country_raw):
                    geo = geocode(country_part.strip())
                    if geo:
                        break

        if not geo:
            print(
                f"[ERROR] No geo data found for destination or country: {location_name}"
            )
            return []

        lat, lon = geo["lat"], geo["lon"]

        weather_res = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={
                "lat": lat,
                "lon": lon,
                "appid": OPENWEATHER_API_KEY,
                "units": units,
            },
        )

        weather_data = weather_res.json()

        forecast = []
        seen_dates = set()
        for entry in weather_data.get("list", []):
            date = entry["dt_txt"].split(" ")[0]
            if date not in seen_dates:
                forecast.append(
                    {
                        "date": entry["dt_txt"],
                        "temp": entry["main"]["temp"],
                        "humidity": entry["main"]["humidity"],
                        "icon": entry["weather"][0]["icon"],
                        "description": entry["weather"][0]["description"],
                    }
                )
                seen_dates.add(date)
        return forecast[:7]

    except Exception as e:
        print(f"[ERROR] Weather fetch failed: {e}")
        return []


def get_country_for_destination(dest_name: str) -> str:
    for dest in get_all_destinations():
        if dest["name"].strip().lower() == dest_name.strip().lower():
            return dest.get("country")
    return ""
