import requests
from decouple import config
from utils.cache import cache

OPENWEATHER_API_KEY = config("OPENWEATHER_API_KEY")  # Store in .env for prod


@cache(ttl=3600)
def get_weather_forecast(destination_name: str, units: str = "metric"):
    # Step 1: Get lat/lon from destination name
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    geo_params = {
        "q": destination_name,
        "limit": 1,
        "appid": OPENWEATHER_API_KEY,
    }

    try:
        geo_res = requests.get(geo_url, params=geo_params)
        geo_data = geo_res.json()

        if not geo_data:
            print(f"[WARN] Could not find geolocation for {destination_name}")
            return generate_empty_weather()

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]

        # Step 2: Fetch weather using lat/lon
        weather_url = "https://api.openweathermap.org/data/2.5/forecast"
        weather_params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": units,
        }

        weather_res = requests.get(weather_url, params=weather_params)
        weather_data = weather_res.json()

        forecast = []
        seen_dates = set()

        for entry in weather_data.get("list", []):
            dt = entry["dt_txt"]
            date = dt.split(" ")[0]

            if date not in seen_dates:
                forecast.append(
                    {
                        "date": dt,
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
        return generate_empty_weather()


def generate_empty_weather():
    return []
