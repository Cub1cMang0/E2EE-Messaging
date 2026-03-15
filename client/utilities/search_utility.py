import requests
from .config import get_base_url

# Searches user by their display name
def search_user_by_dn(display_name):
    """Asks the server to search for the user by display name."""
    try:
        base_url = get_base_url()
        url = f"{base_url}/search_dn/{display_name}"
        response = requests.get(url, timeout=5)
        return response
    except requests.exceptions.RequestException:
        return None

# Searches user by their username
def search_user_by_un(username):
    try:
        base_url = get_base_url()
        url = f"{base_url}/search_un/{username}"
        response = requests.get(url, timeout=5)
        return response
    except requests.exceptions.RequestException:
        return None