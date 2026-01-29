import os
import requests
from dotenv import load_dotenv

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit,
    QLineEdit, QPushButton, QHBoxLayout
)

from PyQt6.QtCore import QThread, pyqtSignal

from client.output.tts import speak
from client.input.voice_input import listen_voice

# =========================
# DeepSeek настройка
# =========================
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"


def ask_deepseek(prompt: str) -> str:
    if not DEEPSEEK_API_KEY:
        return "❌ DEEPSEEK_API_KEY не найден в .env"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(
            DEEPSEEK_URL,
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ Ошибка DeepSeek: {e}"


# =========================
# QThread для голосового ввода
# =========================
class VoiceThread(QThread):
    recognized = pyqtSignal(str)

    def run(self):
        text = listen_voice()
        self.recognized.emit(text)


# =========================
# Главное окно
# =========================
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Voice Assistant")
        self.resize(500, 400)

        # ===== Виджеты =====
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Введите текст и нажмите Enter")

        self.send_btn = QPushButton("Отправить")
        self.voice_btn = QPushButton("🎤 Говорить")

        # ===== Layout =====
        bottom = QHBoxLayout()
        bottom.addWidget(self.input)
        bottom.addWidget(self.send_btn)
        bottom.addWidget(self.voice_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(self.chat)
        layout.addLayout(bottom)

        # ===== Сигналы =====
        self.send_btn.clicked.connect(self.send_text)
        self.input.returnPressed.connect(self.send_text)
        self.voice_btn.clicked.connect(self.start_voice)

    # =========================
    # Общая логика
    # =========================
    def process_text(self, text: str):
        text = text.strip()
        if not text:
            return

        self.chat.append(f"🗣 Вы: {text}")

        answer = ask_deepseek(text)

        self.chat.append(f"🤖 AI: {answer}")
        speak(answer)

    # =========================
    # Текстовый ввод
    # =========================
    def send_text(self):
        text = self.input.text()
        self.input.clear()
        self.process_text(text)

    # =========================
    # Голосовой ввод
    # =========================
    def start_voice(self):
        self.chat.append("🎧 Слушаю...")
        self.voice_thread = VoiceThread()
        self.voice_thread.recognized.connect(self.on_voice_recognized)
        self.voice_thread.start()

    def on_voice_recognized(self, text: str):
        if not text:
            self.chat.append("❌ Голос не распознан")
            return
        self.process_text(text)
