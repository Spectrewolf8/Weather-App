import os
import requests
from dotenv import load_dotenv


load_dotenv()

# Add variables in .env file
# API Key from https://www.weatherapi.com/my/
API_KEY = os.environ.get("API_KEY")


# Weather checking module
def get_weather_data(query):
    api_key = os.environ.get("API_KEY")
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": api_key, "q": query, "aqi": "yes"}
    response = requests.get(base_url, params=params).json()

    return response
