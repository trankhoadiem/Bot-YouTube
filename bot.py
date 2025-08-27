from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pytube import YouTube
import os

TOKEN = os.getenv("TOKEN")  # Lấy token từ biến môi trường

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Chào! Gửi link YouTube để tải video.")

def download_youtube(url):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    filename = stream.download()
    return filename

def handle_message(update: Update, context: CallbackContext):
    url = update.message.text
    update.message.reply_text("Đang tải video...")
    try:
        file_path = download_youtube(url)
        with open(file_path, "rb") as video_file:
            update.message.reply_video(video_file)
        os.remove(file_path)
    except Exception as e:
        update.message.reply_text(f"Lỗi: {e}")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
