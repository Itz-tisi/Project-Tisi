from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Dictionary to store player details
player_data = {}
team_data = []

# Start Command
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id in player_data and player_data[chat_id].get("registered"):
        update.message.reply_text("You are already registered! Use /menu to continue.")
        return

    player_data[chat_id] = {"registered": False, "step": "start"}
    update.message.reply_text(
        "Welcome to BGMI Team Finder Bot!\nPlease register to get started.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Register", callback_data="register")]
        ])
    )

# Registration Process
def registration(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id

    player_data[chat_id]["registered"] = True
    player_data[chat_id]["step"] = "complete"
    query.edit_message_text(
        "Registration complete! Use /menu to access options."
    )

# Main Menu
def main_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "Main Menu:\nChoose an option:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Create New Team", callback_data="create_team")],
            [InlineKeyboardButton("Join a Team", callback_data="join_team")],
            [InlineKeyboardButton("Request a Player", callback_data="request_player")],
            [InlineKeyboardButton("Quick Team", callback_data="quick_team")]
        ])
    )

# Create Team
def create_team(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id

    if chat_id not in player_data or not player_data[chat_id].get("registered"):
        query.edit_message_text("Please register first using /start.")
        return

    query.edit_message_text(
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
def select_level_range(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id
    selected_level = query.data.split("_")[1]

    player_data[chat_id]["team_level"] = selected_level
    query.edit_message_text(
        "What is the purpose of your team?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Rank Pushing", callback_data="purpose_rank")],
            [InlineKeyboardButton("Fun Gameplay", callback_data="purpose_fun")],
            [InlineKeyboardButton("Ultimate Royale", callback_data="purpose_ultimate")]
        ])
    )

# Team Purpose Selection
def select_team_purpose(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id
    selected_purpose = query.data.split("_")[1]

    player_data[chat_id]["team_purpose"] = selected_purpose
    query.edit_message_text(
        "Your team is almost ready! Please send your team code to complete the process."
    )

# Submit Team Code
def submit_team_code(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = update.message.text

    if "creating_team" in player_data.get(chat_id, {}) and player_data[chat_id]["creating_team"]:
        player_data[chat_id]["team_code"] = message
        team_data.append({
            "creator_id": chat_id,
            "level_range": player_data[chat_id]["team_level"],
            "purpose": player_data[chat_id]["team_purpose"],
            "code": message,
            "language": player_data[chat_id].get("language", "Any"),
        })
        update.message.reply_text(
            f"Your team has been created successfully!\nTeam Code: {message}\n"
            "The bot will now find eligible players and share the team code."
        )
        share_team_code_with_players(chat_id)
    else:
        update.message.reply_text("You are not creating a team currently. Use the menu to start.")

# Share Team Code with Players
def share_team_code_with_players(creator_id):
    team = next((t for t in team_data if t["creator_id"] == creator_id), None)
    if not team:
        return

    for player_id, details in player_data.items():
        if player_id == creator_id or details.get("step") != "complete":
            continue

        if (
            details.get("language", "Any") == team["language"]
            and details.get("level_range") == team["level_range"]
        ):
            context.bot.send_message(
                chat_id=player_id,
                text=(
                    f"Team Code Found for You!\n"
                    f"Level Range: {team['level_range']}\n"
                    f"Purpose: {team['purpose']}\n"
                    f"Team Code: {team['code']}\n\n"
                    "Click 'Join Team' in the menu to join!"
                )
            )

# Main Function
def main():
    TOKEN = "7461925686:AAHiQp1RS7YAVFVVHoWEyKgaE5wGYgO0QJo"  # Replace with your bot token
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(registration, pattern="^register$"))
    dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern="^menu$"))
    dispatcher.add_handler(CallbackQueryHandler(create_team, pattern="^create_team$"))
    dispatcher.add_handler(CallbackQueryHandler(select_level_range, pattern="^level_"))
    dispatcher.add_handler(CallbackQueryHandler(select_team_purpose, pattern="^purpose_"))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, submit_team_code))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()