import os
import aiohttp
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
API_KEY = os.getenv("API_KEY")

API_URL = "http://api.openweathermap.org/data/2.5/weather"


async def fetch_weather(lat, lon):
    url = f"{API_URL}?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                print(data)
                return data
            else:
                return None