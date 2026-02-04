import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from app_gui import Ui_main_window
from register_gui import Ui_Dialog
from user_handling import handle_registration
from add_new_gc import Ui_add_gc_window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
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
        self.dialog = QDialog(self)
        self.add_new_gc = Ui_add_gc_window()
        self.add_new_gc.setupUi(self.dialog)
        self.dialog.show()

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.register_button.clicked.connect(self.register_user)
        self.authenticated = False
    
    def register_user(self):
        username = self.ui.username.text()
        password = self.ui.password.text()
        display_name = self.ui.display_name.text()
        response = handle_registration(username, display_name, password)
        if response.status_code == 200:
            self.handle_login_success()

    def handle_login_success(self):
        self.authenticated = True
        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    if login.exec() == QDialog.Accepted:
        window = MainWindow()
        window.show()
    else:
        sys.exit(0)