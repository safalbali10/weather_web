import urllib.request
import urllib.parse
import json
import os
from datetime import datetime

# Base URL for the current weather endpoint
# units=metric gives us Celsius temperatures
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# URL for the 5-day forecast endpoint (free plan gives 3-hourly data for 5 days)
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def load_env(filepath):
    """
    Reads a .env file and loads each KEY=VALUE line into os.environ.
    We do this manually so we don't need any third-party packages.
    Lines starting with # are comments and are ignored.
    """
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            # Skip blank lines and comments
            if not line or line.startswith("#"):
                continue
            # Split on the first '=' to get key and value
            key, _, value = line.partition("=")
            os.environ[key.strip()] = value.strip()


# Load the .env file that lives in the same folder as this script
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_env(env_path)

# Read the API key from the environment — never hardcoded in the source code
API_KEY = os.environ.get("OPENWEATHER_API_KEY")


def get_weather(city):
    """
    Fetches current weather data for the given city from OpenWeatherMap.
    Returns a dictionary with temperature, humidity, condition, and feels-like temp.
    Returns None if the city is not found or something goes wrong.
    """
    # Stop early with a helpful message if the API key wasn't loaded
    if not API_KEY:
        print("  Error: OPENWEATHER_API_KEY not found in .env file.")
        return None

    # URL-encode the city name so spaces become %20 (e.g. "new york" → "new+york")
    # Without this, spaces in the URL cause a crash
    encoded_city = urllib.parse.quote_plus(city)
    url = f"{BASE_URL}?q={encoded_city}&appid={API_KEY}&units=metric"

    try:
        # Make the HTTP request and read the response
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        # Pull out the fields we care about from the JSON response
        temperature = data["main"]["temp"]          # Current temperature in Celsius
        feels_like = data["main"]["feels_like"]     # Feels like temperature in Celsius
        humidity = data["main"]["humidity"]          # Humidity percentage
        condition = data["weather"][0]["description"]  # e.g. "clear sky", "light rain"
        city_name = data["name"]                    # City name as returned by the API
        country = data["sys"]["country"]            # Country code, e.g. "US", "IN"

        return {
            "city": city_name,
            "country": country,
            "temperature": temperature,
            "feels_like": feels_like,
            "humidity": humidity,
            "condition": condition,
        }

    except urllib.error.HTTPError as e:
        # 404 means city not found; other codes mean something else went wrong
        if e.code == 404:
            print(f"  City '{city}' not found. Please check the spelling and try again.")
        else:
            print(f"  HTTP error {e.code}: {e.reason}")
        return None

    except urllib.error.URLError:
        # This happens if there is no internet connection
        print("  Could not connect to the internet. Please check your connection.")
        return None


def get_forecast(city):
    """
    Fetches a 5-day weather forecast for the given city from OpenWeatherMap.
    The free API gives one reading every 3 hours for 5 days (40 readings total).
    We group those by day and return one entry per day showing:
      - the day name and date
      - the highest and lowest temperatures that day
      - the weather condition at noon (or the closest reading to noon)
    Returns a list of daily dicts, or None if something goes wrong.
    """
    if not API_KEY:
        return None

    encoded_city = urllib.parse.quote_plus(city)
    url = f"{FORECAST_URL}?q={encoded_city}&appid={API_KEY}&units=metric"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        # Group the 3-hourly entries by date (e.g. "2025-05-13")
        days = {}
        for entry in data["list"]:
            date_str = entry["dt_txt"].split(" ")[0]
            if date_str not in days:
                days[date_str] = []
            days[date_str].append(entry)

        forecast = []
        today_str = datetime.now().strftime("%Y-%m-%d")

        for date_str in sorted(days.keys()):
            # Skip today — current conditions are already shown above
            if date_str == today_str:
                continue

            entries = days[date_str]

            # Find the highest and lowest temperature across all entries for this day
            temps = [e["main"]["temp"] for e in entries]
            temp_high = max(temps)
            temp_low  = min(temps)

            # Use the entry closest to noon for the weather description
            noon_entry = min(
                entries,
                key=lambda e: abs(int(e["dt_txt"].split(" ")[1].split(":")[0]) - 12)
            )
            condition = noon_entry["weather"][0]["description"]

            # Format the date as a readable day name + short date
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            day_name = date_obj.strftime("%A")    # e.g. "Monday"
            day_date = date_obj.strftime("%b %d") # e.g. "May 13"

            forecast.append({
                "day_name":  day_name,
                "day_date":  day_date,
                "temp_high": temp_high,
                "temp_low":  temp_low,
                "condition": condition,
            })

        return forecast

    except (urllib.error.URLError, KeyError):
        return None


def display_weather(weather):
    """
    Prints the weather information in a clean, readable format.
    """
    print()
    print(f"  Weather in {weather['city']}, {weather['country']}")
    print(f"  {'─' * 30}")
    print(f"  Condition   : {weather['condition'].capitalize()}")
    print(f"  Temperature : {weather['temperature']:.1f} °C")
    print(f"  Feels Like  : {weather['feels_like']:.1f} °C")
    print(f"  Humidity    : {weather['humidity']}%")
    print()


def display_forecast(forecast):
    """
    Prints the 5-day forecast in a simple table format.
    Each row shows the day name, date, high/low temps, and weather condition.
    """
    print(f"  {'─' * 55}")
    print(f"  {'5-Day Forecast':^55}")
    print(f"  {'─' * 55}")
    print(f"  {'Day':<12} {'Date':<10} {'High':>6} {'Low':>6}  Condition")
    print(f"  {'─' * 55}")

    for day in forecast:
        print(
            f"  {day['day_name']:<12} {day['day_date']:<10} "
            f"{day['temp_high']:>5.1f}° {day['temp_low']:>5.1f}°  {day['condition'].capitalize()}"
        )

    print(f"  {'─' * 55}")
    print()


def main():
    """
    Main loop — asks the user for a city name, fetches and displays the weather,
    then asks if they want to check another city.
    """
    print("╔══════════════════════════════╗")
    print("║       Weather App            ║")
    print("╚══════════════════════════════╝")

    while True:
        # Ask the user for a city name
        city = input("\nEnter city name (or 'quit' to exit): ").strip()

        # Exit if the user types 'quit' or leaves it blank
        if city.lower() in ("quit", "q", "exit", ""):
            print("\nGoodbye!")
            break

        # Fetch and display the current weather
        weather = get_weather(city)
        if weather:
            display_weather(weather)

            # Fetch and display the 5-day forecast
            forecast = get_forecast(city)
            if forecast:
                display_forecast(forecast)


# Run the app only when this file is executed directly
if __name__ == "__main__":
    main()
