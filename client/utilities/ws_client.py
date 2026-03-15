import asyncio
import json
import base64
import sys
import os
import websockets
from PySide6.QtCore import QThread, Signal

# apparently need this so crypto stuff can be imported (because of directory stuff)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from crypto.protocol import send_message, receive_message
from .config import get_base_url
from .database import save_message

class PersistentWebSocketClient(QThread):
    """Persistent WebSocket client that handles multiple recipients and saves all messages"""
    message_received = Signal(dict)
    connected = Signal()
    disconnected = Signal()
    error_occurred = Signal(str)

    def __init__(self, username, sender_id_priv, sender_dh_priv):
        super().__init__()
        self.username = username
        self.sender_id_priv = sender_id_priv
        self.sender_dh_priv = sender_dh_priv
        self.ws = None
        self.loop = None
        self.running = True
        
        # maps names to keys to handle multiple group chats
        self.user_crypto_map = {}

    def run(self):
        """start asyncio event loop"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect())

    async def connect(self):
        """Connect to websocket server"""
        url = get_base_url().replace("http", "ws") #for websocket connection
        try:
            async with websockets.connect(f"{url}/ws/{self.username}") as ws:
                self.ws = ws
                self.connected.emit()
                
                # Listen for messages from all users
                while self.running:
                    try:
                        msg = await ws.recv()
                        data = json.loads(msg)
                        
                        if data.get("type") == "message":
                            await self.decrypt_and_save(data)
                    except asyncio.CancelledError:
                        break
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.disconnected.emit()

    async def decrypt_and_save(self, data):
        """Decrypt message save to database and emit signal"""
        try:
            sender = data.get("sender")
            
            # check if there are crypto keys for this sender
            if sender not in self.user_crypto_map:
                return
            
            user_info = self.user_crypto_map[sender]
            recipient_dh_pub = user_info["dh_pub"]
            recipient_id_pub = user_info["id_pub"]
            group_id = user_info["group_id"]
            
            payload = data["payload"]
            raw_payload = {
                "ciphertext": base64.b64decode(payload["ciphertext"]),
                "nonce": base64.b64decode(payload["nonce"]),
                "signature": base64.b64decode(payload["signature"]),
            }
            plaintext = receive_message(
                raw_payload,
                receiver_dh_private=self.sender_dh_priv,
                sender_identity_public=recipient_id_pub,
                sender_dh_public=recipient_dh_pub
            )
            
            text = plaintext.decode('utf-8')
            
            # Save to database
            save_message(group_id, sender, text)
            
            # Emit signal for ui
            self.message_received.emit({
                "sender": sender,
                "text": text,
                "group_id": group_id
            })
        except Exception as e:
            self.error_occurred.emit(f"Decryption failed for {sender}: {str(e)}")

    def register_user(self, user_display_name, group_id, recipient_dh_pub, recipient_id_pub):
        """Register a users crypto keys for message decryption if doesnt already exist"""
        # skip if already registered with identical keys
        if user_display_name in self.user_crypto_map:
            existing = self.user_crypto_map[user_display_name]
            if (existing["dh_pub"] == recipient_dh_pub and 
                existing["id_pub"] == recipient_id_pub):
                return
        
        self.user_crypto_map[user_display_name] = {
            "dh_pub": recipient_dh_pub,
            "id_pub": recipient_id_pub,
            "group_id": group_id
        }

    def ws_send_message(self, recipient, text):
        """Send encrypted message to a specific recipient"""
        if not self.loop or not self.loop.is_running():
            return
        try:
            payload = send_message( #from crypto
                text.encode('utf-8'),
                sender_identity_private=self.sender_id_priv,
                sender_dh_private=self.sender_dh_priv,
                recipient_dh_public=self.user_crypto_map[recipient]["dh_pub"],
                sender_id=self.username,
                recipient_id=recipient
            )
            msg = {
                "type": "message",
                "recipient": recipient,
                "payload": {
                    "ciphertext": base64.b64encode(payload["ciphertext"]).decode(),
                    "nonce": base64.b64encode(payload["nonce"]).decode(),
                    "signature": base64.b64encode(payload["signature"]).decode(),
                }
            }
            asyncio.run_coroutine_threadsafe(self.ws.send(json.dumps(msg)), self.loop)
        except Exception as e:
            self.error_occurred.emit(str(e))

    def stop(self):
        """Stop WebSocket connection"""
        self.running = False
        if self.ws and self.loop and self.loop.is_running():
            try:
                asyncio.run_coroutine_threadsafe(self.ws.close(), self.loop)
            except:
                pass
