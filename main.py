import requests


def get_coordinates(city_name):
    """
    Finds the latitude and longitude for a given city name using Open-Meteo Geocoding.
    Returns (latitude, longitude, country_name) or None if not found.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = data.get("results")
        if not results:
            print(f"Error: Could not find coordinates for '{city_name}'.")
            return None

        first_match = results[0]
        latitude = first_match["latitude"]
        longitude = first_match["longitude"]
        country = first_match.get("country", "Unknown")

        return latitude, longitude, country

    except requests.exceptions.RequestException as e:
        print(f"Network error while searching for city: {e}")
        return None

def get_weather_condition(code):
    """
    Translates WMO weather interpretation codes to readable descriptions.
    """
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
    }
    return descriptions.get(code, "Unknown")


def get_weather(latitude, longitude):
    """
    Fetches current weather for the provided latitude and longitude.
    Returns a dictionary of current weather values or None if an error occurs.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("current")

    except requests.exceptions.RequestException as e:
        print(f"Network error while fetching weather data: {e}")
        return None
def main():
    print("=" * 35)
    print("       WEATHER CLI")
    print("=" * 35)

    city = input("Enter your city name: ").strip()
    if not city:
        print("City name cannot be empty.")
        return

    print(f"\nSearching for '{city}'...")
    coords = get_coordinates(city)
    if not coords:
        return

    latitude, longitude, country = coords
    print(f"Coordinates found: ({latitude}, {longitude}) in {country}")
    print("Fetching weather data...\n")

    weather = get_weather(latitude, longitude)
    if not weather:
        return

    temp = weather.get("temperature_2m")
    humidity = weather.get("relative_humidity_2m")
    wind_speed = weather.get("wind_speed_10m")
    condition = get_weather_condition(weather.get("weather_code"))

    print("-" * 35)
    print(f"Weather for: {city.title()}, {country}")
    print("-" * 35)
    print(f"Condition:    {condition}")
    print(f"Temperature:  {temp} °C")
    print(f"Humidity:     {humidity} %")
    print(f"Wind Speed:   {wind_speed} km/h")
    print("=" * 35)


if __name__ == "__main__":
    main()