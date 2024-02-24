from weatherapp import get_weather_data, get_forecast_astro_data
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import os

app = Flask(__name__, template_folder="weatherapp/templates")
CORS(app)


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


@app.route("/api/key", methods=["GET"])
def get_api_key():
    return jsonify(key=os.getenv("MAPS_API_KEY"))


# 'error': {'code': 1006, 'message': 'No matching location found.'}}

if __name__ == "__main__":
    app.run(debug=True)
