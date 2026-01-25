import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTextEdit, QLineEdit, QPushButton,
                               QSizePolicy)
from PySide6.QtGui import QAction

class FullScreenMessenger(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desktop Messenger")
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen_geometry.width() * 0.7), int(screen_geometry.height() * 0.7))
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet("font-size: 16px;") 
        self.chat_history.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_layout.addWidget(self.chat_history)
        self.input_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.setStyleSheet("font-size: 14px; padding: 5px;")
        self.message_input.returnPressed.connect(self.send_message)
        self.input_layout.addWidget(self.message_input)
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("font-size: 14px; padding: 5px;")
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)
        self.main_layout.addLayout(self.input_layout)


    def send_message(self):
        user_text = self.message_input.text().strip()
        if user_text:
            self.chat_history.append(f"<b>You:</b> {user_text}")
            self.message_input.clear()
            self.receive_message(f"Echo: {user_text}")

    def receive_message(self, text):
        self.chat_history.append(f"<span style='color: blue'><b>Friend:</b> {text}</span>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FullScreenMessenger()
    window.showMaximized() 
    sys.exit(app.exec())