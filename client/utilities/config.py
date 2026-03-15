_mode = "local"

URLS = {
    "local": "http://127.0.0.1:8000",
    "server": "https://chat.yoshi.red"
}

def set_mode(mode: str):
    global _mode
    _mode = mode

def get_mode():
    return _mode

def get_base_url():
    return URLS[_mode]
