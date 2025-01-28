from pytube import YouTube
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

# Function to handle YouTube URL and auto-delete
def handle_youtube(update: Update, context):
    url = update.message.text
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        file_path = stream.download(output_path="downloads/")  # Download video to "downloads/" folder

        # Send video to user
        update.message.reply_video(video=open(file_path, 'rb'), caption=f"Downloaded: {yt.title}")
        
        # Delete the downloaded video after sending
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
        
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

# Start command
def start(update: Update, context):
    update.message.reply_text("Send a YouTube URL to download the video.")

# Main function
def main():
    updater = Updater("YOUR_TELEGRAM_BOT_API_TOKEN", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_youtube))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()