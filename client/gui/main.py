import sys
import os
import re
import json
import requests
from cryptography.hazmat.primitives.asymmetric import ed25519, x25519
from cryptography.hazmat.primitives import serialization
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QLineEdit, QListWidgetItem
from PySide6.QtCore import QRegularExpression, Qt, Signal as pyqtSignal
from PySide6.QtGui import QRegularExpressionValidator
from app_gui import Ui_main_window
from register_gui import Ui_Dialog
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.user_handling import handle_registration, handle_login, handle_gc_creation, fetch_user_gcs, fetch_gc
from utilities.search_utility import search_user_by_dn, search_user_by_un
from utilities.ws_client import PersistentWebSocketClient
from utilities.config import set_mode, get_base_url
from utilities.database import save_message, get_messages
from add_new_gc import Ui_add_gc_window
# These are used as guidelines for users on what they can add to their credentials
# (What they can and can't have in thier username/password/displayname)
user_regex = QRegularExpression("^[a-zA-Z0-9_]{8,32}$")
user_validator = QRegularExpressionValidator(user_regex)

display_regex = QRegularExpression("^[a-zA-Z0-9 ]{6,32}$")
display_validator = QRegularExpressionValidator(display_regex)

password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,64}$"

RESERVED_NAMES = ["admin", "root", "support", "moderator", "staff", "system"]

