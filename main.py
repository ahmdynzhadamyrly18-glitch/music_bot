import os
import telebot
from yt_dlp import YoutubeDL

TOKEN = '8897837950:AAGL9_Phb6kD0tszV5RBuMrbmPEkOvFnmjg'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! 🎧 نام آهنگ یا خواننده مد نظرت رو بفرست تا با کیفیت عالی (320) برات پیدا کنم و بفرستم.")

@bot.message_handler(func=lambda message: True)
def search_and_send_music(message):
    query = message.text
    msg = bot.reply_to(message, "🔎 در حال جستجو و دریافت باکیفیت‌ترین نسخه...")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': '%(title)s.%(ext)s',
        'default_search': 'ytsearch1:',
        'quiet': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            filename = ydl.prepare_filename(info['entries'][0]).rsplit('.', 1)[0] + '.mp3'

        with open(filename, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, title=info['entries'][0].get('title', 'Music'))

        bot.delete_message(message.chat.id, msg.message_id)
        if os.path.exists(filename):
            os.remove(filename)
        
    except Exception as e:
        bot.edit_message_text("❌ متأسفانه آهنگی پیدا نشد یا مشکلی در دریافت پیش آمد.", message.chat.id, msg.message_id)

bot.infinity_polling()
