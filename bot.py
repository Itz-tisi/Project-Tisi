from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import sqlite3
import os

# Replace with your bot token
TOKEN = "7461925686:AAHiQp1RS7YAVFVVHoWEyKgaE5wGYgO0QJo"

# Database Setup
DB_FILE = "bgmi_bot.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        bgmi_id TEXT,
        level INTEGER,
        tier TEXT,
        skill TEXT,
        role TEXT,
        kd FLOAT,
        language TEXT,
        gender TEXT
    )''')
    conn.commit()
    conn.close()

# Start Command
async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players WHERE user_id = ?", (user_id,))
    player = cursor.fetchone()
    conn.close()

    if player:
        await update.message.reply_text("You're already registered! Use /menu to access features.")
    else:
        await update.message.reply_text("Welcome to BGMI Squad Finder! Let's register you. Send your BGMI ID:")
        context.user_data['register_step'] = 'bgmi_id'

# Handle Registration Steps
async def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    text = update.message.text

    if 'register_step' in context.user_data:
        step = context.user_data['register_step']
        
        if step == 'bgmi_id':
            context.user_data['bgmi_id'] = text
            await update.message.reply_text("Enter your Level (e.g., 40, 50, etc.):")
            context.user_data['register_step'] = 'level'
        
        elif step == 'level':
            context.user_data['level'] = int(text)
            await update.message.reply_text("Enter your Tier (Bronze, Silver, Gold, Platinum, etc.):")
            context.user_data['register_step'] = 'tier'
        
        elif step == 'tier':
            context.user_data['tier'] = text
            await update.message.reply_text("Skill Level? (Beginner, Intermediate, Pro):")
            context.user_data['register_step'] = 'skill'
        
        elif step == 'skill':
            context.user_data['skill'] = text
            await update.message.reply_text("Your Role? (IGL, Close-Range, Long-Range, Supporter, Both):")
            context.user_data['register_step'] = 'role'
        
        elif step == 'role':
            context.user_data['role'] = text
            await update.message.reply_text("Your KD Ratio (e.g., 1.5, 2.3, etc.):")
            context.user_data['register_step'] = 'kd'
        
        elif step == 'kd':
            context.user_data['kd'] = float(text)
            await update.message.reply_text("Preferred Language? (Tamil, English, Hindi, etc.):")
            context.user_data['register_step'] = 'language'
        
        elif step == 'language':
            context.user_data['language'] = text
            await update.message.reply_text("Gender? (Male/Female):")
            context.user_data['register_step'] = 'gender'
        
        elif step == 'gender':
            context.user_data['gender'] = text
            # Save to Database
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO players (user_id, bgmi_id, level, tier, skill, role, kd, language, gender) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                           (user_id, context.user_data['bgmi_id'], context.user_data['level'], context.user_data['tier'], 
                            context.user_data['skill'], context.user_data['role'], context.user_data['kd'], 
                            context.user_data['language'], context.user_data['gender']))
            conn.commit()
            conn.close()
            await update.message.reply_text("✅ Successfully Registered! Use /menu to continue.")
            del context.user_data['register_step']

# Menu
async def menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Create New Team", callback_data="create_team")],
        [InlineKeyboardButton("Join a Team", callback_data="join_team")],
        [InlineKeyboardButton("Request a Player", callback_data="request_player")],
        [InlineKeyboardButton("Quick Team", callback_data="quick_team")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)

# Button Handler
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "create_team":
        await query.message.reply_text("Creating a new team feature coming soon!")
    elif query.data == "join_team":
        await query.message.reply_text("Joining a team feature coming soon!")
    elif query.data == "request_player":
        await query.message.reply_text("Requesting a player feature coming soon!")
    elif query.data == "quick_team":
        await query.message.reply_text("Quick team matchmaking coming soon!")

# Run the bot
def main():
    init_db()
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()