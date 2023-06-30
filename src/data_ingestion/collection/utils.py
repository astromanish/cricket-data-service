import requests
import json

def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data from the API.")
        return None

def save_json(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f)
