# client/input/voice_input.py
import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

MODEL_PATH = os.path.join(BASE_DIR, "model")

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

audio = pyaudio.PyAudio()


def listen_voice():
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8000
    )

    stream.start_stream()

    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")
            stream.stop_stream()
            stream.close()
            return text
