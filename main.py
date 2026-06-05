from telebot import TeleBot

bot = TeleBot("8903906713:AAFzgXutjbqOPL2B7osbWb8YpluZJ4siiog")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет 🌸")

bot.infinity_polling()
from telebot import TeleBot, types

BOT_TOKEN = "8903906713:AAFzgXutjbqOPL2B7osbWb8YpluZJ4siiog"
CHANNEL = "@avarka001"  # сюда вставляем твой канал

bot = TeleBot(BOT_TOKEN)

# Проверка подписки
def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False

# /start команда
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    if not is_subscribed(user_id):
        # Если не подписан, даём инструкцию
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Подписаться", url=f"https://t.me/{CHANNEL.replace('@','')}"))
        markup.add(types.InlineKeyboardButton("✅ Я подписался", callback_data="check"))
        bot.send_message(user_id, "❌ Сначала подпишись на канал!", reply_markup=markup)
        return

    # Если подписан — приветствие
    bot.send_message(user_id, "✅ Добро пожаловать! Доступ открыт 🌸")

# Кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.message.chat.id

    if call.data == "check":
        if is_subscribed(user_id):
            bot.send_message(user_id, "✅ Отлично! Доступ открыт 🌸")
        else:
            bot.answer_callback_query(call.id, "❌ Ты всё ещё не подписан!", show_alert=True)

bot.infinity_polling()
