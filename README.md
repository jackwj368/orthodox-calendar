# orthodox-calendar

This is a small desktop widget for macOS that shows the daily feast days, saints, and fasting information from the Eastern Orthodox Church. It runs as a lightweight macOS window that stays on top of everything and looks like a floating glass-style card.

I built this because I wanted something simple I could glance at during the day without opening a browser or app.

setup:

    git clone https://github.com/yourusername/orthodox-calendar-widget.git
    
    cd orthodox-calendar-widget

    python3 -m venv .venv

    source .venv/bin/activate

    pip install flask requests pyobjc pynput

to run:

    python mac_window.py

## macOS Permissions

For the keyboard shortcut (Command + Shift + O) to work, you must allow input monitoring:

1. Open System Settings
2. Go to Privacy & Security
3. Click Accessibility
4. Add and enable:
   - Terminal (or your IDE like PyCharm)

Without this, the hotkey will not work.

## Controls

- Drag the widget using the top area
- Toggle click-through mode:
  - Command + Shift + O

When click-through is ON, the widget ignores mouse input and lets you click through it.
