import requests

BASE_URL = "http://127.0.0.1:8000"

# Asks the server to search for the user
def search_user(display_name):
    try:
        url = f"{BASE_URL}/search/{display_name}"
        response = requests.get(url)
        return response
    except requests.exceptions.ConnectionError:
        return None