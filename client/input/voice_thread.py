from PyQt6.QtCore import QThread, pyqtSignal
from client.input.voice_input import listen_voice

class VoiceThread(QThread):
    recognized = pyqtSignal(str)

    def run(self):
        text = listen_voice()
        self.recognized.emit(text)
