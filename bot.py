from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from flask import Flask, request
import logging
import os

# Flask app for webhook server
app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Dictionary to store player details and team data
player_data = {}
team_data = []

# Your bot's token
TOKEN = '7461925686:AAHiQp1RS7YAVFVVHoWEyKgaE5wGYgO0QJo'

# Webhook URL (set this to the URL where you want Telegram to send updates)
WEBHOOK_URL = 'https://your-domain.com/YOUR-BOT-HANDLE'

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

# Create Team
async def create_team(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    if chat_id not in player_data or not player_data[chat_id].get("registered"):
        await query.edit_message_text("Please register first using /start.")
        return

    await query.edit_message_text(
        "Select the Level Range for your Team (e.g., 30-40):",
        reply_markup=level_range_buttons()
    )
    player_data[chat_id]["creating_team"] = True

# Level Range Buttons
def level_range_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("30-40", callback_data="level_30_40")],
        [InlineKeyboardButton("40-50", callback_data="level_40_50")],
        [InlineKeyboardButton("50-60", callback_data="level_50_60")],
        [InlineKeyboardButton("60-70", callback_data="level_60_70")],
        [InlineKeyboardButton("70-80", callback_data="level_70_80")],
        [InlineKeyboardButton("80-90", callback_data="level_80_90")]
    ])

# Level Range Selection
async def select_level_range(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    selected_level = query.data.split("_")[1]  # Extract the level range from callback data

    player_data[chat_id]["team_level"] = selected_level  # Store the selected level in the player data
    await query.edit_message_text(
        "What is the purpose of your team?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Rank Pushing", callback_data="purpose_rank")],
            [InlineKeyboardButton("Fun Gameplay", callback_data="purpose_fun")],
            [InlineKeyboardButton("Ultimate Royale", callback_data="purpose_ultimate")]
        ])
    )

# Team Purpose Selection (The missing function now defined)
async def select_team_purpose(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    selected_purpose = query.data.split("_")[1]  # Extract the purpose from callback data

    player_data[chat_id]["team_purpose"] = selected_purpose  # Store the selected purpose in the player data
    await query.edit_message_text(
        "Team setup is complete! You can now share your team code or request players to join."
    )

# Flask route to receive webhook updates
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, application.bot)
    application.update_queue.put(update)
    return 'ok', 200

# Main function to set up the application and webhook
def main():
    # Create the application and add handlers
    global application
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(registration, pattern="^register$"))
    application.add_handler(CallbackQueryHandler(main_menu, pattern="^menu$"))
    application.add_handler(CallbackQueryHandler(create_team, pattern="^create_team$"))
    application.add_handler(CallbackQueryHandler(select_level_range, pattern="^level_"))
    application.add_handler(CallbackQueryHandler(select_team_purpose, pattern="^purpose_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, submit_team_code))

    # Set webhook with Telegram
    application.bot.setWebhook(WEBHOOK_URL)

    # Start the Flask web server to handle incoming requests
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 4000)))

if __name__ == "__main__":
    main()