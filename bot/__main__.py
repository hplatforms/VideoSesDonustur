from pyrogram import filters
from bot import app, data, sudo_users
from bot.helper.utils import add_task

video_mimetype = [
  "video/TS",
  "video/x-flv",
  "video/mp4",
  "video/mkv",
  "application/x-mpegURL",
  "video/MP2T",
  "video/3gpp",
  "video/quicktime",
  "video/x-msvideo",
  "video/x-ms-wmv",
  "video/x-matroska",
  "video/webm",
  "video/x-m4v",
  "video/quicktime",
  "video/mpeg"
  ]

@app.on_message(filters.incoming & filters.command(['start', 'help']))
def help_message(app, message):
    message.reply_text(f"Merhaba {message.from_user.mention()}\nHiç sesi olmayan Telegram videolarını sesli olarak kodlayabilirim, sadece bana sesi olmayan bir video gönder.", quote=True)

@app.on_message(filters.user(sudo_users) & filters.incoming & (filters.video | filters.document))
def encode_video(app, message):
    if message.document:
      if not message.document.mime_type in video_mimetype:
        message.reply_text("```Geçersiz Video !\nBu video dosyasına benzemiyor.```", quote=True)
        return
    message.reply_text("```Sıraya alındı...```", quote=True)
    data.append(message)
    if len(data) == 1:
      add_task(message)

app.run()
