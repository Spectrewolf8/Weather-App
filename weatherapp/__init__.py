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


def get_forecast_astro_data(query, days):
    api_key = os.environ.get("API_KEY")
    base_url = "http://api.weatherapi.com/v1/forecast.json"
    params = {"key": api_key, "q": query, "days": days}
    response = requests.get(base_url, params=params).json()

    # Extract the astro data for each day
    astro_data = [day["astro"] for day in response["forecast"]["forecastday"]]
    astro_data = astro_data[0]
    print("astro_data:", astro_data)
    return astro_data
