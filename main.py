import requests
from datetime import date
import tkinter as tk

def get_orthodox_day(calendar):
    today = date.today()
    url = f"https://orthocal.info/api/{calendar}/{today.year}/{today.month}/{today.day}/"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    output = []
    output.append(f"Orthodox Calendar for {today.strftime('%B %d, %Y')} ({calendar})")
    output.append("=" * 50)

    # feasts
    if data.get("feasts"):
        output.append("\nFeasts:")
        for feast in data["feasts"]:
            output.append(f"- {feast}")
    else:
        output.append("\nFeasts:")
        output.append("- No feast day.")

    # saints
    if data.get("saints"):
        output.append("\nSaints commemorated:")
        for saint in data["saints"]:
            output.append(f"- {saint}")
    else:
        output.append("\nSaints commemorated:")
        output.append("- No saints listed.")

    # fasting
    if data.get("fast_level_desc"):
        output.append("\nFasting:")
        output.append(data["fast_level_desc"])

    return "\n".join(output)


def show_calendar():
    calendar = "gregorian" if var.get() == 1 else "julian"
    text_box.delete("1.0", tk.END)
    result = get_orthodox_day(calendar)
    text_box.insert(tk.END, result)


# setup
root = tk.Tk()
root.title("Orthodox Calendar")

var = tk.IntVar(value=1)

tk.Label(root, text="Choose calendar:").pack()

tk.Radiobutton(root, text="Gregorian (New Calendar)", variable=var, value=1).pack()
tk.Radiobutton(root, text="Julian (Old Calendar)", variable=var, value=2).pack()

tk.Button(root, text="Show Today", command=show_calendar).pack(pady=10)

text_box = tk.Text(root, height=20, width=60)
text_box.pack()

root.mainloop()