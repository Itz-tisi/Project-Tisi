import logging
import yt_dlp
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackContext

# Replace with your Bot's Token
TOKEN = "7461925686:AAHiQp1RS7YAVFVVHoWEyKgaE5wGYgO0QJo"

# Set up logging to track errors and activity
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to download YouTube videos using yt-dlp
async def handle_youtube(update: Update, context: CallbackContext):
    url = update.message.text
    try:
        # yt-dlp options for video download
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save video with title as filename
            'format': 'best',  # Choose the best quality
        }
        
        # Using yt-dlp to download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
        
        # Send video to user
        await update.message.reply_video(video=open(file_path, 'rb'), caption=f"Downloaded: {info_dict['title']}")
        
        # Delete the downloaded video after sending
        os.remove(file_path)
        logger.info(f"Deleted file: {file_path}")
        
    except yt_dlp.DownloadError as e:
        await update.message.reply_text(f"Error: {e}")
        logger.error(f"Download Error: {e}")
    except Exception as e:
        await update.message.reply_text(f"An unexpected error occurred: {e}")
        logger.error(f"Unexpected Error: {e}")

# Function to start the bot and show a welcome message
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Send me a YouTube URL, and I'll download the video for you.")

# Main function to start the bot and set up webhooks
def main():
    # Create the Application and set the webhook URL
    application = Application.builder().token(TOKEN).build()

    # Set up the webhook URL (replace 'your_webhook_url' with the actual URL of your server)
    application.bot.set_webhook("https://project-tisi.onrender.com")

    # Set up the command handler for /start
    application.add_handler(CommandHandler("start", start))
    
    # Set up the message handler to handle YouTube URLs
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_youtube))

    # Run the bot via webhook
    application.run_webhook(listen="0.0.0.0", port=80, url_path="YOUR_URL_PATH")

if __name__ == '__main__':
    main()