import os
from pytube import YouTube
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from pytube.exceptions import VideoUnavailable, RegexMatchError
import logging

# Your Bot's Token
TOKEN = "7461925686:AAHiQp1RS7YAVFVVHoWEyKgaE5wGYgO0QJo"

# Function to handle YouTube URL and auto-delete
async def handle_youtube(update: Update, context):
    url = update.message.text
    try:
        # Attempt to create a YouTube object
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        file_path = stream.download(output_path="downloads/")  # Download video to "downloads/" folder

        # Send video to user
        await update.message.reply_video(video=open(file_path, 'rb'), caption=f"Downloaded: {yt.title}")
        
        # Delete the downloaded video after sending
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
        
    except VideoUnavailable:
        await update.message.reply_text("Error: The video is unavailable. It might be private or removed.")
    except RegexMatchError:
        await update.message.reply_text("Error: The URL format is incorrect or unsupported.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
        logging.error(f"Error downloading video from {url}: {e}")

# Start command
async def start(update: Update, context):
    await update.message.reply_text("Send a YouTube URL to download the video.")

# Main function to set up the bot and start polling
def main():
    application = Application.builder().token(TOKEN).build()

    # Add the command handler
    application.add_handler(CommandHandler("start", start))
    
    # Add the message handler for non-command messages (YouTube URLs)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_youtube))

    # Start polling
    application.run_polling()

if __name__ == '__main__':
    main()