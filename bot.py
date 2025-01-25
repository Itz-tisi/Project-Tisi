from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes
import time

# Define states for the conversation
PLAYER_ID, PLAYER_KD, PLAYER_LEVEL, PLAYER_LANGUAGE, PLAYER_SKILL, PLAYER_TIER, CHANGE_SETTINGS = range(7)
registered_players = {}  # To store registered player data
cooldown_time = 86400  # 24 hours in seconds

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the /start command to initiate the registration process."""
    user_id = update.effective_user.id

    if user_id in registered_players:
        last_change_time = registered_players[user_id].get("last_change_time", 0)
        time_since_last_change = time.time() - last_change_time

        if time_since_last_change < cooldown_time:
            await update.message.reply_text(
                "**\ud83d\udd12 You are already registered.**",
                parse_mode="Markdown"
            )
            return ConversationHandler.END

        await update.message.reply_text(
            "**\ud83d\udd12 You are already registered.**\nClick *Change Settings* to update your details.",
            reply_markup=ReplyKeyboardMarkup([["\u2699 Change Settings"]], one_time_keyboard=True, resize_keyboard=True),
            parse_mode="Markdown"
        )
        return CHANGE_SETTINGS

    await update.message.reply_text(
        "**\ud83c\udf89 Welcome to the Squad Finder!**\n\n**Register as a player.**\nUse the following steps to register.\n\nEnter your Player ID (numbers only):",
        parse_mode="Markdown"
    )
    return PLAYER_ID

async def get_player_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Player ID input."""
    if not update.message.text.isdigit():
        await update.message.reply_text("**\u274c Invalid Player ID.** Please enter numbers only:", parse_mode="Markdown")
        return PLAYER_ID

    context.user_data['player_id'] = update.message.text

    # Provide KD ratio options
    kd_keyboard = [["1-5 \ud83d\udca1", "5-10 \ud83c\udfc6"], ["10-15 \ud83c\udfcb\ufe0f", "15-20 \u2694\ufe0f"]]
    reply_markup = ReplyKeyboardMarkup(kd_keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("**\ud83d\udcca Select your KD ratio:**", reply_markup=reply_markup, parse_mode="Markdown")
    return PLAYER_KD

async def get_player_kd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle KD Ratio input."""
    context.user_data['player_kd'] = update.message.text

    # Provide level options
    level_keyboard = [["40-50 \ud83c\udf1f", "50-60 \ud83d\udcaa"], ["60-70 \ud83d\udd25", "70-80 \ud83c\udf0c"], ["80-90 \ud83d\udc51"]]
    reply_markup = ReplyKeyboardMarkup(level_keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("**\ud83d\udd22 Select your Player Level:**", reply_markup=reply_markup, parse_mode="Markdown")
    return PLAYER_LEVEL

async def get_player_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Player Level input."""
    context.user_data['player_level'] = update.message.text

    # Provide language options
    language_keyboard = [["Tamil \ud83c\uddf9\ud83c\uddf3", "Telugu \ud83c\uddf9\ud83c\uddf4"], ["Malayalam \ud83c\uddf2\ud83c\uddf3", "Kannada \ud83c\uddf3\ud83c\uddf0"], ["Hindi \ud83c\uddee\ud83c\uddf3"]]
    reply_markup = ReplyKeyboardMarkup(language_keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("**\ud83c\udf10 Select your language:**", reply_markup=reply_markup, parse_mode="Markdown")
    return PLAYER_LANGUAGE

async def get_player_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Player Language input."""
    context.user_data['player_language'] = update.message.text

    # Provide skill options
    skill_keyboard = [["Short Range Player \ud83d\udee1\ufe0f"], ["Long Range Player \ud83c\udfca"], ["Both Short & Long Range \u2694\ufe0f\ud83c\udfca"], ["IGL \ud83d\udd27"]]
    reply_markup = ReplyKeyboardMarkup(skill_keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("**\ud83d\udd27 Select your skill:**", reply_markup=reply_markup, parse_mode="Markdown")
    return PLAYER_SKILL

async def get_player_skill(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Player Skill input."""
    context.user_data['player_skill'] = update.message.text

    # Provide tier options
    tier_keyboard = [["Diamond \ud83d\udd39", "Crown \ud83d\udc51"], ["Ace \ud83d\udd1e", "Ace Dominator \ud83d\udd30"], ["Conqueror \ud83c\udfc6"]]
    reply_markup = ReplyKeyboardMarkup(tier_keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("**\ud83d\udd3a Select your maximum tier:**", reply_markup=reply_markup, parse_mode="Markdown")
    return PLAYER_TIER

async def get_player_tier(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle Player Tier input and complete registration."""
    context.user_data['player_tier'] = update.message.text

    user_id = update.effective_user.id
    registered_players[user_id] = {
        "player_id": context.user_data['player_id'],
        "player_kd": context.user_data['player_kd'],
        "player_level": context.user_data['player_level'],
        "player_language": context.user_data['player_language'],
        "player_skill": context.user_data['player_skill'],
        "player_tier": context.user_data['player_tier'],
        "last_change_time": time.time()
    }

    # Registration summary
    summary = (
        f"**\ud83d\udce2 Registration Complete!** Your details are:\n"
        f"- **Player ID:** {context.user_data['player_id']}\n"
        f"- **KD Ratio:** {context.user_data['player_kd']}\n"
        f"- **Level:** {context.user_data['player_level']}\n"
        f"- **Language:** {context.user_data['player_language']}\n"
        f"- **Skill:** {context.user_data['player_skill']}\n"
        f"- **Maximum Tier:** {context.user_data['player_tier']}\n"
        f"\n**\ud83c\udf89 Player has been successfully registered!**"
    )
    await update.message.reply_text(summary, parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

async def change_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Allow the user to update their details."""
    user_id = update.effective_user.id

    if user_id not in registered_players:
        await update.message.reply_text("You are not registered yet. Use /start to register.", parse_mode="Markdown")
        return ConversationHandler.END

    registered_players[user_id]["last_change_time"] = time.time()

    await update.message.reply_text("**You can now update your details. Please use /start to re-register.**", parse_mode="Markdown")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the registration process."""
    await update.message.reply_text("**\u274c Registration cancelled.**", parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Main function to run the bot
def main() -> None:
    """Start the bot and set up the handlers."""
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
            CHANGE_SETTINGS: [MessageHandler(filters.TEXT & ~filters.COMMAND, change_settings)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
