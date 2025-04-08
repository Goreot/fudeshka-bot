
from flask import Flask, request
import requests
import json
import random

TOKEN = "7266812114:AAGnN8K6CgTmfFsItCC34Ac7cYBUzNOHv20"
API_URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

# Загрузка рецептов из файла
with open("recipes.json", "r", encoding="utf-8") as f:
    recipes = json.load(f)

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
            send_message(chat_id, "👋 Привет! Это *Фуд.Ешка* — бот с пошаговыми рецептами.\n\nНапиши /recipe, чтобы получить рецепт дня.", "Markdown")
        elif text == "/recipe":
            recipe = random.choice(recipes)
            send_photo_with_caption(chat_id, recipe)
    return "OK"

def send_message(chat_id, text, parse_mode=None):
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    requests.post(url, json=payload)

def send_photo_with_caption(chat_id, recipe):
    caption = f"🍽 *{recipe['title']}*
🕒 Время: {recipe['time']}

📋 *Ингредиенты:*
"
    caption += "\n".join(f"- {item}" for item in recipe["ingredients"])
    caption += "\n\n👨‍🍳 *Шаги:*
" + "\n".join(recipe["steps"])
    url = f"{API_URL}/sendPhoto"
    payload = {
        "chat_id": chat_id,
        "photo": recipe["photo"],
        "caption": caption,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
