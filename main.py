import requests
import datetime as dt
import smtplib
import time

MY_LAT = 51.509865
MY_LONG = -0.118092
# Example Latitude and Longitude for London. Use https://www.latlong.net/ to get yours.
MY_EMAIL = "you-email-address-here@gmail.com"  # This script is preconfigured for Gmail.
# Change the SMTP settings below if you are not using Gmail to send these emails.
MY_PASSWORD = "your-app-password-here"  # Use an App Password, not your email password
# How to set up an App Password: https://support.google.com/accounts/answer/185833
RECIPIENT_EMAIL = "your-recipient's-email-address@website.com"  # Any email address should work.
# Make sure to send a test email and mark it as 'Not Spam' so that it reaches your inbox.


def is_iss_close():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()["iss_position"]

    iss_latitude = data["latitude"]
    iss_longitude = data["longitude"]

    iss_position = {
        "lat": iss_latitude,
        "long": iss_longitude,
        "formatted": 0
    }

    my_position = {
        "lat": MY_LAT,
        "long": MY_LONG,
        "formatted": 0
    }

    iss_lat_distance = my_position["lat"] - float(iss_position["lat"])
    iss_long_distance = my_position["long"] - float(iss_position["long"])

    if 6 > iss_lat_distance > -6 and 6 > iss_long_distance > -6:
        return True
    else:
        return False


def is_currently_dark():
    now = dt.datetime.now()
    response = requests.get("https://api.sunrise-sunset.org/json?", params={"lat": MY_LAT,
                                                                            "long": MY_LONG,
                                                                            "formatted": 0})
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    return now.hour < sunrise or now.hour > sunset


while True:
    time.sleep(60)
    if is_currently_dark() and is_iss_close():
        with smtplib.SMTP("smtp.gmail.com:587") as connection:  # Change these SMTP settings if you are not using Gmail
            connection.ehlo()
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=RECIPIENT_EMAIL,
                                msg="Subject:The ISS is above you!\n\nLook up!")
