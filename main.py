
import requests, re, json

"""
Weather Advisor
A command-line weather advisor using Open-Meteo APIs.
"""

# API Endpoints
GEOCODING_BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_BASE_URL = "https://api.open-meteo.com/v1/forecast"
CACHE_FILE = "locations_cache.json"

def load_cache():
    try: 
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_to_cache(city_input: str, location_data: dict):
    cache = load_cache()
    cache[city_input] = location_data
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def give_weather_advice(weather: dict):
    feels_like = weather.get("apparent_temperature", 0)
    wind_speed = weather.get("wind_speed_10m", 0)
    weather_code = weather.get("weather_code", 0)

    match weather_code:
        case 0 | 1:
            condition_category = "clear"
        case 2 | 3:
            condition_category = "cloudy"
        case 45 | 48:
            condition_category = "foggy"
        case 51 | 53 | 55 | 61 | 63 | 65 | 80 | 81 | 82:
            condition_category = "rain"
        case 71 | 73 | 75 | 77 | 85 | 86:
            condition_category = "snow"
        case 95 | 96 | 99:
            condition_category = "storm"
        case _:
            condition_category = "other"

    match condition_category:
        case "clear":
            print("Skies are clear! Great day to spend time outdoors.")
        case "cloudy":
            print("Cloudy skies. Good weather for outdoor activities!")
        case "foggy":
            print("Reduced visibility due to fog. Drive carefully.")
        case "rain":
            print("Wet conditions. Grab an umbrella or rain jacket on the way out!")
        case "snow":
            print("It's snowing. Dress warm and have fun!")
        case "storm":
            print("\U0001F6A8 Severe storm warning!")
            print("Avoid outdoor activities and stay inside.")
        case _:
            print("Check local weather alerts")

    if feels_like < 32:
        print("Freezing temperatures! Wear a winter coat, gloves, and a hat.")
    elif feels_like < 50:
        print("A medium jacket or sweater is recommended.")
    elif feels_like > 85:
        print("High heat! Stay hydrated and wear light clothing.")

    if wind_speed >= 20:
        print(f"High winds ({wind_speed} mph). Be careful with loose items like hats and umbrellas")


def GET_weather_data(latitude: float, longitude: float):
    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "wind_speed_10m",
            "weather_code"
        ],
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch"
    }

    try:
        response = requests.get(FORECAST_BASE_URL, params=parameters, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("current")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred on GET weather: {e}")
        return None

def GET_location_coordinates(city_input: str):
    parameters = {
        "name": city_input,
        "count": 5,
    }

    try: 
        response = requests.get(GEOCODING_BASE_URL, params=parameters, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occured on GET request: {e}")
        return None

    results = data.get("results")
    if not results:
        print(f"No locations found for '{city_input}'")
        return None

    if len(results) == 1:
        location = results[0]
        state = location.get("admin1", "")
        country = location.get("country", "")
        display = f"{location['name']}, {state}, {country}".strip()
        return {
            "name": display,
            "latitude": location["latitude"],
            "longitude": location["longitude"]
        }

    print(f"Multiple matches found for '{city_input}'")
    for index, item in enumerate(results, start=1):
        state = item.get("admin1", "")
        country = item.get("country", "")
        print(f"{index} {item['name']}, {state}, {country}")

    while True:
        pick = input(f"\nSelect a location 1-{len(results)} from results or 'q' to quit: ")
        if pick.lower() == "q":
            print("quiting...")
            return None
        if int(pick) <= len(results) and int(pick) >= 1:
            location = results[int(pick)-1]
            state = location.get("admin1", "")
            country = location.get("country", "")
            display = f"{location['name']}, {state}, {country}".strip()
            return {
                "name": display,
                "latitude": location["latitude"],
                "longitude": location["longitude"]
            }
        print(f"Invalid pick, Please enter a number between 1 and {len(results)}")

def main():
    print("=" * 50)
    print("               Weather Advisor")
    print("=" * 50)
    print("Get real-time weather and outdoor advice.")
    print("Type 'q' or 'Q' at any time to exit.\n")

    while True:
        city_input = input("Enter city or town name: ").strip()

        if city_input.lower() == "q":
            print("\nExiting Weather Advisor")
            exit(0)

        if not re.match(r"^[A-Za-z ]{2,}$", city_input):
            print("Invalid input. City/Town names must only contain letters and spaces\n")
            continue 

        cache_city = city_input.lower()
        cache = load_cache()

        if cache_city in cache:
            print(f"Found '{city_input}' in cache.")
            location = cache[cache_city]
        else:
            print(f"Looking up '{city_input}' via Geocoding API")
            location = GET_location_coordinates(city_input)
            if not location:
                continue
            save_to_cache(cache_city, location)

        print(f"\nLooking up weather for '{city_input}'...\n")

        weather = GET_weather_data(location["latitude"], location["longitude"])
        if not weather:
            print("Error occured while trying to retrieve weather data. Please try again.\n")
            continue

        print("-" * 50)
        print(f"Temperature:       {weather.get('temperature_2m')}°F (Feels like {weather.get('apparent_temperature')}°F)")
        print(f"Humidity:          {weather.get('relative_humidity_2m')}%")
        print(f"Wind Speed:        {weather.get('wind_speed_10m')} mph")
        print(f"Precipitation:     {weather.get('precipitation')} in")
        print("-" * 50)

        give_weather_advice(weather)

        print("End of Advice!\n")


if __name__ == "__main__":
    main()