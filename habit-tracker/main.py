import requests
from datetime import datetime

USER_NAME = "thisismyusername12"
TOKEN = "as23:dfsw3asdf43ader3"
GRAPH_ID = "graph1"
pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
	"token": TOKEN,
	"username":USER_NAME ,
	"agreeTermsOfService": "yes",
	"notMinor": "yes",
}

# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

graph_config = {
	"id": GRAPH_ID,
	"name": "Code Tracker",
	"unit": "Lines of Code",
	"type": "int",
	"color": "ajisai",
}
headers = {
	"X-USER-TOKEN": TOKEN,
}

graph_endpoint = f"{pixela_endpoint}/{USER_NAME}/graphs"

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
today = datetime.now()

post_config = {
	"date": today.strftime("%Y%m%d"),
	"quantity": "40",

}

post_pixel = f"{pixela_endpoint}/{USER_NAME}/graphs/{GRAPH_ID}"

response = requests.post(url=post_pixel, json=post_config, headers=headers)

print(response.text)