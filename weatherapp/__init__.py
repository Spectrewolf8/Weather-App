import os
import requests
from dotenv import load_dotenv


load_dotenv()

# Add variables in .env file
# API Key from https://www.weatherapi.com/my/
API_KEY = os.environ.get("API_KEY")


def error(request):
    if request.get("error"):
        err = request["error"]
        text = "Error ({error['code']}):- " + err["message"]
        return text
    else:
        return False


def get_location_details(request):
    l_arr = []
    for i in request:
        if i == "lat":
            name = "Latitude"
        elif i == "lon":
            name = "Longitude"
        elif i == "tz_id":
            name = "Timezone ID"
        else:
            name = i.replace("_", " ")
            if " " in name:
                words = name.split()
                name = " ".join(word.capitalize() for word in words)
        l_arr.append(f"<b>{name}:</b> {str(request[i])}")
    text = "<br/>".join(l_arr)
    return text


def uv(n):
    if n < 2:
        return "Low"
    if n < 5:
        return "Moderate"
    if n < 7:
        return "High"
    if n < 10:
        return "Very High"
    return "Extreme"


def get_aqi(request):
    aqi_arr = []
    for i in request:
        if i == "co":
            name = "Carbon Monoxide"
        elif i == "no2":
            name = "Nitrogen dioxide"
        elif i == "o3":
            name = "Ozone"
        elif i == "so2":
            name = "Sulfur dioxide"
        elif i == "pm2_5":
            name = "PM 2.5"
        elif i == "pm10":
            name = "PM 10"
        elif i == "us-epa-index":
            name = "US EPA Index"
        elif i == "gb-defra-index":
            name = "GB Defra Index"
        else:
            name = i.replace("_", " ")
            if " " in name:
                words = name.split()
                name = " ".join(word.capitalize() for word in words)
        aqi_arr.append(f"<b>{name}:</b> {str(request[i])}")
    text = "<br/>".join(aqi_arr)
    return text


def get_current_details(request):
    curr_arr = []
    for i in request:
        if i in ["condition", "air_quality"]:
            pass
        else:
            value = str(request[i])
            if i == "is_day":
                name = "Day/Night"
                if value == "0":
                    value = "Night"
                else:
                    value = "Day"
            elif i == "uv":
                name = "Ultraviolet Index"
                value = str(request[i]) + f" ({uv(request[i])})"
            else:
                name = i.replace("_", " ")
                if " " in name:
                    words = name.split()
                    name = " ".join(word.capitalize() for word in words)
            curr_arr.append(f"<b>{name}:</b> {value}")
    text = "<br/>".join(curr_arr)
    return text


# Weather checking module
def weather(query):
    api = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={query}&aqi=yes"
    response = requests.get(api).json()
    print(response)
    text = ""

    if error(response):
        return error(response)
    text += "<h3>Location Details</h3>"
    text += get_location_details(response["location"])
    text += "<br/><br/>"

    text += "<h3>Current Weather Details</h3>"
    text += get_current_details(response["current"])
    text += "<br/><br/>"

    text += "<h3>Air Quality Details</h3>"
    text += get_aqi(response["current"]["air_quality"])
    return response
    # return text
