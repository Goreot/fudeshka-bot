
from flask import Flask, request
import requests
import random

TOKEN = "7266812114:AAGnN8K6CgTmfFsItCC34Ac7cYBUzNOHv20"
API_URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

recipes = [
    "🍝 *Паста с томатами и базиликом*\n1. Отвари макароны\n2. Обжарь помидоры\n3. Добавь базилик и перемешай",
    "🥗 *Греческий салат*\n1. Нарежь огурцы, помидоры, перец\n2. Добавь фету и маслины\n3. Полей оливковым маслом",
    "🍳 *Яичница с овощами*\n1. Обжарь перец и помидоры\n2. Вбей яйца сверху\n3. Готовь под крышкой 5 минут",
    "🥘 *Курица в сливочном соусе*\n1. Обжарь курицу\n2. Добавь сливки и специи\n3. Туши 15 минут",
    "🍲 *Овощной суп*\n1. Нарежь овощи\n2. Вари до мягкости\n3. Добавь зелень и специи"
]

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
            send_message(chat_id, "👋 Привет! Это *Фуд.Ешка* — бот с рецептами дня!\n\nНажми /recipe, чтобы получить вкусное вдохновение.", parse_mode="Markdown")
        elif text == "/recipe":
            recipe = random.choice(recipes)
            send_message(chat_id, recipe, parse_mode="Markdown")

    return "OK"

def send_message(chat_id, text, parse_mode=None):
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
