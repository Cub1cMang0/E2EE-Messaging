import sys
import os
import re
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QLineEdit
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from app_gui import Ui_main_window
from register_gui import Ui_Dialog
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.user_handling import handle_registration, handle_login
from utilities.search_utility import search_user
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
    def __init__(self):
        super().__init__()
        self.ui = Ui_main_window()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.ui.setupUi(self.central_widget)
        self.setWindowTitle("E2EE Messaging")
        self.ui.message_log.setReadOnly(True)
        self.ui.send_button.clicked.connect(self.send_clicked)
        self.ui.add_group_button.clicked.connect(self.add_new_group_chat)

    # Sends messages to the chat 
    def send_clicked(self):
        user_text = self.ui.texting_box.toPlainText()
        if user_text:
            self.ui.message_log.append(f"<p align='right'>You: {user_text}\n</p>")
            self.ui.texting_box.clear()

    # Opens a new window where the user adds other user's to a new group chat
    def add_new_group_chat(self):
        dialog = AddNewGC_Window(self)
        dialog.show()

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
            self.handle_login_success()
        else:
            self.ui.error_label_l.show()
            self.ui.error_label_l.setText(response["error"])
        
    def handle_login_success(self):
        self.authenticated = True
        self.accept()

class AddNewGC_Window(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_add_gc_window()
        self.ui.setupUi(self)
        self.ui.search_button.clicked.connect(self.search_user)
        self.ui.error_label.hide()

    def search_user(self):
        display_name = self.ui.user_search_box.text().strip()
        if not display_name:
            return
        response = search_user(display_name)
        if response is None:
            self.ui.error_label.show()
            self.ui.error_label.setText("Server is offline")
            return
        if response.status_code == 200:
            user_data = response.json()
            self.ui.user_list.addItem(user_data['display_name'])
        elif response.status_code == 404:
            self.ui.error_label.show()
            self.ui.error_label.setText("User does not exist")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_register_window = Login_Register_Window()
    if login_register_window.exec() == QDialog.DialogCode.Accepted:
        main_chat = MainWindow()
        main_chat.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)
