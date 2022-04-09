import shutil
import psutil
import math

import requests
import heroku3

from pyrogram import filters
from pyrogram.types import (
    Message
)
from pyrogram import Client

@app.on_message(filters.command("restart") & filters.user(OWNER_ID))
async def restart(_, m: Message):
    restart_message = await m.reply_text(text="`İntihar ediyom bekle...`")
    await restart_message.edit("`Ölmek üzereyim...`")
    try:
        if HEROKU_API_KEY is not None:
            heroku_conn = heroku3.from_key(HEROKU_API_KEY)
            server = heroku_conn.app(HEROKU_APP_NAME)
            server.restart()
        else:
            await restart_message.edit("`Heroku Api Key ve uygulama adını ekleyin.`")
    except Exception as e:
        await restart_message.edit(f"**İntihar bile edemedim:** `{e}`")
