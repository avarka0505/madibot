import telebot
from telebot import types
from openai import OpenAI
import os
import time
import traceback

# ======================
# 🔑 KEYS
# ======================
TOKEN = os.getenv("TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

if not TOKEN:
    raise Exception("TOKEN is missing")

bot = telebot.TeleBot(TOKEN)

client = None
if OPENAI_KEY:
    try:
        client = OpenAI(api_key=OPENAI_KEY)
    except Exception as e:
        print("OPENAI INIT ERROR:", e)

# ======================
# 🧠 MEMORY (in RAM, stable)
# ======================
users = {}
last_msg_time = {}

# ======================
# 🎭 MODES
# ======================
MODES = {
    "друг": "Ты дружелюбный помощник 😊 отвечай просто",
    "учитель": "Ты учитель 📚 объясняй понятно",
    "строгий": "Ты строгий учитель ⚠️ кратко и чётко"
}

# ======================
# 🤖 AI SAFE CALL
# ======================
def ask_ai(uid, text):
    try:
        if not client:
            return "⚠️ AI не подключён"

        u = users.setdefault(uid, {
            "xp": 0,
            "level": 1,
            "mode": "друг",
            "history": []
        })

        u["history"].append({"role": "user", "content": text})

        messages = [
            {"role": "system", "content": MODES[u["mode"]]}
        ] + u["history"][-6:]

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        answer = res.choices[0].message.content

        u["history"].append({"role": "assistant", "content": answer})

        return answer

    except Exception as e:
        print("AI ERROR:", e)
        return "⚠️ AI временно недоступен"

# ======================
# 🎮 MENU
# ======================
def menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🧠 AI", "📚 Урок")
    kb.row("🏆 Профиль", "🎭 Режим")
    return kb

# ======================
# 🚀 START
# ======================
@bot.message_handler(commands=["start"])
def start(m):
    try:
        uid = str(m.chat.id)

        users.setdefault(uid, {
            "xp": 0,
            "level": 1,
            "mode": "друг",
            "history": []
        })

        bot.send_message(
            m.chat.id,
            "🤖 БОТ ЗАПУЩЕН СТАБИЛЬНО 🚀",
            reply_markup=menu()
        )

    except Exception as e:
        print("START ERROR:", e)

# ======================
# 🎭 MODE
# ======================
@bot.message_handler(func=lambda m: m.text == "🎭 Режим")
def mode(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("друг", "учитель", "строгий")
    bot.send_message(m.chat.id, "Выбери режим 🎭", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text in MODES)
def set_mode(m):
    uid = str(m.chat.id)
    users.setdefault(uid, {})["mode"] = m.text
    bot.send_message(m.chat.id, f"✅ Режим: {m.text}")

# ======================
# 💬 MAIN HANDLER
# ======================
@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        uid = str(m.chat.id)

        # anti spam
        now = time.time()
        if uid in last_msg_time and now - last_msg_time[uid] < 1:
            return
        last_msg_time[uid] = now

        u = users.setdefault(uid, {
            "xp": 0,
            "level": 1,
            "mode": "друг",
            "history": []
        })

        answer = ask_ai(uid, m.text)

        u["xp"] += 1
        if u["xp"] % 5 == 0:
            u["level"] += 1
            bot.send_message(m.chat.id, "🏆 LEVEL UP!")

        bot.send_message(m.chat.id, f"{answer}\n\n⭐ +1 XP")

    except Exception as e:
        print("HANDLER ERROR:", e)
        traceback.print_exc()
        try:
            bot.send_message(m.chat.id, "⚠️ ошибка, попробуй снова")
        except:
            pass

# ======================
# 🔄 IMMORTAL LOOP
# ======================
print("🚀 BOT RUNNING STABLE MODE")

while True:
    try:
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print("RESTARTING BOT:", e)
        time.sleep(3)
