import requests
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun


@tool
def get_weather(city: str):
    """Get the current weather for a city."""

    # Step 1: Convert city name into coordinates
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    geocoding_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    geocoding_response = requests.get(
        geocoding_url,
        params=geocoding_params
    )

    geocoding_data = geocoding_response.json()

    if "results" not in geocoding_data:
        return f"Could not find the city: {city}"

    location = geocoding_data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]

    # Step 2: Get weather
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params
    )

    weather_data = weather_response.json()

    return weather_data


if __name__ == "__main__":
    weather = get_weather.invoke({"city": "Tokyo"})

    print(weather)
    

@tool
def search_places(city: str, interest: str) -> str:
    """Find interesting tourist places in a city."""

    # -----------------------------
    # Step 1: Find city coordinates
    # -----------------------------

    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    geocoding_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    geocoding_response = requests.get(
        geocoding_url,
        params=geocoding_params,
        timeout=10
    )

    geocoding_response.raise_for_status()

    geocoding_data = geocoding_response.json()

    if "results" not in geocoding_data:
        return f"Could not find the city: {city}"

    location = geocoding_data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]

    # -----------------------------
    # Step 2: Search OpenStreetMap
    # -----------------------------

    overpass_url = "https://overpass-api.de/api/interpreter"

    query = f"""
    [out:json][timeout:25];

    (
      node["tourism"](around:5000,{latitude},{longitude});
      way["tourism"](around:5000,{latitude},{longitude});
    );

    out center;
    """

    response = requests.get(
        overpass_url,
        params={"data": query},
        headers={
            "User-Agent": "AI-Travel-Planner/1.0"
        },
        timeout=35
    )

    # -----------------------------
    # Step 3: Check the response
    # -----------------------------

    if response.status_code != 200:
        return (
            f"Unable to search places right now. "
            f"The places service returned HTTP {response.status_code}."
        )

    try:
        data = response.json()
    except ValueError:
        return "The places service returned an invalid response."

    # -----------------------------
    # Step 4: Extract places
    # -----------------------------

    places = []

    for element in data.get("elements", []):

        tags = element.get("tags", {})

        name = tags.get("name")

        if name:
            places.append(name)

    # Remove duplicates
    places = list(dict.fromkeys(places))

    if not places:
        return f"No tourist places found in {city}."

    places = places[:15]

    return (
        f"Interesting places in {city} "
        f"for someone interested in {interest}:\n"
        + "\n".join(f"- {place}" for place in places)
    )
    
    
@tool
def web_search(query: str) -> str:
    """Search the web for current travel information."""

    search = DuckDuckGoSearchRun()

    result = search.invoke(query)

    return result
 