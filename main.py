import time

import requests
from config import *
from datetime import datetime, timezone


def is_over_head():
    response = requests.get(url=ISS_URL)
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    return abs(MY_LAT - iss_latitude) < 5 and abs(MY_LONG - iss_longitude) < 5


def is_nighttime():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    response = requests.get(url=DAY_NIGHT_URL, params=parameters)
    response.raise_for_status()

    sunrise_data = response.json()["results"]

    sunrise = datetime.fromisoformat(sunrise_data["sunrise"])
    # print(f"Sunrise:{sunrise}")
    sunset = datetime.fromisoformat(sunrise_data["sunset"])
    # print(f"Sunset:{sunset}")
    now = datetime.now(timezone.utc)  # Returns TZ aware datetime object
    # print(f"Now:{now}")
    return sunrise > now or now > sunset


# convert_to_local()
# print(f"Is night:{is_nighttime()}")
# print(f"Is over head:{is_over_head()}")


# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
while True:
    if is_nighttime():
        if is_over_head():
            print("look at the sky!")
        else:
            print("not overhead")
    else:
        print("day time now")

    time.sleep(CHECK_EVERY_SECOND)
