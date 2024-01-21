import requests
from datetime import datetime
import smtplib

MY_LAT = 48.208176
MY_LNG = 16.373819
my_lat_lng = (MY_LNG, MY_LAT)
my_email = "merab1223t@gmail.com"
password = "xhygcsvzayclrrnw"

res = requests.get("http://api.open-notify.org/iss-now.json")
res.raise_for_status()
data = res.json()
longitude = data["iss_position"]["longitude"]
latitude = data["iss_position"]["latitude"]
iss_position = (longitude, latitude)

lat_long = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0
}

res = requests.get(f"https://api.sunrise-sunset.org/json", params=lat_long, )
res.raise_for_status()
sun_set = res.json()["results"]["sunset"].split("T")[1].split(":")[0]
sun_rise = res.json()["results"]["sunrise"].split("T")[1].split(":")[0]

time_now = datetime.now().hour


def comp_positions():
    # Assuming my_lat_lng and iss_position are tuples or lists with [latitude, longitude] format

    # Check if the absolute difference in latitude is within 5 degrees
    lat_diff = abs(float(my_lat_lng[0]) - float(iss_position[0]))
    lat_within_range = lat_diff <= 5

    # Check if the absolute difference in longitude is within 5 degrees
    lng_diff = abs(float(my_lat_lng[1]) - float(iss_position[1]))
    lng_within_range = lng_diff <= 5

    # Return True only if both latitude and longitude are within the specified range
    return lat_within_range and lng_within_range


if comp_positions() and int(sun_set) <= int(time_now) or int(time_now) <= int(sun_rise):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.login(user=my_email, password=password)
        connection.starttls()
        connection.sendmail(from_addr=my_email, to_addrs="merabtodua7@gmail.com", msg="Subject: Iss is here\n\nLook "
                                                                                      "up Iss should be above you")
