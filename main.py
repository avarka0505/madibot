import telebot
from telebot import types
from openai import OpenAI
import os
import time
import traceback
import json

# ======================
# 🔑 KEYS
# ======================
TOKEN = os.getenv("TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

# ======================
# 🤖 INIT SAFE
# ======================
bot = None
client = None

try:
    if TOKEN:
        bot = telebot.TeleBot(TOKEN)
except Exception as e:
    print("BOT INIT ERROR:", e)

try:
    if OPENAI_KEY:
        client = OpenAI(api_key=OPENAI_KEY)
except Exception as e:
    print("OPENAI INIT ERROR:", e)

# ======================
# 💾 FILE STORAGE (NO DB NEEDED)
# ======================
DATA_FILE = "users.json"

def load_users():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return {}

def save_users():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("SAVE ERROR:", e)

users = load_users()
last_msg_time = {}

# ======================
# 🎭 MODES
# ======================
MODES = {
    "друг": "Ты дружелюбный помощник 😊 объясняй просто",
    "учитель": "Ты учитель 📚 объясняй структурно",
    "строгий": "Ты строгий учитель ⚠️ отвечай кратко"
}

# ======================
# 🧠 AI (ULTRA SAFE)
# ======================
def ask_ai(user_id, text):
    try:
        if not client:
            return "⚠️ AI не подключён"

        u = users.setdefault(str(user_id), {
            "xp": 0,
            "level": 1,
            "mode": "друг",
            "history": []
        })

        u["history"].append({"role": "user", "content": text})

        messages = [
            {"role": "system", "content": MODES.get(u["mode"], MODES["друг"])}
        ] + u["history"][-8:]

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        answer = res.choices[0].message.content

        u["history"].append({"role": "assistant", "content": answer})

        save_users()
        return answer

    except Exception as e:
        print("AI ERROR:", e)
        traceback.print_exc()
        return "⚠️ AI временно недоступен"

# ======================
# 🎮 MENU
# ======================
def menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🧠 AI", "📚 Урок")
    kb.row("🎯 Тест", "🏆 Профиль")
    kb.row("🎭 Режим")
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

        save_users()

        bot.send_message(
            m.chat.id,
            "🤖 ULTRA PRO MAX GOD MODE BOT ⚡",
            reply_markup=menu()
        )

    except Exception as e:
        print("START ERROR:", e)

# ======================
# 🎭 MODE
# ======================
@bot.message_handler(func=lambda m: m.text == "🎭 Режим")
def mode_menu(m):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row("друг", "учитель", "строгий")
        bot.send_message(m.chat.id, "Выбери режим 🎭", reply_markup=kb)
    except:
        pass

@bot.message_handler(func=lambda m: m.text in MODES)
def set_mode(m):
    try:
        uid = str(m.chat.id)
        users.setdefault(uid, {})["mode"] = m.text
        save_users()
        bot.send_message(m.chat.id, f"✅ Режим: {m.text}")
    except:
        pass

# ======================
# 💬 MAIN HANDLER (IMMORTAL)
# ======================
@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        uid = str(m.chat.id)

        # anti spam
        now = time.time()
        if uid in last_msg_time:
            if now - last_msg_time[uid] < 1:
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
            try:
                bot.send_message(m.chat.id, "🏆 LEVEL UP!")
            except:
                pass

        try:
            bot.send_message(m.chat.id, f"{answer}\n\n⭐ +1 XP")
        except:
            pass

        save_users()

    except Exception as e:
        print("HANDLER ERROR:", e)
        traceback.print_exc()
        try:
            bot.send_message(m.chat.id, "⚠️ временная ошибка, попробуй снова")
        except:
            pass

# ======================
# 🔄 IMMORTAL POLLING
# ======================
print("🚀 GOD MODE BOT STARTED")

while True:
    try:
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print("CRASH RECOVERED:", e)
        time.sleep(2)
