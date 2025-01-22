import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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

def run_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())  # Fix for async loop issue
    app.run_polling()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    flask_app.run(host="0.0.0.0", port=10000)
import asyncio

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app.run_polling()