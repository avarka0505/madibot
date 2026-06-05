from telebot import TeleBot, types

BOT_TOKEN = "8903906713:AAFzgXutjbqOPL2B7osbWb8YpluZJ4siiog"
CHANNEL = "@avarka001"

bot = TeleBot(BOT_TOKEN)

# 🔒 проверка подписки (защита от обхода)
def is_subscribed(user_id):
    try:
        chat = bot.get_chat_member(CHANNEL, user_id)
        print("STATUS:", chat.status)

        if chat.status in ["creator", "administrator"]:
            return True
        if chat.status == "member":
            return True

        return False

    except Exception as e:
        print("ERROR:", e)
        return False
# 🎮 красивое меню
def main_menu():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("🎬 Получить видео", callback_data="video"),
        types.InlineKeyboardButton("ℹ️ Помощь", callback_data="help")
    )
    return kb

# 🚀 старт
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    bot.send_message(user_id, f"STATUS: {is_subscribed(user_id)}")

    if not is_subscribed(user_id):
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(
            types.InlineKeyboardButton(
                "📢 Подписаться на канал",
                url=f"https://t.me/{CHANNEL.replace('@','')}"
            ),
            types.InlineKeyboardButton(
                "✅ Я подписался",
                callback_data="check_sub"
            )
        )

        bot.send_message(
            user_id,
            "❌ Чтобы пользоваться ботом, подпишись на канал:",
            reply_markup=kb
        )
        return

    bot.send_message(
        user_id,
        "✅ Добро пожаловать! Выбери действие 👇",
        reply_markup=main_menu()
    )

# 🔘 кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.message.chat.id

    # проверка подписки
    if call.data == "check_sub":
        if is_subscribed(user_id):
            bot.send_message(user_id, "✅ Отлично! Доступ открыт 💥", reply_markup=main_menu())
        else:
            bot.answer_callback_query(call.id, "❌ Ты ещё не подписан!", show_alert=True)

    # видео
    elif call.data == "video":
        if not is_subscribed(user_id):
            bot.answer_callback_query(call.id, "❌ Сначала подпишись!", show_alert=True)
            return

        bot.send_video(
            user_id,
            "https://file-examples.com/storage/fe3a3f2b6d6f/video.mp4",
            caption="🎬 Вот твой контент!"
        )

    # помощь
    elif call.data == "help":
        bot.send_message(user_id, "ℹ️ Просто подпишись и получи доступ к контенту 💖")

bot.infinity_polling()
