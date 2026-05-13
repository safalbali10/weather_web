"""
Flask Weather Web App
Shows current weather and a 5-day forecast for any city using the OpenWeatherMap API.
"""

import os
import requests
from datetime import datetime
from flask import Flask, render_template, request
from dotenv import load_dotenv

# Load API key from the .env file in the same folder
load_dotenv()

app = Flask(__name__)

@app.route('/debug')
@app.route('/debug/<city>')
def debug(city="London"):
    """
    Diagnostic page — visit /debug or /debug/YourCity on Railway to see:
    - whether the API key is loaded
    - whether the current weather call works
    - whether the forecast call works, and how many days it returns
    This makes it easy to spot what's failing without reading server logs.
    """
    api_key_loaded = bool(os.getenv("OPENWEATHER_API_KEY"))
    weather, weather_err = get_weather(city)
    forecast = get_forecast(city)
    return (
        f"API key loaded : {api_key_loaded}\n"
        f"Weather result : {weather if weather else weather_err}\n"
        f"Forecast days  : {len(forecast) if forecast else 0}  →  {forecast}\n"
    ), 200, {"Content-Type": "text/plain"}

# OpenWeatherMap API URLs
API_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Maps weather condition codes to emoji icons
WEATHER_ICONS = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Smoke": "🌫️",
    "Haze": "🌫️",
    "Fog": "🌫️",
    "Tornado": "🌪️",
}


def get_forecast(city):
    """
    Fetches a 5-day weather forecast for a city from OpenWeatherMap.
    The free API returns one entry every 3 hours for 5 days.
    We group those entries by day and pick the high temp, low temp,
    and the condition closest to noon for each day.
    Returns a list of daily forecast dicts, or None on error.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=5)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        data = response.json()

        # Group the 3-hourly forecast entries by calendar date
        # Each entry has a "dt_txt" like "2025-05-13 12:00:00"
        days = {}
        for entry in data["list"]:
            date_str = entry["dt_txt"].split(" ")[0]   # e.g. "2025-05-13"
            if date_str not in days:
                days[date_str] = []
            days[date_str].append(entry)

        forecast = []
        today_str = datetime.now().strftime("%Y-%m-%d")

        for date_str in sorted(days.keys()):
            # Skip today — we already show current conditions at the top
            if date_str == today_str:
                continue

            entries = days[date_str]

            # Find the highest and lowest temperatures across all entries for this day
            temps = [e["main"]["temp"] for e in entries]
            temp_high = round(max(temps))
            temp_low  = round(min(temps))

            # Use the entry closest to noon for the icon and condition description
            noon_entry = min(
                entries,
                key=lambda e: abs(int(e["dt_txt"].split(" ")[1].split(":")[0]) - 12)
            )
            condition_main = noon_entry["weather"][0]["main"]
            condition      = noon_entry["weather"][0]["description"].title()
            icon           = WEATHER_ICONS.get(condition_main, "🌡️")

            # Convert the date string to a human-readable day name and short date
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            day_name = date_obj.strftime("%A")    # e.g. "Monday"
            day_date = date_obj.strftime("%b %d") # e.g. "May 13"

            forecast.append({
                "day_name":  day_name,
                "day_date":  day_date,
                "temp_high": temp_high,
                "temp_low":  temp_low,
                "condition": condition,
                "icon":      icon,
            })

        return forecast

    except Exception as e:
        # Log the actual error so it shows up in Railway's deployment logs.
        # Previously this was a silent return None — that made it impossible to
        # diagnose failures on the server.
        print(f"[get_forecast] ERROR for city '{city}': {type(e).__name__}: {e}")
        return None


def get_weather(city):
    """
    Fetches current weather data for a given city from OpenWeatherMap.
    Returns a dictionary with weather info, or None if the city wasn't found.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")

    # Build the request with metric units (Celsius)
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    try:
        response = requests.get(API_URL, params=params, timeout=5)

        # 404 means city not found; any other error is unexpected
        if response.status_code == 404:
            return None, "City not found. Please check the spelling and try again."

        response.raise_for_status()
        data = response.json()

        # Pull out the fields we want to display
        condition = data["weather"][0]["main"]
        weather = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"].title(),
            "condition_main": condition,
            "icon": WEATHER_ICONS.get(condition, "🌡️"),
            "wind_speed": round(data["wind"]["speed"] * 3.6),  # m/s → km/h
        }
        return weather, None

    except requests.exceptions.Timeout:
        return None, "Request timed out. Please try again."
    except requests.exceptions.RequestException:
        return None, "Could not reach the weather service. Please try again later."


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main page — handles both the empty search page (GET)
    and the weather result after the user submits a city (POST).
    Also fetches the 5-day forecast when weather data is found.
    """
    weather = None
    forecast = None
    error = None
    city_query = ""

    if request.method == "POST":
        city_query = request.form.get("city", "").strip()
        if city_query:
            weather, error = get_weather(city_query)
            # Only fetch the forecast if current weather was found successfully
            if weather:
                forecast = get_forecast(city_query)
        else:
            error = "Please enter a city name."

    return render_template("index.html", weather=weather, forecast=forecast, error=error, city_query=city_query)


if __name__ == "__main__":
    # Use Railway's PORT env var in production, fall back to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
