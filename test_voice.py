import requests

API_KEY = "sk-7c7902d888f64be0a2dfe80c15a42cf4"

url = "https://api.deepseek.com/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "Привет! Ответь одним словом: работает?"}
    ]
}

response = requests.post(url, headers=headers, json=data)

print("Status code:", response.status_code)
print(response.text)
