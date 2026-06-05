import telebot
from telebot import types
import os

TOKEN = os.getenv("TOKEN")
CHANNEL = "@avarka001"

bot = telebot.TeleBot(TOKEN)

# 👤 пользователи
users = {}

# 📚 знания
brain = {
    "фотосинтез": "🌿 растения превращают свет в энергию",
    "клетка": "🧬 основа жизни",
    "магнит": "🧲 создаёт поле и притягивает металл",
    "скорость": "🏃‍♂️ v = s / t"
}

# 🎯 тест
tests = {
    "bio": [
        ("Клетка это?", "единица жизни"),
        ("Где фотосинтез?", "в листьях"),
        ("Что нужно растениям?", "свет")
    ]
}

# 🔒 подписка (БЕЗ КРАША)
def is_subscribed(user_id):
    try:
        m = bot.get_chat_member(CHANNEL, user_id)
        return m.status in ["member", "administrator", "creator"]
    except:
        return True  # чтобы бот не падал

# 📢 подписка
def subscribe(chat_id):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        "📢 Подписаться",
        url=f"https://t.me/{CHANNEL.replace('@','')}"
    ))
    bot.send_message(chat_id,
        "❌ Доступ закрыт!\nПодпишись на канал 👇",
        reply_markup=kb
    )

# 🎮 меню
def menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🧠 AI", "📚 Урок")
    kb.row("🎯 Тест", "🏆 Профиль")
    kb.row("🥇 Топ")
    return kb

# 🚀 старт
@bot.message_handler(commands=['start'])
def start(m):
    if not is_subscribed(m.from_user.id):
        subscribe(m.chat.id)
        return

    users.setdefault(m.chat.id, {"xp":0,"level":1,"score":0})

    bot.send_message(m.chat.id,
        "👑 GOD BOT СТАБИЛЬНАЯ ВЕРСИЯ\nДобро пожаловать 🚀",
        reply_markup=menu()
    )

# 🧠 AI
@bot.message_handler(func=lambda m: m.text == "🧠 AI")
def ai(m):
    bot.send_message(m.chat.id,
        "✍️ Напиши: объясни + тема"
    )

@bot.message_handler(func=lambda m: m.text and m.text.startswith("объясни"))
def explain(m):
    if not is_subscribed(m.from_user.id):
        subscribe(m.chat.id)
        return

    topic = m.text.replace("объясни", "").strip().lower()
    u = users.setdefault(m.chat.id, {"xp":0,"level":1,"score":0})

    answer = brain.get(topic, "🤔 Это школьная тема")

    u["xp"] += 1

    if u["xp"] % 5 == 0:
        u["level"] += 1
        bot.send_message(m.chat.id, "🏆 LEVEL UP!")

    bot.send_message(m.chat.id, f"{answer}\n\n⭐ +1 XP")

# 📚 урок
@bot.message_handler(func=lambda m: m.text == "📚 Урок")
def lesson(m):
    bot.send_message(m.chat.id, "📖 Напиши: объясни клетка")

# 🎯 тест
@bot.message_handler(func=lambda m: m.text == "🎯 Тест")
def test(m):
    users.setdefault(m.chat.id, {"xp":0,"level":1,"score":0})
    users[m.chat.id]["score"] = 0

    q, a = tests["bio"][0]
    msg = bot.send_message(m.chat.id, "❓ " + q)
    bot.register_next_step_handler(msg, check_test, a)

def check_test(m, correct):
    u = users.setdefault(m.chat.id, {"xp":0,"level":1,"score":0})

    if m.text and m.text.lower() == correct:
        u["score"] += 1
        u["xp"] += 1
        bot.send_message(m.chat.id, "✔️ правильно!")
    else:
        bot.send_message(m.chat.id, f"❌ ответ: {correct}")

    bot.send_message(m.chat.id, f"📊 Баллы: {u['score']}")

# 👤 профиль
@bot.message_handler(func=lambda m: m.text == "🏆 Профиль")
def profile(m):
    u = users.get(m.chat.id, {"xp":0,"level":1,"score":0})

    bot.send_message(m.chat.id,
        f"👤 ПРОФИЛЬ\n\n⭐ XP: {u['xp']}\n🏆 Level: {u['level']}\n📊 Score: {u['score']}"
    )

# 🥇 топ
@bot.message_handler(func=lambda m: m.text == "🥇 Топ")
def top(m):
    if not users:
        bot.send_message(m.chat.id, "Пока игроков нет 😄")
        return

    sorted_users = sorted(users.items(),
                          key=lambda x: x[1]["xp"],
                          reverse=True)

    text = "🥇 ТОП ИГРОКОВ:\n\n"
    for i, (uid, d) in enumerate(sorted_users[:10], 1):
        text += f"{i}. XP {d['xp']} | LVL {d['level']}\n"

    bot.send_message(m.chat.id, text)

# 🚀 ВАЖНО ДЛЯ RAILWAY
bot.infinity_polling()
