from cryptography.hazmat.primatives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import asyncio

def gen_user_id():
    # Generates a private key for signing/identity
    priv_key = ed25519.Ed25519PrivateKey.generate()
    pub_key = priv_key.public_key()
    # Serialization of public key for the server
    pub_bytes = pub_key.public_bytes(encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw)
    return priv_key, pub_bytes

class ChatServer:
    def __init__(self):
        self.users = {}

    async def registration_handler(self, username, pub_key):
        if username in self.users:
            return "Error: Username is taken"
        self.users[username] = pub_key
        return "Success"
    async def search_user(self, username):
        return self.users.get(username, None)

