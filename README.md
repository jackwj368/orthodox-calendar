# orthodox-calendar

This is a small desktop widget that shows the daily feast days, saints, and fasting information from the Eastern Orthodox Church. It runs as a lightweight macOS window that stays on top of everything and looks like a floating glass-style card.

I built this because I wanted something simple I could glance at during the day without opening a browser or app.

setup:

    git clone https://github.com/yourusername/orthodox-calendar-widget.git
    
    cd orthodox-calendar-widget

    python3 -m venv .venv

    source .venv/bin/activate

    pip install flask requests pyobjc

to run:

    python mac_window.py

ONLY WORKS ON MACOS
