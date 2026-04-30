import requests
from datetime import date

def get_orthodox_day(calendar="gregorian"):
    today = date.today()
    url = f"https://orthocal.info/api/{calendar}/{today.year}/{today.month}/{today.day}/"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    print(f"Orthodox Calendar for {today.strftime('%B %d, %Y')}")
    print("=" * 40)

    if "feasts" in data:
        print("\nFeasts:")
        for feast in data["feasts"]:
            print(f"- {feast}")

    if "saints" in data:
        print("\nSaints commemorated:")
        for saint in data["saints"]:
            print(f"- {saint}")

    if "fast_level_desc" in data:
        print("\nFasting:")
        print(data["fast_level_desc"])

get_orthodox_day()