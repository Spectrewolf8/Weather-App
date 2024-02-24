from weatherapp import weather
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="weatherapp/templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    place_name = request.form["place_name"].lower()
    weather_data = weather(query=place_name)
    user_name = "John Doe"  # Example variable
    context = {"weather_data": weather_data, "user_name": user_name}
    return render_template("submit.html", **context)


if __name__ == "__main__":
    app.run(debug=True)
