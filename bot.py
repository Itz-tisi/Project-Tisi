from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes

# Define states for the conversation
PLAYER_ID, PLAYER_KD, PLAYER_LEVEL, PLAYER_LANGUAGE, PLAYER_SKILL, PLAYER_TIER = range(6)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the registration process."""
    await update.message.reply_text(
        "Register as a player. Please provide the following details.\n\nEnter your Player ID:",
    )
    return PLAYER_ID

async def get_player_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get the player's ID."""
    context.user_data['player_id'] = update.message.text
    await update.message.reply_text("Enter your KD ratio:")
    return PLAYER_KD

async def get_player_kd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get the player's KD ratio."""
    context.user_data['player_kd'] = update.message.text
    await update.message.reply_text("Enter your Player Level:")
    return PLAYER_LEVEL

async def get_player_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get the player's level."""
    context.user_data['player_level'] = update.message.text

    # Provide language options
    language_keyboard = [["Tamil", "Telugu"], ["Malayalam", "Kannada"], ["Hindi"]]
    reply_markup = ReplyKeyboardMarkup(language_keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("Select your language:", reply_markup=reply_markup)
    return PLAYER_LANGUAGE

async def get_player_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get the player's language."""
    context.user_data['player_language'] = update.message.text

    # Provide skill options
    skill_keyboard = [["Short Range Player"], ["Long Range Player"], ["Both Short & Long Range"], ["IGL"]]
    reply_markup = ReplyKeyboardMarkup(skill_keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("Select your skill:", reply_markup=reply_markup)
    return PLAYER_SKILL

async def get_player_skill(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get the player's skill."""
    context.user_data['player_skill'] = update.message.text

    # Provide tier options
    tier_keyboard = [["Diamond", "Crown"], ["Ace", "Ace Dominator"], ["Conqueror"]]
    reply_markup = ReplyKeyboardMarkup(tier_keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("Select your maximum tier:", reply_markup=reply_markup)
    return PLAYER_TIER

async def get_player_tier(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get the player's maximum tier."""
    context.user_data['player_tier'] = update.message.text

    # Registration summary
    summary = (
        f"Registration Complete! Your details are:\n"
        f"- Player ID: {context.user_data['player_id']}\n"
        f"- KD Ratio: {context.user_data['player_kd']}\n"
        f"- Level: {context.user_data['player_level']}\n"
        f"- Language: {context.user_data['player_language']}\n"
        f"- Skill: {context.user_data['player_skill']}\n"
        f"- Maximum Tier: {context.user_data['player_tier']}\n"
        f"\nPlayer has been successfully registered!"
    )
    await update.message.reply_text(summary)

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the registration process."""
    await update.message.reply_text("Registration cancelled.")
    return ConversationHandler.END

# Main function to run the bot
def main() -> None:
    application = Application.builder().token("7461925686:AAHiQp1RS7YAVFVVHoWEyKgaE5wGYgO0QJo").build()

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PLAYER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_player_id)],
            PLAYER_KD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_player_kd)],
            PLAYER_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_player_level)],
            PLAYER_LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_player_language)],
            PLAYER_SKILL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_player_skill)],
            PLAYER_TIER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_player_tier)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
