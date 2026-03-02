import requests

BASE_URL = "http://127.0.0.1:8000"

def search_user(display_name):
    """Asks the server to search for the user by display name."""
    try:
        url = f"{BASE_URL}/search/{display_name}"
        response = requests.get(url, timeout=5)
        return response
    except requests.exceptions.RequestException:
        return None