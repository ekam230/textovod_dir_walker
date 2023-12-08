
import requests

url = 'https://textovod.com/api/unique/user/add'
user_id = 334831
api_key = "szRNHfXwF5jpkeniWHxCG9g3iP5J1bmHRwG8CC1LZI7TL0kHNyNL7Uw4gdVZ"

def send_request(text):
    data = {"user_id":user_id,"api_key":api_key,"text":text}
    # Send POST request with JSON data using the json parameter
    response = requests.post(url, json=data)
    return response.json()