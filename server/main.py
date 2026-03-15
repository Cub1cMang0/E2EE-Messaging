from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Dict
import os
import json
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
import base64
from client.utilities.database import SessionLocal, User, Group, Group_Member, Group_Create
from crypto.protocol import receive_message, MessagePayload
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ConnectionManager:
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}  # username -> websocket
    
    async def connect_to_server(self, websocket: WebSocket, username: str):
        """connect a user to the server"""
        await websocket.accept()
        self.connections[username] = websocket # add key gen stuff here
        return True
    
    def disconnect_from_server(self, username: str):
        """Remove user from connections"""
        if username in self.connections:
            del self.connections[username]
    
    # send a raw message to a recipient (using this for all message sends now)
    async def send_raw(self, recipient: str, data: dict):
        if recipient not in self.connections:
            return {"success": False, "error": f"{recipient} is not online"}
        try:
            await self.connections[recipient].send_text(json.dumps(data))
            return {"success": True, "message": "sent"}
        except:
            return {"success": False, "error": "Failed to send message"}

manager = ConnectionManager()

# Used to fetch server key (or create if it doesn't exist)
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

# Used to query for a user's public keys from the database
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

# Used to send the server's public key for communication
@app.get("/pub_key")
def get_public_key():
    pub_key = server_dh_private.public_key()
    pub_bytes = pub_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    return {"server_dh_public": pub_bytes.hex()}

# Used to attempt to register and store a user in the database
@app.post("/register")
async def register_user(user: UserRegister, db: Session = Depends(get_db)):
    existing_username = db.query(User).filter(User.username == user.username).first()
    existing_display_name = db.query(User).filter(User.display_name == user.display_name).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already exist")
    elif existing_display_name:
        raise HTTPException(status_code=400, detail="Display name already exist")
    new_user = User(username=user.username,
        display_name=user.display_name,
        id_pub_key=user.id_pub_key,
        dh_pub_key=user.dh_pub_key
    )
    db.add(new_user)
    db.commit()
    return {
        "message": f"User {user.username} has been registered",
        "username": user.username,
        "display_name": user.display_name
    }
# Used to attempt to login a user
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
        user = db.query(User).filter(User.username == payload.sender_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found in database")
        return {
            "status": "success",
            "message": "Login payload has been successfully decrypted",
            "decrypted_data": plain_text,
            "username": user.username,
            "display_name": user.display_name
        }
    except HTTPException:
        raise HTTPException(status_code=404, detail="Sender not found in database.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication or decryption failed: {str(e)}")

# Searches for a user by display name
@app.get("/search_dn/{display_name}")
async def search_display_name(display_name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.display_name == display_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return {
        "username": user.username,
        "display_name": user.display_name,
        "id_pub_key": user.id_pub_key,
        "dh_pub_key": user.dh_pub_key
    }

@app.get("/search_un/{username}")
async def search_username(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return {
        "username": user.username,
        "display_name": user.display_name,
        "id_pub_key": user.id_pub_key,
        "dh_pub_key": user.dh_pub_key
    }

# Used to create a group chat and store it in the database
@app.post("/groups/create")
async def create_group_chat(group_data: Group_Create, db: Session = Depends(get_db)):
    creator = db.query(User).filter(User.display_name == group_data.creator_display_name).first()
    if not creator:
        raise HTTPException(status_code=404, detail="Creator user not found")
    # v Used to ensure no true duplicate chats are created
    members = db.query(User).filter(User.display_name.in_(group_data.members_display_names)).all()
    target_user_ids = {u.id for u in members}
    target_user_ids.add(creator.id)
    potential_groups = db.query(Group_Member.group_id).filter(Group_Member.user_id == creator.id).all()
    potential_group_ids = [g[0] for g in potential_groups]
    for g_id in potential_group_ids:
        existing_member_ids = {m.user_id for m in db.query(Group_Member).filter(Group_Member.group_id == g_id).all()}
        if existing_member_ids == target_user_ids:
            existing_group = db.query(Group).filter(Group.id == g_id).first()
            if existing_group.chat_name == group_data.name:
                raise HTTPException(status_code=400, detail=f"A group named '{group_data.name}' with these exact members alreday exists")
    # ^ Used to ensure no true duplicate group chats are created
    new_group = Group(
        chat_name=group_data.name,
        creator=creator.id
    )
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    admin_member = Group_Member(
        group_id=new_group.id,
        user_id=creator.id,
        role="admin"
    )
    db.add(admin_member)
    for display_name in group_data.members_display_names:
        if display_name == creator.display_name:
            continue            
        user = db.query(User).filter(User.display_name == display_name).first()
        if user:
            new_member = Group_Member(
                group_id=new_group.id,
                user_id=user.id,
                role="member"
            )
            db.add(new_member)
        else:
            print(f"Warning: User {display_name} not found, skipping.")
    db.commit()
    return {
        "success": True, 
        "message": f"Group '{new_group.chat_name}' created successfully!",
        "group_id": new_group.id
    }

# Used to fetch the user's group chats that they are a part of during login
@app.get("/users/{display_name}/groups")
def get_user_gcs(display_name: str, requester: str, signature: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.display_name == display_name).first()
    requester_user = db.query(User).filter(User.display_name == requester).first()
    
    if not user or not requester_user:
        raise HTTPException(status_code=404, detail="User does not exist")
    
    # verify identiy of requesting user

    if requester_user.id != user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    try:
        pub_key = ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(requester_user.id_pub_key))
        pub_key.verify(base64.b64decode(signature), requester.encode())
    except:
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    user_group_chats = db.query(Group).join(Group_Member).filter(Group_Member.user_id == user.id).all()
    group_chats_data = [{"group_id": g.id, "name": g.chat_name} for g in user_group_chats]
    return {"success": True, "group_chats": group_chats_data}

# Fetch a single group chat (used to add newly created group chats dynamically to the GUI)
@app.get("/groups/{group_id}")
async def get_single_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")        
    return {
        "id": group.id,
        "chat_name": group.chat_name,
        "created_on": group.created_on.isoformat() if group.created_on else None
    }

@app.get("/users")
def get_online_users():
    """Get list of users"""
    return {"users": list(manager.connections.keys())}

@app.get("/groups/{group_id}/members")
async def get_group_members(group_id: int, db: Session = Depends(get_db)):
    """Get display names of all members in a group"""
    members = db.query(User.display_name).join(Group_Member).filter(Group_Member.group_id == group_id).all()
    if not members:
        raise HTTPException(status_code=404, detail="Group not found")
    return {"members": [m[0] for m in members]}

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
            
            if message_data.get("type") == "message":
                # message_data["payload"] is a dict like MessagePayload but base64-encoded
                await manager.send_raw(message_data["recipient"], {
                    "type": "message",
                    "sender": username,
                    "payload": message_data["payload"],
                })

                # message = Message(
                #     sender=message_data["sender"],
                #     recipient=message_data["recipient"],
                #     content=message_data["content"]
                # )
                # await manager.send_message(message)
                
    except WebSocketDisconnect:
        manager.disconnect_from_server(username)
