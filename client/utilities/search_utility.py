import requests

BASE_URL = "http://127.0.0.1:8000"

# Searches user by their display name
def search_user_by_dn(display_name):
    """Asks the server to search for the user by display name."""
    try:
        url = f"{BASE_URL}/search_dn/{display_name}"
        response = requests.get(url, timeout=5)
        return response
    except requests.exceptions.RequestException:
        return None

# Searches user by their username
def search_user_by_un(username):
    try:
        url = f"{BASE_URL}/search_un/{username}"
        response = requests.get(url, timeout=5)
        return response
    except requests.exceptions.RequestException:
        return None