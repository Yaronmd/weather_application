import os
import aiohttp
from dotenv import load_dotenv
import requests
# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
API_KEY = os.getenv("GOOGLE_MAP_KEYS")


GOOGLE_PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
GOOGLE_GEOCODE_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"

def fetch_location_suggestions( query, types="(cities)"):
    """
    Fetch location suggestions from Google Places API.
    
    :param api_key: Google API key
    :param query: Input text for location
    :param types: Type of location to restrict results
    :return: List of location suggestions
    """
    params = {
        "input": query,
        "key": API_KEY,
        "types": types
    }
    response = requests.get(GOOGLE_PLACES_API_URL, params=params)
    data = response.json()
    if "predictions" in data:
        return [item["description"] for item in data["predictions"]]
    return []

def fetch_lat_lon(location):
    """
    Fetch latitude and longitude of a location using Google Geocoding API.
    
    :param api_key: Google API key
    :param location: Location string
    :return: Tuple (latitude, longitude) or None if not found
    """
    params = {"address": location, "key": API_KEY}
    response = requests.get(GOOGLE_GEOCODE_API_URL, params=params)
    data = response.json()
    print(data)
    if data.get("results"):
        lat = data["results"][0]["geometry"]["location"]["lat"]
        lon = data["results"][0]["geometry"]["location"]["lng"]
        return lat, lon
    return None