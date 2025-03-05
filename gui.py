from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class JarvisUI(QWidget):
    def __init__(self, start_listening_callback):
        super().__init__()
        self.start_listening_callback = start_listening_callback
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Jarvis AI Assistant")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QPushButton {
                background-color: #0d47a1;
                border: none;
                border-radius: 5px;
                padding: 10px;
                min-width: 100px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QLabel {
                font-size: 16px;
                padding: 10px;
            }
        """)

        # Create widgets
        self.status_label = QLabel("Press the button and speak", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        
        self.speak_button = QPushButton("Speak", self)
        self.speak_button.clicked.connect(self.handle_speak_button)
        
        # Layout
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.status_label)
        layout.addWidget(self.speak_button)
        layout.addStretch()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def handle_speak_button(self):
        self.speak_button.setEnabled(False)
        self.status_label.setText("Listening...")
        self.start_listening_callback()
        self.speak_button.setEnabled(True)

    def update_status(self, text):
        self.status_label.setText(text)
