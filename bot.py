from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7461925686:AAHiQp1RS7YAVFVVHoWEyKgaE5wGYgO0QJo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I'm your bot.")

app = ApplicationBuilder().token("7461925686:AAHiQp1RS7YAVFVVHoWEyKgaE5wGYgO0QJo").build()
app.add_handler(CommandHandler("start", start))

app.run_polling()