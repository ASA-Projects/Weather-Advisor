"""
Weather Advisor
A command-line weather advisor using Open-Meteo APIs.
"""

# API Endpoints
GEOCODING_BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_BASE_URL = "https://api.open-meteo.com/v1/forecast"
CACHE_FILE = "locations_cache.json"


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

        print(f"Looking up weather for '{city_input}'...\n")


if __name__ == "__main__":
    main()