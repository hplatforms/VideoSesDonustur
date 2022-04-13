from pyrogram import filters
from pyrogram import filters
import requests
import heroku3
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
import logging
import os
import time
from bot.utils import ReadableTime

from pyrogram import filters
from pyrogram.types import (
    Message
)
from pyrogram import Client

from bot import app, data, sudo_users, heroku_api_key, heroku_app_name, owner, send_logs_when_dying
from bot.helper.utils import add_task
from pyrogram.types.bots_and_keyboards import InlineKeyboardButton, InlineKeyboardMarkup
from .translation import Translation
from pyrogram import Client, filters

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)
botStartTime = time.time()


async def start(self):
        if not os.path.isdir(DOWNLOAD_LOCATION): os.makedirs(DOWNLOAD_LOCATION)
        await super().start()
        me = await self.get_me()
        self.username = '@' + me.username
        LOGGER.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        if sudo_users != 0:
            try:
                await self.send_message(text="`SENİN GÜCÜN SAYESİNDE YENİDEN DOĞDUM SAHİP.`",
                    chat_id=sudo_users)
            except Exception as t:
                LOGGER.error(str(t))

async def stop(self, *args):
    if owner != 0:
        texto = f"BUGÜN BENİM ÖLÜM GÜNÜM.\nYAŞADIĞIM SÜRE: `{ReadableTime(time.time() - botStartTime)}`"
        try:
                await self.send_document(document='log.txt', caption=texto, chat_id=sudo_users)
            else:
                await self.send_message(text=texto, chat_id=sudo_users)
        except Exception as t:
            LOGGER.warning(str(t))
    await super().stop()
    LOGGER.info(msg="App Stopped.")
    exit()

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

@app.on_message(filters.command('log') & filters.user(sudo_users))
async def sendLogs(client, message):
    with open('log.txt', 'rb') as f:
        try:
            await client.send_document(document=f,
                                       file_name=f.name, reply_to_message_id=message.message_id,
                                       chat_id=message.chat.id, caption=f.name)
        except Exception as e:
            await message.reply_text(str(e))

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

@app.on_message(filters.command("restart"))
async def restart(_, m: Message):
    restart_message = await m.reply_text(text="`Ölmek üzereyim...\nbana hayat verdiğin için teşekkürler😢`")
    try:
        if heroku_api_key is not None:
            heroku_conn = heroku3.from_key(heroku_api_key)
            server = heroku_conn.app(heroku_app_name)
            server.restart() 
            await restart_message.edit('`Senin ellerinde can verdim kurt bakışlım.`')
            time.sleep(2)
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
