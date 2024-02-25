# Import necessary modules
from weatherapp import get_weather_data, get_forecast_astro_data
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import os
import requests

# Initialize Flask app
app = Flask(__name__, template_folder="weatherapp/templates")
CORS(app)  # Enable CORS

# Get API key from environment variables
MAPS_API_KEY = OPENCAGE_API_KEY = os.getenv("MAPS_API_KEY")


@app.route("/")
def index():
    # Render the index page
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    # Get location from form data
    query_location = request.form["place_name"].lower()
    # Get weather data for the location
    weather_data = get_weather_data(query=query_location)
    if "error" in weather_data:
        context = {
            "weather_data": weather_data,
            "location": query_location,
        }
        # If there's an error, render the error page
        if weather_data.get("error")["code"] == 1006:
            return render_template("404.html", **context)
    else:
        # Get forecast and astronomical data for the location
        forecast_astro_data = get_forecast_astro_data(query=query_location, days=1)
        context = {
            "weather_data": weather_data,
            "astro_data": forecast_astro_data,
            "weather_condition": weather_data["current"]["condition"]["text"],
            "location": query_location,
        }
        # Render the submit page with the weather and astronomical data
        return render_template("submit.html", **context)


@app.route("/api/autocomplete", methods=["GET"])
def autocomplete():
    # Get query parameter for autocomplete
    query = request.args.get("q")

    if query:
        # Make a request to the OpenCage Geocoding API for autocompletion
        response = requests.get(
            f"https://api.opencagedata.com/geocode/v1/json?q={query}&key={OPENCAGE_API_KEY}"
        )
        data = response.json()

        # Extract relevant information for autocomplete suggestions
        suggestions = []
        for result in data.get("results", []):
            # Customize the suggestion based on your needs
            suggestion = {
                "place": result.get("formatted"),
            }
            suggestions.append(suggestion)
        return jsonify({"suggestions": suggestions})

    # Return error if query parameter is missing
    return jsonify({"error": "Missing query parameter"}), 400


if __name__ == "__main__":
    # Run the app
    app.run(debug=True)
