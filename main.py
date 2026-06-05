import telebot
from telebot import types
from openai import OpenAI
import os
import time

# 🔑 ключи
TOKEN = os.getenv("TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

bot = telebot.TeleBot(TOKEN)
client = OpenAI(api_key=OPENAI_KEY)

# 👤 память
users = {}

# 🎭 режимы
MODES = {
    "друг": "Ты дружелюбный помощник, объясняешь просто 😊",
    "учитель": "Ты школьный учитель, объясняешь понятно и структурно 📚",
    "строгий": "Ты строгий учитель, отвечаешь коротко и чётко ⚠️"
}

# 🛡 анти-спам
last_msg_time = {}

CHANNEL = "@avarka001"

# 🔒 подписка
def is_subscribed(user_id):
    try:
        m = bot.get_chat_member(CHANNEL, user_id)
        return m.status in ["member", "administrator", "creator"]
    except:
        return True

# 🎮 меню
def menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🧠 AI", "📚 Урок")
    kb.row("🎯 Тест", "🏆 Профиль")
    kb.row("🎭 Режим")
    return kb

# 🚀 старт
@bot.message_handler(commands=['start'])
def start(m):
    users.setdefault(m.chat.id, {
        "xp": 0,
        "level": 1,
        "score": 0,
        "mode": "друг",
        "history": []
    })

    bot.send_message(m.chat.id,
        "🤖 ULTRA GOD BOT ЗАПУЩЕН 🚀",
        reply_markup=menu()
    )

# 🎭 режим
@bot.message_handler(func=lambda m: m.text == "🎭 Режим")
def mode_menu(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("друг", "учитель", "строгий")
    bot.send_message(m.chat.id, "Выбери режим 🎭", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text in MODES)
def set_mode(m):
    u = users.setdefault(m.chat.id, {})
    u["mode"] = m.text
    bot.send_message(m.chat.id, f"✅ Режим: {m.text}")

# 🧠 ChatGPT
def ask_ai(user_id, text):
    u = users[user_id]

    u["history"].append({"role": "user", "content": text})

    messages = [
        {"role": "system", "content": MODES.get(u.get("mode", "друг"))}
    ] + u["history"][-10:]

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    answer = res.choices[0].message.content

    u["history"].append({"role": "assistant", "content": answer})

    return answer

# 💬 обработка
@bot.message_handler(func=lambda m: True)
def handle(m):

    u = users.setdefault(m.chat.id, {
        "xp": 0,
        "level": 1,
        "score": 0,
        "mode": "друг",
        "history": []
    })

    # 🛡 анти-спам
    now = time.time()
    if m.chat.id in last_msg_time:
        if now - last_msg_time[m.chat.id] < 1:
            return
    last_msg_time[m.chat.id] = now

    try:
        answer = ask_ai(m.chat.id, m.text)
    except:
        answer = "⚠️ ошибка AI"

    # 🎮 XP
    u["xp"] += 1
    if u["xp"] % 5 == 0:
        u["level"] += 1
        bot.send_message(m.chat.id, "🏆 LEVEL UP!")

    bot.send_message(m.chat.id, answer + "\n\n⭐ +1 XP")

# 🚀 запуск
bot.infinity_polling()
