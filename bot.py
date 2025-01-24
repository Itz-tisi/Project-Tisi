from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from flask import Flask, request
import logging
import os
import asyncio

# Flask app for webhook server
app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Dictionary to store player details and team data
player_data = {}
team_data = []

# Your bot's token
TOKEN = '7461925686:AAHiQp1RS7YAVFVVHoWEyKgaE5wGYgO0QJo'

# Webhook URL (Replace with your actual deployed URL)
WEBHOOK_URL = 'https://<your-app-name>.onrender.com/webhook'  # Replace this

# Start Command
async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id in player_data and player_data[chat_id].get("registered"):
        await update.message.reply_text("You are already registered! Use /menu to continue.")
        return

    player_data[chat_id] = {"registered": False, "step": "start"}
    await update.message.reply_text(
        "Welcome to BGMI Team Finder Bot!\nPlease register to get started.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Register", callback_data="register")]
        ])
    )

# Registration Process
async def registration(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    player_data[chat_id]["registered"] = True
    player_data[chat_id]["step"] = "complete"
    await query.edit_message_text(
        "Registration complete! Use /menu to access options."
    )

# Main Menu
async def main_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "Main Menu:\nChoose an option:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Create New Team", callback_data="create_team")],
            [InlineKeyboardButton("Join a Team", callback_data="join_team")],
            [InlineKeyboardButton("Request a Player", callback_data="request_player")],
            [InlineKeyboardButton("Quick Team", callback_data="quick_team")]
        ])
    )

# Flask route to receive webhook updates
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, application.bot)
    asyncio.run(application.process_update(update))  # ✅ Fixed: Run the async update processor
    return 'ok', 200

# Async function to set webhook
async def set_webhook():
    await application.bot.setWebhook(WEBHOOK_URL)

# Main function
def main():
    global application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(registration, pattern="^register$"))
    application.add_handler(CallbackQueryHandler(main_menu, pattern="^menu$"))

    # Set webhook asynchronously
    asyncio.run(set_webhook())  # ✅ Fixed: Properly awaiting webhook setup

    # Start Flask server
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 4000)))

if __name__ == "__main__":
    main()