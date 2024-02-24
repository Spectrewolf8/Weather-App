import os
import requests
from dotenv import load_dotenv
from requests.exceptions import JSONDecodeError

load_dotenv()  # Load environment variables from a .env file

# Retrieve the API key from environment variables
API_KEY = os.environ.get("API_KEY")


def get_weather_data(query):
    # Define the base URL for the current weather data API
    base_url = "http://api.weatherapi.com/v1/current.json"
    # Define the parameters for the API request
    params = {"key": API_KEY, "q": query, "aqi": "yes"}

    # Send a GET request to the API
    response = requests.get(base_url, params=params)
    # Parse the response as JSON
    data = response.json()
    print("data", data)
    # Return the parsed data
    return data


def get_forecast_astro_data(query, days):
    # Define the base URL for the forecast data API
    base_url = "http://api.weatherapi.com/v1/forecast.json"
    # Define the parameters for the API request
    params = {"key": API_KEY, "q": query, "days": days}

    try:
        # Send a GET request to the API
        response = requests.get(base_url, params=params)
        # If the response status is 4xx or 5xx, raise an HTTPError
        response.raise_for_status()
        # Parse the response as JSON
        data = response.json()

        # Check if the 'forecast' key exists in the response
        if "forecast" in data and "forecastday" in data["forecast"]:
            # Extract the astro data for each day
            astro_data = [day["astro"] for day in data["forecast"]["forecastday"]]
            astro_data = astro_data[0]
            # Return the astro data
            return astro_data
        else:
            print("The 'forecast' key does not exist in the response")
    except JSONDecodeError:
        print("Error decoding the response")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")
