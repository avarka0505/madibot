from telebot import TeleBot

bot = TeleBot("8903906713:AAFzgXutjbqOPL2B7osbWb8YpluZJ4siiog")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет 🌸")

bot.infinity_polling()
