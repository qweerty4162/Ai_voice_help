from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTextEdit
from client.input.voice_thread import VoiceThread


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Voice Assistant")

        self.text = QTextEdit()
        self.button = QPushButton("Говорить")

        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.button.clicked.connect(self.start_listening)

    def start_listening(self):
        self.text.append("🎤 Слушаю...")
        self.thread = VoiceThread()
        self.thread.recognized.connect(self.on_text)
        self.thread.start()

    def on_text(self, text):
        self.text.append(f"🗣 {text}")
