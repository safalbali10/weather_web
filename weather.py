import urllib.request
import json

# Your OpenWeatherMap API key
API_KEY = "d98b40ae53752993ac752a01d4fff840"

# Base URL for the current weather endpoint
# units=metric gives us Celsius temperatures
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    """
    Fetches current weather data for the given city from OpenWeatherMap.
    Returns a dictionary with temperature, humidity, condition, and feels-like temp.
    Returns None if the city is not found or something goes wrong.
    """
    # Build the full URL with query parameters
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"

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