class MainWindow(QMainWindow):
    def __init__(self, username, display_name, id_priv_key, dh_priv_key):
        super().__init__()
        self.username = username
        self.display_name = display_name
        self.id_priv_key = id_priv_key  # ed25519 private key
        self.dh_priv_key = dh_priv_key  # x25519 private key
        self.current_group_id = None
        self.current_recipient = None
        
        # Create persistent WebSocket client
        self.ws_client = PersistentWebSocketClient(username, id_priv_key, dh_priv_key)
        self.ws_client.message_received.connect(self.on_message_received)
        self.ws_client.error_occurred.connect(self.on_ws_error)
        self.ws_client.start()
        
        self.ui = Ui_main_window()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.ui.setupUi(self.central_widget)
        self.setWindowTitle("E2EE Messaging")
        self.ui.message_log.setReadOnly(True)
        self.ui.send_button.clicked.connect(self.send_clicked)
        self.ui.add_group_button.clicked.connect(self.open_add_gc_window)
        self.ui.refresh_gc_button.clicked.connect(self.refresh_group_chats)
        self.ui.gc_list.itemClicked.connect(self.on_chat_selected)

    def on_chat_selected(self, item):
        """Handle group chat selection"""
        group_id = item.data(Qt.ItemDataRole.UserRole)
        self.current_group_id = group_id
        self.ui.message_log.clear()
        self.load_messages_from_db(group_id)
        self.setup_chat_for_group(group_id)

    def refresh_group_chats(self):
        """Refresh the list of group chats to check for new additions"""
        if self.display_name:
            self.load_group_chats(self.display_name)

    def load_messages_from_db(self, group_id):
        """Load messages from database and display them"""
        try:
            response = get_messages(group_id)
            if response["success"]:
                messages = response["messages"]
                for msg in messages:
                    self.ui.message_log.append(f"<p>{msg.sender}: {msg.text}</p>")
        except Exception as e:
            self.ui.message_log.append(f"<p style='color:red'>Error loading messages: {str(e)}</p>") #fancy error text

    def setup_chat_for_group(self, group_id):
        """Fetch other user in group and register with persistent WebSocket"""
        try:
            # Get group member
            response = requests.get(f"{get_base_url()}/groups/{group_id}/members", timeout=5)
            if response.status_code != 200:
                self.ui.message_log.append("<p style='color:red'>Failed to connect to chat</p>")
                return
            members = response.json()["members"]
            # Find the other user (not self)
            recipient_display_name = next((m for m in members if m != self.display_name), None) #gets other user
            if not recipient_display_name:
                self.ui.message_log.append("<p style='color:red'>Could not find chat partner</p>")
                return
            
            self.current_recipient = recipient_display_name
            
            # fetch recipients keys
            response = requests.get(f"{get_base_url()}/search_dn/{recipient_display_name}", timeout=5)
            if response.status_code != 200:
                self.ui.message_log.append("<p style='color:red'>Failed to find recipient</p>")
                return
            recipient_data = response.json()
            # convert hex keys to key objects
            id_pub_bytes = bytes.fromhex(recipient_data["id_pub_key"])
            dh_pub_bytes = bytes.fromhex(recipient_data["dh_pub_key"])
            recipient_id_pub = ed25519.Ed25519PublicKey.from_public_bytes(id_pub_bytes)
            recipient_dh_pub = x25519.X25519PublicKey.from_public_bytes(dh_pub_bytes)
            
            # register user with client
            self.ws_client.register_user(recipient_display_name, group_id, recipient_dh_pub, recipient_id_pub)
        except Exception as e:
            self.ui.message_log.append(f"<p style='color:red'>Error: {str(e)}</p>")

    def on_message_received(self, message_data):
        """Display received message if its from the current chat"""
        group_id = message_data.get("group_id")
        # only display if this message is for the currently focused chat
        if group_id == self.current_group_id:
            sender = message_data["sender"]
            text = message_data["text"]
            self.ui.message_log.append(f"<p>{sender}: {text}</p>")

    def on_ws_error(self, error_msg):
        """Display WebSocket errors"""
        self.ui.message_log.append(f"<p style='color:red'>Error: {error_msg}</p>")

    # Used to establish a signal when a new group chat is created for dynamic updating
    def open_add_gc_window(self):
        self.add_win = AddNewGC_Window(self.display_name)
        self.add_win.new_gc_created.connect(self.refresh_gcs) 
        self.add_win.show()

    # Fetches and adds new group chat
    def refresh_gcs(self, group_id):
        response = fetch_gc(group_id)
        if response["success"]:
            gc_data = response["result"]
            chat_item = QListWidgetItem(gc_data["chat_name"])
            chat_item.setData(Qt.ItemDataRole.UserRole, gc_data["id"])            
            self.ui.gc_list.addItem(chat_item)            
            self.ui.gc_list.setCurrentItem(chat_item)

    # Sends messages to the chat 
    def send_clicked(self):
        user_text = self.ui.texting_box.toPlainText()
        if user_text and self.current_recipient:
            self.ui.message_log.append(f"<p align='right'>You: {user_text}</p>")
            # Save message to database
            if self.current_group_id:
                save_message(self.current_group_id, "You", user_text)
            # Send via persistent client
            self.ws_client.ws_send_message(self.current_recipient, user_text)
            self.ui.texting_box.clear()

    # Loads all of the user's group chats
    def load_group_chats(self, display_name):
        self.ui.gc_list.clear()
        response = fetch_user_gcs(display_name, self.username, self.id_priv_key)
        if response.get("success"):
            group_chats = response.get("group_chats")
            for gc in group_chats:
                chat = QListWidgetItem(gc["name"])
                chat.setData(Qt.ItemDataRole.UserRole, gc["group_id"])
                self.ui.gc_list.addItem(chat)
        else:
            #  error message if refresh fails
            error_msg = response.get("error", "Failed to load group chats")
            self.ui.gc_list.addItem(f"Error: {error_msg}")

    def closeEvent(self, event):
        """clean up when closing the window"""
        if self.ws_client:
            self.ws_client.stop()
        event.accept() # so it doesnt break

