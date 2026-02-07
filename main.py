import telebot
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"

bot = telebot.TeleBot(TOKEN)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(creds)
sheet = client.open("مصاريفي").sheet1


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "👋 هلا بيك\n"
        "سجّل مصروفك هيج:\n"
        "اكل 5000\n\n"
        "📌 أوامر:\n"
        "/today مجموع اليوم\n"
        "/month مجموع الشهر"
    )


@bot.message_handler(commands=['today'])
def today(message):
    اليوم = datetime.now().strftime("%Y-%m-%d")
    rows = sheet.get_all_records()
    المجموع = sum(
        r["المبلغ"] for r in rows
        if r["التاريخ"] == اليوم
    )
    bot.reply_to(message, f"📅 مجموع اليوم: {المجموع} دينار")


@bot.message_handler(commands=['month'])
def month(message):
    الشهر = datetime.now().strftime("%Y-%m")
    rows = sheet.get_all_records()
    المجموع = sum(
        r["المبلغ"] for r in rows
        if r["التاريخ"].startswith(الشهر)
    )
    bot.reply_to(message, f"📊 مجموع الشهر: {المجموع} دينار")


@bot.message_handler(func=lambda message: True)
def save_expense(message):
    try:
        text = message.text.split()
        الوصف = text[0]
        المبلغ = int(text[1])
        التاريخ = datetime.now().strftime("%Y-%m-%d")

        sheet.append_row([التاريخ, الوصف, المبلغ])
        bot.reply_to(message, "✅ تم تسجيل المصروف")
    except:
        bot.reply_to(message, "❌ اكتبها هيج: اكل 5000")


bot.polling()
