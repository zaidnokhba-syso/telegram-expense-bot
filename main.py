import os
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 هلا! البوت شغّال تمام ✅")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, "وصلتني رسالتك 📩")

print("Bot is running...")

bot.infinity_polling()
