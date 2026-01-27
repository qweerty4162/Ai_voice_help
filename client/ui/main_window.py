from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTextEdit
from client.input.voice_thread import VoiceThread
from client.output.tts import speak
import requests

SERVER_URL = "http://127.0.0.1:8000/command"

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Voice Assistant")
        self.resize(500, 400)

        self.text = QTextEdit()
        self.button = QPushButton("🎤 Говорить")

        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.button.clicked.connect(self.start_listening)

    def start_listening(self):
        self.text.append("🎧 Слушаю...")
        self.thread = VoiceThread()
        self.thread.recognized.connect(self.on_text)
        self.thread.start()

    def on_text(self, text: str):
        if not text:
            self.text.append("❌ Ничего не распознано")
            return

        self.text.append(f"🗣 {text}")

        try:
            response = requests.post(
                SERVER_URL,
                json={"text": text},
                timeout=60
            )
            response.raise_for_status()
            answer = response.json()["answer"]
        except Exception as e:
            self.text.append(f"❌ Ошибка сервера: {e}")
            return

        self.text.append(f"🤖 {answer}")
        speak(answer)
