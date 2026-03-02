from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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

class Message(BaseModel): # add stuff to this as needed
    sender: str
    recipient: str
    content: str

class ConnectToUser(BaseModel): # can add key exchange
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

class ConnectionManager:
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}  # username -> websocket
        self.active_chats: Dict[str, str] = {}  # username -> who theyre talking to
    
    async def connect_to_server(self, websocket: WebSocket, username: str):
        """connect a user to the server"""
        await websocket.accept()
        self.connections[username] = websocket # add key gen stuff here
        return True
    
    async def connect_to_user(self, username: str, target_user: str): # add stuff to pass some kind of key to validate
        """Connect a user to chat with another user (both must be online)"""
        if target_user not in self.connections:
            return {"success": False, "error": f"{target_user} is not online"}
        
        if username not in self.connections:
            return {"success": False, "error": f"{username} is not online"}
        
        # set up the chat connection
        self.active_chats[username] = target_user
        
        # Notify both users
        connect_notification = { # add key exchange stuff
            "type": "chat_connected",
            "sender": "system",
            "message": f"Connected to {target_user}",
            "chat_partner": target_user
        }
        
        partner_notification = {
            "type": "chat_partner_connected",
            "sender": "system", 
            "message": f"{username} started a chat with you",
            "chat_partner": username
        }
        
        try:
            await self.connections[username].send_text(json.dumps(connect_notification))
            await self.connections[target_user].send_text(json.dumps(partner_notification))
        except:
            pass
            
        return {"success": True, "message": f"Connected to {target_user}"}
    
    def disconnect_from_server(self, username: str): # add stuff to pass some kind of key to validate
        if username not in self.connections:
            return
            
        chat_partner = self.active_chats.get(username)
        if chat_partner and chat_partner in self.connections:
            disconnect_notification = {
                "type": "chat_partner_disconnected",
                "sender": "system",
                "message": f"{username} disconnected from server"
            }
            try:
                import asyncio
                loop = asyncio.get_event_loop() 
                loop.create_task(self.connections[chat_partner].send_text(json.dumps(disconnect_notification)))
            except:
                pass
        
        del self.connections[username]
        if username in self.active_chats:
            del self.active_chats[username]
    
    async def send_message(self, message: Message): # add stuff to pass some kind of key to validate sender
        """Send a message from sender to recipient."""
        # check if both users are online
        # also need to check validate sender's identity, maybe make a separate parallel key between users and server
        if message.recipient not in self.connections:
            return {"success": False, "error": f"{message.recipient} is not online"}
        
        if message.sender not in self.connections:
            return {"success": False, "error": f"{message.sender} is not online"}
        
        message_data = {
            "type": "message",
            "sender": message.sender,
            "recipient": message.recipient,
            "content": message.content
        }
        
        # send to recipient
        try:
            await self.connections[message.recipient].send_text(json.dumps(message_data))
            return {"success": True, "message": "sent"}
        except:
            return {"success": False, "error": "Failed to send message"}

manager = ConnectionManager()

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
def health_check():
    return {"status": "messaging server running"}

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

@app.get("/users")
def get_online_users():
    """Get list of users"""
    return {"users": list(manager.connections.keys())}

# could include something specifying a new or returning user, where
# new users pass along a public key and returning users pass along an encrypted
# message using a key created from the server's public key (?)
@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    # change this entirely or add something that enables a login, still working
    await manager.connect_to_server(websocket, username)
    try:
        while True:
            # wait for message or action
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "connect_to_user":
                result = await manager.connect_to_user(username, message_data["target_user"])
                response = {"type": "connect_response", "data": result}
                await websocket.send_text(json.dumps(response))
                
            elif message_data.get("type") == "message":
                message = Message(
                    sender=message_data["sender"],
                    recipient=message_data["recipient"],
                    content=message_data["content"]
                )
                await manager.send_message(message)
                
    except WebSocketDisconnect:
        manager.disconnect_from_server(username)
