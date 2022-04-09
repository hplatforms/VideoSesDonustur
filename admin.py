import shutil
import psutil
import math

import requests
import heroku3

from config import HEROKU_APP_NAME, HEROKU_API_KEY

from pyrogram import filters
from pyrogram.types import (
    Message
)
from config import OWNER_ID
from pyrogram import Client

@Client.on_message(filters.command("reset") & filters.user(OWNER_ID))
async def restart(_, m: Message):
    restart_msg = await m.reply_text(text="`İşleniyor...`")
    await restart_msg.edit("`Yeniden başlatılıyor! Lütfen bekle...`")
    try:
        if HEROKU_API_KEY is not None:
            heroku_conn = heroku3.from_key(HEROKU_API_KEY)
            server = heroku_conn.app(HEROKU_APP_NAME)
            server.restart()
        else:
            await restart_msg.edit("`Heroku değişkenlerini ekleyin.`")
    except Exception as e:
        await restart_msg.edit(f"**Error:** `{e}`") 
