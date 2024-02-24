from weatherapp import get_weather_data, get_forecast_astro_data
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import os
import requests

app = Flask(__name__, template_folder="weatherapp/templates")
CORS(app)

MAPS_API_KEY = OPENCAGE_API_KEY = os.getenv("MAPS_API_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    query_location = request.form["place_name"].lower()
    weather_data = get_weather_data(query=query_location)
    print(weather_data)
    if "error" in weather_data:
        context = {
            "weather_data": weather_data,
            "location": query_location,
        }
        if weather_data.get("error")["code"] == 1006:
            return render_template("404.html", **context)
    else:
        forecast_astro_data = get_forecast_astro_data(query=query_location, days=1)
        context = {
            "weather_data": weather_data,
            "astro_data": forecast_astro_data,
            "weather_condition": weather_data["current"]["condition"]["text"],
            "location": query_location,
        }

        return render_template("submit.html", **context)


@app.route("/api/autocomplete", methods=["GET"])
def autocomplete():
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
                # "latitude": result.get("geometry", {}).get("lat"),
                # "longitude": result.get("geometry", {}).get("lng"),
            }
            suggestions.append(suggestion)
        # print(suggestions)
        return jsonify({"suggestions": suggestions})

    return jsonify({"error": "Missing query parameter"}), 400


# 'error': {'code': 1006, 'message': 'No matching location found.'}}

if __name__ == "__main__":
    app.run(debug=True)
