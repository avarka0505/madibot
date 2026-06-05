from telebot import TeleBot, types

BOT_TOKEN = "8903906713:AAFzgXutjbqOPL2B7osbWb8YpluZJ4siiog"
CHANNEL = "@avarka001"

bot = TeleBot(BOT_TOKEN)

print("Bot is starting...")

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "creator", "administrator"]
    except Exception as e:
        print("ERROR:", e)
        return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    if not is_subscribed(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                "📢 Подписаться",
                url=f"https://t.me/{CHANNEL.replace('@','')}"
            )
        )
        bot.send_message(user_id, "❌ Подпишись на канал сначала!", reply_markup=markup)
        return

    bot.send_message(user_id, "✅ Добро пожаловать! Всё работает 🌸")

bot.infinity_polling(skip_pending=True)
