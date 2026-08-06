import os
import requests
from twilio.rest import Client

TWILIO_ACCOUNT_SID: str = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN: str = os.environ["TWILIO_AUTH_TOKEN"]
OWN_AP: str = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY: str = os.environ["OWM_API_KEY"]
LAT: str = "41.2563"
LNG: str = "-95.9404"
parameters: dict= {
	"lat": LAT,
	"lon": LNG,
	"appid": API_KEY,
	"units": "imperial",
	"cnt": 4,
}

response = requests.get(url=OWN_AP, params=parameters)
response.raise_for_status()
data = response.json()

will_rain = False

for hour_data in data["list"]:
	condition_code = hour_data["weather"][0]["id"]
	if int(condition_code) < 600:
		will_rain = True

if will_rain:
	client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
	message = client.messages.create(
		body="Bring an Umbrella! God's pissing on all of us today!",
		from_=os.environ["TWILIO_FROM_NUMBER"],
		to=os.environ["TWILIO_TO_NUMBER"],
	)
	print(message.status)

# weather ={
#
# }

# for i in range(4):
# 	weather_id = data["list"][i]["weather"][0]["id"]
# 	weather_description = data["list"][i]["weather"][0]["description"]
# 	weather[i] = {"id":weather_id, "description":weather_description}

# for i in range(4):
# 	if weather[i]["id"] > 600:
# 		print(weather[i]["description"] + "\n Bring an Umbrella")
