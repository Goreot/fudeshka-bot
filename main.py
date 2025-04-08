
from flask import Flask, request
import requests

TOKEN = "7266812114:AAGnN8K6CgTmfFsItCC34Ac7cYBUzNOHv20"
API_URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

@app.route("/")
def index():
    return "FudEshkaBot работает!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "Привет! Это Фуд.Ешка. Нажми /recipe, чтобы получить рецепт.")
        elif text == "/recipe":
            send_message(chat_id, "Сегодняшний рецепт: Паста с томатами и базиликом.\n1. Отвари макароны...\n2. Обжарь помидоры...")

    return "OK"

def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run()
