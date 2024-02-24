from weatherapp import get_weather_data
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="weatherapp/templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    query_location = request.form["place_name"].lower()
    weather_data = get_weather_data(query=query_location)
    context = {
        "weather_data": weather_data,
        "weather_condition": weather_data["current"]["condition"]["text"],
        "location": query_location,
    }
    print(context)

    if "error" in weather_data:
        if weather_data.get("error")["code"] == 1006:
            return render_template("404.html", **context)
    else:
        return render_template("submit.html", **context)


# 'error': {'code': 1006, 'message': 'No matching location found.'}}

if __name__ == "__main__":
    app.run(debug=True)
