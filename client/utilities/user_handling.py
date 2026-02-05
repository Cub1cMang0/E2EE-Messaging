from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import asyncio
import os
import requests

def gen_user_id():
    # Generates a private key for signing/identity
    priv_key = ed25519.Ed25519PrivateKey.generate()
    pub_key = priv_key.public_key()
    # Serialization of public key for the server
    pub_bytes = pub_key.public_bytes(encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw)
    return priv_key, pub_bytes

def handle_registration(username, display_name, password):
    priv_key, pub_bytes = gen_user_id()
    pub_hex = pub_bytes.hex()
    salt = os.urandom(16)
    priv_bytes = priv_key.private_bytes(encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw, encryption_algorithm=serialization.NoEncryption()
    )
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=b"local-storage-encryption")
    storage_key = hkdf.derive(password.encode())
    aesgcm = AESGCM(storage_key)
    nonce = os.urandom(12)
    encrypted_priv_key = aesgcm.encrypt(nonce, priv_bytes, None)
    with open(f"{username}.dat", "wb") as file:
        file.write(salt + nonce + encrypted_priv_key)
    payload = {
        "username": username,
        "display_name": display_name,
        "pub_key": pub_hex
    }
    response = requests.post("http://127.0.0.1:8000/register", json=payload)
    return response

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

