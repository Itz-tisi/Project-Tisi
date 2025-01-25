from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ConversationHandler, ContextTypes
)

# Constants for conversation states
MENU, LANGUAGE, MIC, TEAM_OPTIONS = range(4)

# Sample user data storage
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Initial command to show the menu."""
    keyboard = [
        [InlineKeyboardButton("Royale", callback_data='royale'),
         InlineKeyboardButton("Fun", callback_data='fun')],
        [InlineKeyboardButton("Settings", callback_data='settings'),
         InlineKeyboardButton("Quick Team", callback_data='quick_team')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)
    return MENU

async def menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the menu options."""
    query = update.callback_query
    await query.answer()

    if query.data in ['royale', 'fun']:
        languages = [
            [InlineKeyboardButton("Tamil", callback_data='lang_tamil'),
             InlineKeyboardButton("English", callback_data='lang_english')],
            [InlineKeyboardButton("Hindi", callback_data='lang_hindi'),
             InlineKeyboardButton("Kannada", callback_data='lang_kannada')],
            [InlineKeyboardButton("Malayalam", callback_data='lang_malayalam'),
             InlineKeyboardButton("Telugu", callback_data='lang_telugu')]
        ]
        reply_markup = InlineKeyboardMarkup(languages)
        await query.edit_message_text("Select your language:", reply_markup=reply_markup)
        return LANGUAGE

    elif query.data == 'settings':
        await query.edit_message_text("Settings options coming soon!")
        return ConversationHandler.END

    elif query.data == 'quick_team':
        await query.edit_message_text("Quick Team options coming soon!")
        return ConversationHandler.END

async def language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles language selection."""
    query = update.callback_query
    await query.answer()
    selected_language = query.data.replace('lang_', '').capitalize()
    user_data[query.from_user.id] = {'language': selected_language}

    mic_options = [
        [InlineKeyboardButton("MIC On", callback_data='mic_on'),
         InlineKeyboardButton("MIC Off", callback_data='mic_off')]
    ]
    reply_markup = InlineKeyboardMarkup(mic_options)
    await query.edit_message_text(f"Language selected: {selected_language}\nMIC On/Off?", reply_markup=reply_markup)
    return MIC

async def mic_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles MIC selection."""
    query = update.callback_query
    await query.answer()
    mic_status = query.data.replace('mic_', '').capitalize()
    user_data[query.from_user.id]['mic'] = mic_status

    team_options = [
        [InlineKeyboardButton("Find a Player", callback_data='find_player')],
        [InlineKeyboardButton("Join a Team", callback_data='join_team')]
    ]
    reply_markup = InlineKeyboardMarkup(team_options)
    await query.edit_message_text("Team options:\n1. Find a Player\n2. Join a Team", reply_markup=reply_markup)
    return TEAM_OPTIONS

# Placeholder functions for team options
async def find_player(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Finding a player...\nShare your team code:")
    return ConversationHandler.END

async def join_team(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Joining a team...\nEnter the team code:")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels the conversation."""
    await update.message.reply_text("Bot stopped.")
    return ConversationHandler.END

def main():
    """Main function to run the bot."""
    # Create the application
    application = Application.builder().token("7461925686:AAHiQp1RS7YAVFVVHoWEyKgaE5wGYgO0QJo").build()  # Replace with your bot's token

    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [CallbackQueryHandler(menu_selection)],
            LANGUAGE: [CallbackQueryHandler(language_selection)],
            MIC: [CallbackQueryHandler(mic_selection)],
            TEAM_OPTIONS: [
                CallbackQueryHandler(find_player, pattern='find_player'),
                CallbackQueryHandler(join_team, pattern='join_team')
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
