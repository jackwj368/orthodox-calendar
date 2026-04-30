import requests
from datetime import date
from flask import Flask, render_template, request
import webview
import threading

app = Flask(__name__)


def get_orthodox_day(calendar):
    today = date.today()
    url = f"https://orthocal.info/api/{calendar}/{today.year}/{today.month}/{today.day}/"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    return {
        "date": today.strftime("%B %d, %Y"),
        "calendar": calendar,
        "feasts": data.get("feasts") or [],
        "saints": data.get("saints") or [],
        "fasting": data.get("fast_level_desc") or "No fasting information listed."
    }


@app.route("/")
def home():
    calendar = request.args.get("calendar", "gregorian")
    info = get_orthodox_day(calendar)
    return render_template("index.html", info=info)


def run_flask():
    app.run(debug=False, port=5000)


if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    webview.create_window(
        "Orthodox Calendar",
        "http://127.0.0.1:5000",
        width=600,
        height=750,
        frameless=True,
    )

    webview.start()