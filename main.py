import requests
from datetime import date

def get_orthodox_day(calendar):
    today = date.today()
    url = f"https://orthocal.info/api/{calendar}/{today.year}/{today.month}/{today.day}/"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    print(f"\nOrthodox Calendar for {today.strftime('%B %d, %Y')} ({calendar})")
    print("=" * 50)

    if data.get("feasts"):
        print("\nFeasts:")
        for feast in data["feasts"]:
            print(f"- {feast}")
    else:
        print("\nFeasts:")
        print("- No feast day.")

    if data.get("saints"):
        print("\nSaints commemorated:")
        for saint in data["saints"]:
            print(f"- {saint}")
    else:
        print("\nSaints commemorated:")
        print("- No saints listed.")

    if "fast_level_desc" in data:
        print("\nFasting:")
        print(data["fast_level_desc"])

print("Choose calendar:")
print("1. Gregorian (New Calendar)")
print("2. Julian (Old Calendar)")

choice = input("Enter 1 or 2: ").strip()

if choice == "1":
    calendar = "gregorian"
elif choice == "2":
    calendar = "julian"
else:
    print("Invalid choice, defaulting to Gregorian.")
    calendar = "gregorian"

get_orthodox_day(calendar)