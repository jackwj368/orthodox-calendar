import threading
import requests
from datetime import date
from flask import Flask, render_template, request

from Cocoa import (
    NSApplication,
    NSApp,
    NSWindow,
    NSView,
    NSMakeRect,
    NSBackingStoreBuffered,
    NSColor,
    NSFloatingWindowLevel,
    NSScreen,
)
from WebKit import WKWebView
from Foundation import NSURL, NSURLRequest


app = Flask(__name__)

WINDOW_WIDTH = 360
WINDOW_HEIGHT = 500
DRAG_BAR_HEIGHT = 40


class DragBar(NSView):
    def mouseDown_(self, event):
        self.window().performWindowDragWithEvent_(event)


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

    screen = NSScreen.mainScreen()
    visible_frame = screen.visibleFrame()

    margin = 20

    x = visible_frame.origin.x + visible_frame.size.width - WINDOW_WIDTH - margin
    y = visible_frame.origin.y + visible_frame.size.height - WINDOW_HEIGHT - margin

    frame = NSMakeRect(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)

    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        frame,
        0,
        NSBackingStoreBuffered,
        False
    )

    window.setTitle_("Orthodox Calendar")
    window.setOpaque_(False)
    window.setBackgroundColor_(NSColor.clearColor())
    window.setLevel_(NSFloatingWindowLevel)

    container = NSView.alloc().initWithFrame_(
        NSMakeRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    )

    webview = WKWebView.alloc().initWithFrame_(
        NSMakeRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    )
    webview.setValue_forKey_(False, "drawsBackground")

    url = NSURL.URLWithString_("http://127.0.0.1:5000")
    request = NSURLRequest.requestWithURL_(url)
    webview.loadRequest_(request)

    drag_bar = DragBar.alloc().initWithFrame_(
        NSMakeRect(0, WINDOW_HEIGHT - DRAG_BAR_HEIGHT, WINDOW_WIDTH, DRAG_BAR_HEIGHT)
    )

    container.addSubview_(webview)
    container.addSubview_(drag_bar)

    window.setContentView_(container)
    window.makeKeyAndOrderFront_(None)

    NSApp.run()


if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    create_mac_window()