class Login_Register_Window(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.username_r.setValidator(user_validator)
        self.ui.username_l.setValidator(user_validator)
        self.ui.display_name.setValidator(display_validator)
        self.ui.password_r.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.password_l.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.register_button.clicked.connect(self.register_user)
        self.ui.login_button.clicked.connect(self.login_user)
        self.ui.register_2_login.clicked.connect(lambda: self.ui.login_register_window.setCurrentIndex(1))
        self.ui.login_2_register.clicked.connect(lambda: self.ui.login_register_window.setCurrentIndex(0))
        self.ui.login_register_window.setCurrentIndex(1)
        self.ui.error_label_l.hide()
        self.ui.error_label_r.hide()
        self.authenticated = False
        self.registered = False
        self.login_response = None
    
    # Extracts registration info from GUI and sends it to server (handle registration) and display errors (if any)
    def register_user(self):
        username = self.ui.username_r.text()
        password = self.ui.password_r.text()
        display_name = self.ui.display_name.text()
        if username.lower() in RESERVED_NAMES:
            self.ui.error_label_r.show()
            self.ui.error_label_r.setText("Your username contains a banned phrase")
        elif re.match(password_regex, password):
            response = handle_registration(username, display_name, password)
            if response["success"]:
                self.login_response = response
                self.handle_login_success()
            else:
                self.ui.error_label_r.show()
                self.ui.error_label_r.setText(response['error'])
        else:
            self.ui.error_label_r.show()
            self.ui.error_label_r.setText("Password must be 8+ chars with upper, lower, number, and symbol.")

    # Extracts login info from GUI and checks with the server and displays errors (if any)
    def login_user(self):
        username = self.ui.username_l.text()
        password = self.ui.password_l.text()
        response = handle_login(username, password)
        if response["success"]:
            self.login_response = response
            self.handle_login_success()
        else:
            self.ui.error_label_l.show()
            self.ui.error_label_l.setText(response["error"])
    
    # ...logs in the user
    def handle_login_success(self):
        self.authenticated = True
        self.accept()

class AddNewGC_Window(QDialog):
    new_gc_created = pyqtSignal(int)

    def __init__(self, display_name, parent=None):
        super().__init__(parent)
        self.ui = Ui_add_gc_window()
        self.ui.setupUi(self)
        self.ui.search_button.clicked.connect(self.search_user)
        self.ui.create_gc_button.clicked.connect(self.create_gc)
        self.ui.error_label.hide()
        self.display_name = display_name
        self.ui.group_chat_name.setValidator(user_validator)

    # Searches for the specified user and adds them to the group chat members list
    def search_user(self):
        display_name = self.ui.user_search_box.text().strip()
        if not display_name:
            return
        duplicate_user = self.ui.user_list.findItems(display_name, Qt.MatchExactly)
        if not duplicate_user:
            response = search_user_by_dn(display_name)
            if response is None:
                self.ui.error_label.setText("Server is offline")
                self.ui.error_label.show()
            elif response.status_code == 200:
                user_data = response.json()
                self.ui.user_list.clear()
                self.ui.user_list.addItem(user_data['display_name'])
            elif response.status_code == 404:
                self.ui.error_label.setText("User does not exist")
                self.ui.error_label.show()
        else:
            self.ui.error_label.setText("User already in group chat list")
            self.ui.error_label.show()

    # Creates a new group chat (true duplicates not allowed)
    def create_gc(self):
        group_chat_name = self.ui.group_chat_name.text()
        creator_d_name = self.display_name
        display_name_list = [self.ui.user_list.item(x).text() for x in range(self.ui.user_list.count())]
        if group_chat_name.strip() != "" and len(display_name_list) != 0:
            response = handle_gc_creation(group_chat_name, creator_d_name, display_name_list)
            if response["success"]:
                self.ui.user_list.clear()
                self.ui.error_label.setText(f"Successfully created {group_chat_name}")
                self.ui.error_label.show()
                new_id = response["data"].get("group_id")
                self.new_gc_created.emit(new_id)
            else:
                self.ui.error_label.setText(f"{response["error"]}")
                self.ui.error_label.show()
        else:
            self.ui.error_label.setText("Cannot create group chat with empty fields")
            self.ui.error_label.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        mode = "local"

    mode = sys.argv[1].lower()

    set_mode(mode)
    
    print(f"Starting client in {mode.upper()} mode")
    
    app = QApplication(sys.argv)
    login_register_window = Login_Register_Window()
    if login_register_window.exec() == QDialog.DialogCode.Accepted:
        # use the login response from the dialog (already called handler during login)
        login_response = login_register_window.login_response
        
        if login_response and login_response.get("success"):
            id_priv_key = login_response.get("id_priv_key")
            dh_priv_key = login_response.get("dh_priv_key")
            user_data = login_response.get("data", {})
            
            main_chat = MainWindow(
                username=user_data.get("username"),
                display_name=user_data.get("display_name"),
                id_priv_key=id_priv_key,
                dh_priv_key=dh_priv_key
            )
            main_chat.load_group_chats(main_chat.display_name)
            main_chat.show()
            sys.exit(app.exec())
    else:
        sys.exit(0)
