from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict
import os
import base64
from client.utilities.database import SessionLocal, User
from crytpo.protocol import receive_message, MessagePayload
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

app = FastAPI()
SERVER_KEY_FILE = "server_dh_key.dat"

class UserRegister(BaseModel):
    username: str
    display_name: str
    id_pub_key: str
    dh_pub_key: str

# Mirrors MessagePayload
class UserLogin(BaseModel):
    ciphertext: bytes | str
    nonce: bytes | str
    signature: bytes | str
    sender_id: str
    recipient_id: str

class CreateGroup(BaseModel):
    creator: str
    members: List[str]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_server_key() -> x25519.X25519PrivateKey:
    if os.path.exists(SERVER_KEY_FILE):
        with open(SERVER_KEY_FILE, "rb") as file:
            priv_bytes = file.read()
            return x25519.X25519PrivateKey.from_private_bytes(priv_bytes)
    else:
        priv_key = x25519.X25519PrivateKey.generate()
        with open (SERVER_KEY_FILE, "wb") as file:
            file.write(priv_key.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption()
            ))
        return priv_key

def get_client_pub_keys(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise ValueError("User not found in database")
    id_bytes = bytes.fromhex(user.id_pub_key)
    dh_bytes = bytes.fromhex(user.dh_pub_key)
    id_public = ed25519.Ed25519PublicKey.from_public_bytes(id_bytes)
    dh_public = x25519.X25519PublicKey.from_public_bytes(dh_bytes)
    return id_public, dh_public

server_dh_private = get_server_key()
server_dh_public = server_dh_private.public_key()

@app.get("/")
def read_root():
    return {"status": "Chat Server Online"}

@app.get("/pub_key")
def get_public_key():
    pub_key = server_dh_private.public_key()
    pub_bytes = pub_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    return {"server_dh_public": pub_bytes.hex()}

@app.post("/register")
async def register_user(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exist")
    new_user = User(username=user.username,
        display_name=user.display_name,
        id_pub_key=user.id_pub_key,
        dh_pub_key=user.dh_pub_key
    )
    db.add(new_user)
    db.commit()
    return {"message": f"User {user.username} has been registered"}

@app.post("/login")
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    try:
        try:
            client_identity_public, client_dh_public, = get_client_pub_keys(db, payload.sender_id)
        except ValueError:
            raise HTTPException(status_code=404, detail="Sender not found in database.")
        raw_payload: MessagePayload = {
            "ciphertext": base64.b64decode(payload.ciphertext),
            "nonce": base64.b64decode(payload.nonce),
            "signature": base64.b64decode(payload.signature),
            "sender_id": payload.sender_id,
            "recipient_id": payload.recipient_id,
        }
        plaintext_bytes = receive_message(
            payload=raw_payload,
            receiver_dh_private=server_dh_private,
            sender_identity_public=client_identity_public,
            sender_dh_public=client_dh_public
        )
        plain_text = plaintext_bytes.decode('utf-8')
        return {
            "status": "success",
            "message": "Login payload has been successfully decrypted",
            "decrypted_data": plain_text
        }
    except HTTPException:
        raise HTTPException(status_code=404, detail="Sender not found in database.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication or decryption failed: {str(e)}")

@app.get("/search/{username}")
async def search_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return {
        "username": user.username,
        "display_name": user.display_name,
        "pub_key": user.pub_key
    }

@app.post("/group/begin")
async def begin_group(group: CreateGroup):
    keys = {}
    for member in group.members:
        user = db.query(User).filter(User.username == member).first()
        if user:
            keys[member] = user.pub_key
        else:
            keys[member] = "N/A"
    return {"group_members": keys}