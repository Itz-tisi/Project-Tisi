from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from flask import Flask, request
import logging
import os
import asyncio

# Flask app setup
app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Dictionary to store player details and team data
player_data = {}
team_requests = {}

# Your bot's token and webhook URL
TOKEN = "7461925686:AAHiQp1RS7YAVFVVHoWEyKgaE5wGYgO0QJo"
WEBHOOK_URL = "https://project-tisi.onrender.com/webhook"

# Start Command
async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id in player_data:
        await update.message.reply_text("You are already registered! Use /menu to continue.")
        return

    player_data[chat_id] = {"step": "registering"}
    await update.message.reply_text(
        "Welcome to BGMI Team Finder Bot!\nRegister to continue.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Register", callback_data="register")]
        ])
    )

# Registration Process
async def registration(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    player_data[chat_id] = {"registered": False, "step": "bgmi_id"}
    await query.edit_message_text("Enter your BGMI ID:")

# Handling Messages (For user inputs)
async def handle_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    if chat_id in player_data and player_data[chat_id].get("step") == "bgmi_id":
        player_data[chat_id]["bgmi_id"] = text
        player_data[chat_id]["step"] = "tier"
        await update.message.reply_text("Select your current tier:", 
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Bronze", callback_data="tier_Bronze"),
                 InlineKeyboardButton("Silver", callback_data="tier_Silver")],
                [InlineKeyboardButton("Gold", callback_data="tier_Gold"),
                 InlineKeyboardButton("Diamond", callback_data="tier_Diamond")],
                [InlineKeyboardButton("Crown", callback_data="tier_Crown"),
                 InlineKeyboardButton("Ace", callback_data="tier_Ace")],
                [InlineKeyboardButton("Ace Dominator", callback_data="tier_Ace_Dominator"),
                 InlineKeyboardButton("Conqueror", callback_data="tier_Conqueror")]
            ])
        )
    elif chat_id in player_data and player_data[chat_id].get("step") == "team_code":
        player_data[chat_id]["team_code"] = text
        await update.message.reply_text("Team Created! Finding players...")

# Handling Button Clicks
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    data = query.data

    if data.startswith("tier_"):
        tier = data.split("_")[1]
        player_data[chat_id]["tier"] = tier
        player_data[chat_id]["step"] = "role"
        await query.edit_message_text(f"Selected Tier: {tier}\nSelect Your Role:", 
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("IGL", callback_data="role_IGL"),
                 InlineKeyboardButton("Close-Range", callback_data="role_Close")],
                [InlineKeyboardButton("Long-Range", callback_data="role_Long"),
                 InlineKeyboardButton("Both", callback_data="role_Both")]
            ])
        )

    elif data.startswith("role_"):
        role = data.split("_")[1]
        player_data[chat_id]["role"] = role
        player_data[chat_id]["step"] = "kd"
        await query.edit_message_text(f"Selected Role: {role}\nEnter Your KD (1-25):")

    elif data.startswith("create_team"):
        player_data[chat_id]["step"] = "team_code"
        await query.edit_message_text("Send Your Team Code:")

    elif data.startswith("join_team"):
        team_code = find_matching_team(player_data[chat_id])
        if team_code:
            await query.edit_message_text(f"Found a matching team!\nTeam Code: {team_code}\nJoin Now!")
        else:
            await query.edit_message_text("No matching team found. Try again later.")

# Function to Find Matching Team
def find_matching_team(player_info):
    for team_id, team_info in team_requests.items():
        if team_info["tier"] == player_info["tier"] and team_info["role"] == player_info["role"]:
            return team_info["team_code"]
    return None

# Webhook Route
@app.route("/webhook", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = Update.de_json(json_str, application.bot)
    asyncio.run(application.process_update(update))
    return "ok", 200

# Set Webhook
async def set_webhook():
    await application.bot.setWebhook(WEBHOOK_URL)

# Main Function
def main():
    global application
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(registration, pattern="^register$"))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 4000)))

if __name__ == "__main__":
    main() 
json_str = request.get_data().decode("UTF-8")

json_data = json.loads(json_str)  # Converts the string to a JSON object
update = Update.de_json(json_data, application.bot)

import json

@app.route("/webhook", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")  # Get the raw JSON data from the request
    data = json.loads(json_str)  # Parse the raw string into a JSON object (dict)
    update = Update.de_json(data, application.bot)  # Now pass the parsed data to de_json
    asyncio.run(application.process_update(update))
    return "ok", 200
@app.route('/')
def home():
    return "Bot is live!", 200