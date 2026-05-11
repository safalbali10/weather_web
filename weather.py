import urllib.request
import urllib.parse
import json
import os

# Base URL for the current weather endpoint
# units=metric gives us Celsius temperatures
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


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

        # Fetch and display the weather
        weather = get_weather(city)
        if weather:
            display_weather(weather)


# Run the app only when this file is executed directly
if __name__ == "__main__":
    main()
