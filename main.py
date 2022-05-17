import requests
from datetime import datetime
import smtplib
import time


MY_LAT = 0 # Your latitude
MY_LONG = 0 # Your longitude
my_email = ""
password = '='
receive_email = ''
alert_on = False


# Get ISS position and check is it's above you
def is_above_you():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    above_you = MY_LAT - 5 < iss_latitude < MY_LAT + 5 and \
                MY_LONG - 5 < iss_longitude < MY_LONG + 5
    return above_you


# Get sunrise/set time and check is it's dark now
def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = int(str(datetime.utcnow()).split(' ')[1].split(':')[0])
    if sunrise > sunset:
        if sunset < time_now < sunrise:
            return True
        else:
            return False
    else:
        if sunrise < time_now < sunset:
            return False
        else:
            return True


def send_email():
    print("working")
    print(is_dark())
    print(is_above_you())
    if is_dark() and is_above_you():
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=receive_email,
                msg="Subject:LOOK UP!\n\n The ISS is above you and you can see it if you look up!"
            )


while alert_on:
    send_email()
    time.sleep(5)




