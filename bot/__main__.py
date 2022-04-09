from pyrogram import filters
from pyrogram import filters
import requests
import heroku3

from pyrogram import filters
from pyrogram.types import (
    Message
)
from pyrogram import Client

from bot import app, data, sudo_users, heroku_api_key, heroku_app_name
from bot.helper.utils import add_task
from pyrogram.types.bots_and_keyboards import InlineKeyboardButton, InlineKeyboardMarkup
from .translation import Translation

video_mimetype = [
  "video/x-flv",
  "video/mp4",
  "video/avi",
  "video/mkv",
  "application/x-mpegURL",
  "video/mp2t",
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

@app.on_message(filters.command('start'))
def help_message(app, message):
        message.reply_text(
            text=Translation.START_TEXT.format(message.from_user.mention()),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Destek", url="https://t.me/botsohbet"
                        )
                    ]
                ]
            ),
            reply_to_message_id=message.message_id
        ) 

@app.on_message(filters.command("restart") & filters.user(sudo_users))
async def restart(_, m: Message):
    restart_message = await m.reply_text(text="`İntihar ediyom bekle...`")
    await restart_message.edit("`Ölmek üzereyim...\nbana hayat verdiğin için teşekkürler😢`")
    try:
        if heroku_api_key is not None:
            heroku_conn = heroku3.from_key(heroku_api_key)
            server = heroku_conn.app(heroku_app_name)
            server.restart()
        else:
            await restart_message.edit("`Heroku Api Key ve uygulama adını ekleyin.`")
    except Exception as e:
        await restart_message.edit(f"**İntihar bile edemedim:** `{e}`")
    
@app.on_message(filters.video)
def encode_video(app, message):
    if message.document:
      if not message.document.mime_type in video_mimetype:
        message.reply_text("```Geçersiz Video !\nBu video dosyasına benzemiyor.```", quote=True)
        return
    message.reply_text(f"`✔️ Sıraya Eklendi...\nSıra: {len(data)}\n\nSabırlı olun...\n\n#kuyruk`", quote=True)
    data.append(message)
    if len(data) == 1:
      add_task(message)

app.run()
