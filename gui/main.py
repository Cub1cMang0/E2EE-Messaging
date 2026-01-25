import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from app_gui import Ui_main_window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        self.ui.message_log.setReadOnly(True)
        self.ui.send_button.clicked.connect(self.send_clicked)

    def send_clicked(self):
        user_text = self.ui.texting_box.toPlainText()
        if user_text:
            self.ui.message_log.append(f"<p align='right'>You: {user_text}\n</p>")
            self.ui.texting_box.clear()
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())