import threading
import requests
from datetime import date
from flask import Flask, render_template, request

from Cocoa import (
    NSApplication,
    NSApp,
    NSWindow,
    NSMakeRect,
    NSBackingStoreBuffered,
    NSColor,
    NSFloatingWindowLevel,
    NSPoint,
)
from WebKit import WKWebView
from Foundation import NSURL, NSURLRequest


app = Flask(__name__)


class DraggableWindow(NSWindow):
    def mouseDown_(self, event):
        self.initial_location = event.locationInWindow()

    def mouseDragged_(self, event):
        current_location = event.locationInWindow()
        window_frame = self.frame()

        new_origin = NSPoint(
            window_frame.origin.x + current_location.x - self.initial_location.x,
            window_frame.origin.y + current_location.y - self.initial_location.y
        )

        self.setFrameOrigin_(new_origin)


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


def create_mac_window():
    NSApplication.sharedApplication()

    frame = NSMakeRect(300, 300, 360, 500)

    window = DraggableWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        frame,
        0,
        NSBackingStoreBuffered,
        False
    )

    window.setTitle_("Orthodox Calendar")
    window.setOpaque_(False)
    window.setBackgroundColor_(NSColor.clearColor())
    window.setLevel_(NSFloatingWindowLevel)

    webview = WKWebView.alloc().initWithFrame_(NSMakeRect(0, 0, 360, 500))
    webview.setValue_forKey_(False, "drawsBackground")

    url = NSURL.URLWithString_("http://127.0.0.1:5000")
    request = NSURLRequest.requestWithURL_(url)
    webview.loadRequest_(request)

    window.setContentView_(webview)
    window.makeKeyAndOrderFront_(None)

    NSApp.run()


if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    create_mac_window()