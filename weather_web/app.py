"""
Flask Weather Web App
Shows current weather for any city using the OpenWeatherMap API.
"""

import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

# Load API key from the .env file in the same folder
load_dotenv()

app = Flask(__name__)

# OpenWeatherMap API base URL
API_URL = "https://api.openweathermap.org/data/2.5/weather"

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
    """
    weather = None
    error = None
    city_query = ""

    if request.method == "POST":
        city_query = request.form.get("city", "").strip()
        if city_query:
            weather, error = get_weather(city_query)
        else:
            error = "Please enter a city name."

    return render_template("index.html", weather=weather, error=error, city_query=city_query)


if __name__ == "__main__":
    # Debug mode is fine for local development
    app.run(debug=True, port=5000)
