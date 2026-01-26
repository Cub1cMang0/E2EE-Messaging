import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from app_gui import Ui_main_window
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())