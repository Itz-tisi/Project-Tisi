from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes
import time

# Define states for the conversation
PLAYER_ID, PLAYER_KD, PLAYER_LEVEL, PLAYER_LANGUAGE, PLAYER_SKILL, PLAYER_TIER, CHANGE_SETTINGS = range(7)
registered_players = {}  # To store registered player data
cooldown_time = 86400  # 24 hours in seconds

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id

    if user_id in registered_players:
        last_change_time = registered_players[user_id].get("last_change_time", 0)
        time_since_last_change = time.time() - last_change_time

        if time_since_last_change < cooldown_time:
            remaining_time = int((cooldown_time - time_since_last_change) / 3600)
            await update.message.reply_text(
                f"**You are already registered.** \nYou can change your settings after {remaining_time} hours.",
                parse_mode="Markdown"
            )
            return ConversationHandler.END

        await update.message.reply_text(
            "**You are already registered.**\nClick *Change Settings* to update your details.",
            reply_markup=ReplyKeyboardMarkup([["Change Settings"]], one_time_keyboard=True, resize_keyboard=True),
            parse_mode="Markdown"
        )
        return CHANGE_SETTINGS

    await update.message.reply_text(
        "**Register as a player.**\nUse the following steps to register.\n\nEnter your Player ID (numbers only):",
        parse_mode="Markdown"
    )
    return PLAYER_ID

async def get_player_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message.text.isdigit():
        await update.message.reply_text("**Invalid Player ID.** Please enter numbers only:", parse_mode="Markdown")
        return PLAYER_ID

    context.user_data['player_id'] = update.message.text

    # Provide KD ratio options
    kd_keyboard = [["1-5", "5-10"], ["10-15", "15-20"]]
    reply_markup = ReplyKeyboardMarkup(kd_keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("**Select your KD ratio:**", reply_markup=reply_markup, parse_mode="Markdown")
    return PLAYER_KD

async def get_player_kd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['player_kd'] = update.message.text

    # Provide level options
    level_keyboard = [["40-50", "50-60"], ["60-70", "70-80"], ["80-90"]]
    reply_markup = ReplyKeyboardMarkup(level_keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("**Select your Player Level:**", reply_markup=reply_markup, parse_mode="Markdown")
    return PLAYER_LEVEL

async def get_player_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['player_level'] = update.message.text

    # Provide language options
    language_keyboard = [["Tamil", "Telugu"], ["Malayalam", "Kannada"], ["Hindi"]]
    reply_markup = ReplyKeyboardMarkup(language_keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("**Select your language:**", reply_markup=reply_markup, parse_mode="Markdown")
    return PLAYER_LANGUAGE

async def get_player_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['player_language'] = update.message.text

    # Provide skill options
    skill_keyboard = [["Short Range Player"], ["Long Range Player"], ["Both Short & Long Range"], ["IGL"]]
    reply_markup = ReplyKeyboardMarkup(skill_keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("**Select your skill:**", reply_markup=reply_markup, parse_mode="Markdown")
    return PLAYER_SKILL

async def get_player_skill(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['player_skill'] = update.message.text

    # Provide tier options
    tier_keyboard = [["Diamond", "Crown"], ["Ace", "Ace Dominator"], ["Conqueror"]]
    reply_markup = ReplyKeyboardMarkup(tier_keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("**Select your maximum tier:**", reply_markup=reply_markup, parse_mode="Markdown")
    return PLAYER_TIER

async def get_player_tier(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
        f"**Registration Complete!** Your details are:\n"
        f"- **Player ID:** {context.user_data['player_id']}\n"
        f"- **KD Ratio:** {context.user_data['player_kd']}\n"
        f"- **Level:** {context.user_data['player_level']}\n"
        f"- **Language:** {context.user_data['player_language']}\n"
        f"- **Skill:** {context.user_data['player_skill']}\n"
        f"- **Maximum Tier:** {context.user_data['player_tier']}\n"
        f"\n**Player has been successfully registered!**"
    )
    await update.message.reply_text(summary, parse_mode="Markdown")

    return ConversationHandler.END

async def change_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id

    if user_id not in registered_players:
        await update.message.reply_text("You are not registered yet. Use /start to register.", parse_mode="Markdown")
        return ConversationHandler.END

    registered_players[user_id]["last_change_time"] = time.time()

    await update.message.reply_text("**You can now update your details. Please use /start to re-register.**", parse_mode="Markdown")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the registration process."""
    await update.message.reply_text("**Registration cancelled.**", parse_mode="Markdown")
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
            CHANGE_SETTINGS: [MessageHandler(filters.TEXT & ~filters.COMMAND, change_settings)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
