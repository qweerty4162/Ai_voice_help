import os
import requests
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/chat/completions"

if not API_KEY:
    raise RuntimeError("DEEPSEEK_API_KEY не найден в .env")


def parse_command(text: str) -> dict:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Ты голосовой помощник. Отвечай кратко."},
            {"role": "user", "content": text}
        ],
        "temperature": 0.3
    }

    response = requests.post(URL, headers=headers, json=payload, timeout=20)
    response.raise_for_status()

    answer = response.json()["choices"][0]["message"]["content"]

    return {
        "intent": "chat",
        "response": answer
    }
