import os
import requests
from dotenv import load_dotenv
from requests.exceptions import JSONDecodeError

load_dotenv()

# Add variables in .env file
# API Key from https://www.weatherapi.com/my/
API_KEY = os.environ.get("API_KEY")
print(API_KEY)


def get_weather_data(query):

    import logging

    logging.info(API_KEY)

    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": API_KEY, "q": query, "aqi": "yes"}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
        data = response.json()

        # Check if 'current' key exists in the response
        if "current" in data:
            return data
        else:
            print("The 'current' key does not exist in the response")
    except JSONDecodeError:
        print("Error decoding the response")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_forecast_astro_data(query, days):
    base_url = "http://api.weatherapi.com/v1/forecast.json"
    params = {"key": API_KEY, "q": query, "days": days}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
        data = response.json()

        # Check if 'forecast' key exists in the response
        if "forecast" in data and "forecastday" in data["forecast"]:
            # Extract the astro data for each day
            astro_data = [day["astro"] for day in data["forecast"]["forecastday"]]
            astro_data = astro_data[0]
            # print("astro_data:", astro_data)
            return astro_data
        else:
            print("The 'forecast' key does not exist in the response")
    except JSONDecodeError:
        print("Error decoding the response")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")
