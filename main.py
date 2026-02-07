import os
import json
import telebot
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# ====== Telegram ======
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# ====== Google Sheets ======
SHEET_ID = os.environ.get("SHEET_ID")
GOOGLE_CREDS = os.environ.get("GOOGLE_CREDENTIALS")

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(GOOGLE_CREDS)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "👋 هلا بيك\n\n"
        "اكتب مصروفك هيج:\n"
        "10000 أكل\n\n"
        "وأنا أسجله مباشرة بالشيت 📊"
    )


@bot.message_handler(func=lambda message: True)
def save_expense(message):
    try:
        parts = message.text.split(" ", 1)
        amount = parts[0]
        note = parts[1] if len(parts) > 1 else ""

        sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            amount,
            note
        ])

        bot.reply_to(message, "✅ تم تسجيل المصروف")

    except Exception as e:
        bot.reply_to(message, "❌ صار خطأ، اكتبها هيج: 10000 أكل")


print("Bot is running...")
bot.infinity_polling()
