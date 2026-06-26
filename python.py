
import html
import json
import sqlite3
import os
import urllib.error
import urllib.request
import datetime
from flask import Flask, render_template, abort
from jinja2 import TemplateNotFound

conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()
# cursor.execute("SELECT game_id, COUNT(*) FROM Characters GROUP BY game_id;")

app = Flask(__name__)

BEACH_COORDINATES = {
    "collaroy": {"lat": -33.7494, "lon": 151.2815},
   "curl-curl": {"lat": -33.7643,"lon": 151.2973},
   "dee-why": {"lat": -33.7511, "lon": 151.2889},
   "freshwater": {"lat": -33.7787, "lon": 151.2857},
   "manly": {"lat": -33.798, "lon": 151.2883},
   "palm": {"lat": -33.597, "lon": 151.321}
}


def weather_code_description(code):
    return {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }.get(code, "Unknown")


def weather_code_icon(code):
    return {
        0: "☀️",
        1: "🌤️",
        2: "⛅",
        3: "☁️",
        45: "🌫️",
        48: "🌫️",
        51: "🌦️",
        53: "🌦️",
        55: "🌧️",
        56: "🌧️",
        57: "🌧️",
        61: "🌧️",
        63: "🌧️",
        65: "⛈️",
        66: "🌨️",
        67: "🌨️",
        71: "❄️",
        73: "❄️",
        75: "❄️",
        77: "🌨️",
        80: "🌦️",
        81: "🌧️",
        82: "⛈️",
        85: "🌨️",
        86: "🌨️",
        95: "⛈️",
        96: "⛈️",
        99: "⛈️",
    }.get(code, "❓")


def get_weather_forecast(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max"
        f"&timezone=Australia/Sydney"
    )

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.load(response)
    except (urllib.error.URLError, json.JSONDecodeError):
        return None

    daily = data.get("daily", {})
    forecast = []
    for index, date in enumerate(daily.get("time", [])[:7]):
        date_obj = datetime.date.fromisoformat(date)
        forecast.append({
            "weekday": date_obj.strftime("%a"),
            "date": date_obj.strftime("%d %b"),
            "description": weather_code_description(daily.get("weathercode", [0])[index]),
            "icon": weather_code_icon(daily.get("weathercode", [0])[index]),
            "temp_max": round(daily.get("temperature_2m_max", [0])[index]),
            "temp_min": round(daily.get("temperature_2m_min", [0])[index]),
            "rain": round(daily.get("precipitation_sum", [0])[index], 1),
            "wind_speed": round(daily.get("windspeed_10m_max", [0])[index], 1),
        })
    return forecast


@app.route("/")
def home():
    return render_template("homepage.html", body=html)


@app.route("/northenbeaches")
def northenbeaches():
    return render_template("northenbeaches.html", body=html)


@app.route("/The-game")
def game():
    return render_template("The-game.html", body=html)


@app.route("/northenbeaches/<beach>")
def beach_page(beach):
    template_path = f"N-beaches_templates/{beach}.html"
    weather_forecast = None
    if beach in BEACH_COORDINATES:
        coords = BEACH_COORDINATES[beach]
        weather_forecast = get_weather_forecast(coords["lat"], coords["lon"])

    try:
        return render_template(
            template_path,
            body=html,
            weather_forecast=weather_forecast,
            beach_name=beach.replace("-", " ").title(),
        )
    except TemplateNotFound:
        abort(404)


if __name__ == "__main__":
    app.run(ssl_context=("localhost.crt", "localhost.key"), port=443, host="0.0.0.0") 