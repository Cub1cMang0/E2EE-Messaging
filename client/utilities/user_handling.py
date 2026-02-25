from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import x25519
import base64
import asyncio
import os
import sys
import json
import requests
from PySide6.QtCore import QStandardPaths, QDir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from crytpo.protocol import send_message

# Uses to retrieve location of user's locally stored private key
def get_priv_key_dir(username):
    path = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)
    if not QDir(path).exists():
        QDir().mkpath(path)
    return os.path.join(path, f"{username}.dat")

# Gets fetches the server's public key
def get_server_pub_key() -> x25519.X25519PublicKey | None:
    try:
        response = requests.get("http://127.0.0.1:8000/pub_key", timeout=5)
        if response.status_code == 200:
            pub_hex = response.json().get("server_dh_public")
            pub_bytes = bytes.fromhex(pub_hex)
            return x25519.X25519PublicKey.from_public_bytes(pub_bytes)
        else:
            return None
    except requests.exceptions.ConnectionError:
        return None
    except Exception as e:
        return None

def gen_user_id():
    # Generates a private key for signing/identity
    id_priv_key = ed25519.Ed25519PrivateKey.generate()
    id_pub_bytes = id_priv_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    )
    # Generates a private key for encryption
    dh_priv_key = x25519.X25519PrivateKey.generate()
    dh_pub_bytes = dh_priv_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    )
    return id_priv_key, id_pub_bytes, dh_priv_key, dh_pub_bytes

# Creats, encrypts and stores new users' public key. Also locally stores new users' private key.
def handle_registration(username, display_name, password):
    id_priv_key, id_pub_bytes, dh_priv_key, dh_pub_bytes = gen_user_id()
    id_priv_bytes = id_priv_key.private_bytes(encoding=serialization.Encoding.Raw, 
        format=serialization.PrivateFormat.Raw, encryption_algorithm=serialization.NoEncryption()
    )
    dh_priv_bytes = dh_priv_key.private_bytes(encoding=serialization.Encoding.Raw, 
        format=serialization.PrivateFormat.Raw, encryption_algorithm=serialization.NoEncryption()
    )
    complete_priv_bytes = id_priv_bytes + dh_priv_bytes
    salt = os.urandom(16)
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=b"local-storage-encryption")
    storage_key = hkdf.derive(password.encode())
    aesgcm = AESGCM(storage_key)
    nonce = os.urandom(12)
    encrypted_priv_keys = aesgcm.encrypt(nonce, complete_priv_bytes, None)
    file_path = get_priv_key_dir(username)
    with open(file_path, "wb") as file:
        file.write(salt + nonce + encrypted_priv_keys)
    payload = {
        "username": username,
        "display_name": display_name,
        "id_pub_key": id_pub_bytes.hex(),
        "dh_pub_key": dh_pub_bytes.hex()
    }
    try:
        response = requests.post("http://127.0.0.1:8000/register", json=payload, timeout=5)        
        if response.status_code != 200:
            return {"success": False, "error": f"Server Error: {response.status_code}"}
        return {"success": True, "data": response.json()}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Server is offline. Check your connection."}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "The request timed out."}
    except Exception as e:
        return {"success": False, "error": f"An unexpected error occurred: {str(e)}"}

# Fetches users' private key and sends a payload to the server and attempts to log the users in.
def handle_login(username, password):
    file_path = get_priv_key_dir(username)
    if not os.path.exists(file_path):
        return {"success": False, "error": "User does not exist"}
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()
        salt = file_data[:16]
        nonce = file_data[16:28]
        enc_priv_keys = file_data[28:]
        hkdf = HKDF (algorithm=hashes.SHA256(), length=32, salt=salt, info=b"local-storage-encryption")
        storage_key = hkdf.derive(password.encode())
        aesgcm = AESGCM(storage_key)
        dec_bytes = aesgcm.decrypt(nonce, enc_priv_keys, None)
        id_priv_bytes = dec_bytes[:32]
        dh_priv_bytes = dec_bytes[32:]
        id_priv_key = ed25519.Ed25519PrivateKey.from_private_bytes(id_priv_bytes)
        dh_priv_key = x25519.X25519PrivateKey.from_private_bytes(dh_priv_bytes)
    except Exception:
        return {"success": False, "error": "Invalid password or data has been corrupted."}
    login_data = {
        "username": username,
        "action": "login"
    }
    plaintext_bytes = json.dumps(login_data).encode('utf-8')
    server_dh_public = get_server_pub_key()
    if not server_dh_public:
        return {"success": False, "error": "Fetching server public key failed."}
    try:
        e2ee_payload = send_message(
            plaintext=plaintext_bytes,
            sender_identity_private=id_priv_key,
            sender_dh_private=dh_priv_key,
            recipient_dh_public=server_dh_public,
            sender_id=username,
            recipient_id="server_main"
        )
        json_payload = {
            "ciphertext": base64.b64encode(e2ee_payload["ciphertext"]).decode('utf-8'),
            "nonce": base64.b64encode(e2ee_payload["nonce"]).decode('utf-8'),
            "signature": base64.b64encode(e2ee_payload["signature"]).decode('utf-8'),
            "sender_id": e2ee_payload["sender_id"],
            "recipient_id": e2ee_payload["recipient_id"]
        }        
        response = requests.post("http://127.0.0.1:8000/login", json=json_payload, timeout=5)        
        if response.status_code != 200:
            return {"success": False, "error": f"Server Error: {response.text}"}
        return {
            "success": True, 
            "data": response.json(),
            "private_key_loaded": True
        }
    except Exception as e:
        print(e)
        return {"success": False, "error": f"Encryption or network error: {str(e)}"}


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

