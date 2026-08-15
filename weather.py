import requests
import os
from dotenv import load_dotenv
import argparse


load_dotenv()
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
if not OPENWEATHER_API_KEY:
    raise RuntimeError(
        "OPENWEATHER_API_KEY environment variable not set.\n"
        "Create a .env file with OPENWEATHER_API_KEY=your_api_key or set the variable in your environment."
    )

BASE_GEOCODING_API_URL = "http://api.openweathermap.org/geo/1.0/direct"
BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"


def read_user_cli_args():
    """Handles the CLI user interactions.

    Returns:
        argparse.Namespace: Populated namespace object
    """
    parser = argparse.ArgumentParser(
        description="gets weather informations for a city"
    )
    parser.add_argument(
        "city",
        nargs="*",
        type=str,
        help='enter the city name; if the name contains an apostrophe, you can also type it at the prompt when no city is provided',
    )
    parser.add_argument(
        "-i",
        "--imperial",
        action="store_true",
        help="display the temperature in imperial units",
    )
    return parser.parse_args()


def get_geocoding(city, limit=3):
    """Get latitude and longitude for a city name.

    Returns a tuple (lat, lon).
    """
    payload = {'q': city, 'limit': limit, 'appid': OPENWEATHER_API_KEY}
    response = requests.get(BASE_GEOCODING_API_URL, params=payload)
    response.raise_for_status()
    geo_data = response.json()

    if not geo_data:
        raise ValueError(f"City not found: {city!r}")

    # Single match: return coordinates as a tuple
    if len(geo_data) == 1:
        location = geo_data[0]
        return location['lat'], location['lon']

    # Multiple matches: let the user choose
    return _prompt_user_choice(geo_data)


def _prompt_user_choice(locations):
    """Prompt the user to choose from multiple location matches.

    Returns a tuple (lat, lon).
    """
    print("Multiple locations found:")
    for i, loc in enumerate(locations, 1):
        name = loc.get('name', 'Unknown')
        state = loc.get('state')
        country = loc.get('country', 'Unknown')
        location_str = f"{name}, {state}, {country}" if state else f"{name}, {country}"
        print(f"  {i}. {location_str}")

    while True:
        try:
            choice = int(input(f"Enter a number (1-{len(locations)}): "))
            if 1 <= choice <= len(locations):
                loc = locations[choice - 1]
                return loc['lat'], loc['lon']
            print(f"Please enter a number between 1 and {len(locations)}")
        except ValueError:
            print("Please enter a valid number")

def get_weather_data(lat, lon, imperial=False):
    """Request current weather for the given coordinates and return the parsed JSON.

    Args:
        lat (float): Latitude
        lon (float): Longitude
        imperial (bool): Use imperial units when True, metric otherwise

    Returns:
        dict: Weather API response
    """
    units = "imperial" if imperial else "metric"
    params = {"lat": lat, "lon": lon, "units": units, "appid": OPENWEATHER_API_KEY}
    response = requests.get(BASE_WEATHER_API_URL, params=params)
    response.raise_for_status()
    return response.json()

def display_weather_info(weather_data, imperial=False):
    """Print formatted weather information about a city."""
    city_name = weather_data.get("name", "Unknown")
    country = weather_data.get("sys", {}).get("country", "Unknown")
    temp = weather_data.get("main", {}).get("temp")
    temp_feel = weather_data.get("main", {}).get("feels_like")
    description = weather_data.get("weather", [{}])[0].get("description", "Unknown")

    unit = "°F" if imperial else "°C"

    def fmt(value):
        if isinstance(value, (int, float)):
            return f"{value:.1f}"
        return str(value) if value is not None else "N/A"

    print(f"{city_name}, {country}: {fmt(temp)}{unit} (feels like: {fmt(temp_feel)}), {description}")

def main():
    user_args = read_user_cli_args()

    if not user_args.city:
        city = input("Enter city name: ").strip()
        if not city:
            raise SystemExit("City name cannot be empty.")
    else:
        city = " ".join(user_args.city)

    lat, lon = get_geocoding(city)
    print(f"Selected location: lat {lat}, lon {lon}")
    weather_data = get_weather_data(lat, lon, user_args.imperial)
    display_weather_info(weather_data, user_args.imperial)

if __name__ == "__main__":
    main()
