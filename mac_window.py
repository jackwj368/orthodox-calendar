import threading
import requests
from pynput import keyboard
from datetime import date
from flask import Flask, render_template, request
from PyObjCTools import AppHelper

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

WINDOW_WIDTH = 336
WINDOW_HEIGHT = 460
DRAG_BAR_HEIGHT = 60

CLICK_THROUGH = False
main_window = None


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


def apply_click_through():
    if main_window:
        main_window.setIgnoresMouseEvents_(CLICK_THROUGH)

    print(f"Click-through mode: {'ON' if CLICK_THROUGH else 'OFF'}")


def toggle_click_through():
    global CLICK_THROUGH
    CLICK_THROUGH = not CLICK_THROUGH

    AppHelper.callAfter(apply_click_through)


def start_hotkey_listener():
    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse("<cmd>+<shift>+o"),
        toggle_click_through
    )

    def for_canonical(function):
        return lambda key: function(listener.canonical(key))

    with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)
    ) as listener:
        listener.join()


def create_mac_window():
    global main_window

    NSApplication.sharedApplication()

    screen = NSScreen.mainScreen()
    visible_frame = screen.visibleFrame()

    x_margin = 20
    y_margin = 5

    x = visible_frame.origin.x + visible_frame.size.width - WINDOW_WIDTH - x_margin
    y = visible_frame.origin.y + visible_frame.size.height - WINDOW_HEIGHT - y_margin

    frame = NSMakeRect(x, y, WINDOW_WIDTH, WINDOW_HEIGHT)

    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        frame,
        0,
        NSBackingStoreBuffered,
        False
    )

    main_window = window

    window.setTitle_("Orthodox Calendar")
    window.setOpaque_(False)
    window.setBackgroundColor_(NSColor.clearColor())
    window.setLevel_(NSFloatingWindowLevel)
    window.setIgnoresMouseEvents_(CLICK_THROUGH)

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

    hotkey_thread = threading.Thread(target=start_hotkey_listener)
    hotkey_thread.daemon = True
    hotkey_thread.start()

    create_mac_window()