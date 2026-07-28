import requests

question_params = {
	"amount":10,
	"type":"boolean",
}

response = requests.get("https://opentdb.com/api.php", params=question_params)
response.raise_for_status()
data = response.json()
# response_code =(data["response_code"])
new_questions = data["results"]
question_data = new_questions


