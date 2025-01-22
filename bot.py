from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import os
from flask import Flask

BOT_TOKEN = os.getenv("BOT_TOKEN", "7461925686:AAHiQp1RS7YAVFVVHoWEyKgaE5wGYgO0QJo")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I'm your bot.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

# Flask server for Render
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    from threading import Thread
    Thread(target=app.run_polling).start()
    flask_app.run(host="0.0.0.0", port=10000)