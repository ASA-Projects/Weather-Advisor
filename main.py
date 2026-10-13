
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



if __name__ == "__main__":
    main()