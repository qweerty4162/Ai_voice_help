import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = os.getenv("DEEPSEEK_API_URL")

class DeepSeekClient:
    def __init__(self):
        if not API_KEY:
            raise RuntimeError("DEEPSEEK_API_KEY не найден в .env")

    def ask(self, text: str) -> str:
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "Ты голосовой помощник."},
                {"role": "user", "content": text}
            ]
        }

        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
