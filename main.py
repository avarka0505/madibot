from telebot import TeleBot, types

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNEL = "@avarka001"

bot = TeleBot(BOT_TOKEN)

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
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
        bot.send_message(user_id, "❌ Сначала подпишись на канал!", reply_markup=markup)
        return

    bot.send_message(user_id, "✅ Добро пожаловать! Доступ открыт 🌸")

print("Bot started...")
bot.infinity_polling()
