from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict
import json

app = FastAPI()

class Message(BaseModel): # add stuff to this as needed
    sender: str
    recipient: str
    content: str

class ConnectToUser(BaseModel): # can add key exchange
    username: str
    target_user: str

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

@app.get("/")
def health_check():
    return {"status": "messaging server running"}

@app.post("/send")
async def send_message(message: Message):
    """send message"""
    result = await manager.send_message(message)
    return result

@app.post("/connect")
async def connect_to_user(connection: ConnectToUser):
    result = await manager.connect_to_user(connection.username, connection.target_user)
    return result

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
