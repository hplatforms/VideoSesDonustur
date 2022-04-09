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

@app.on_message(filters.command("restart") & filters.user(OWNER_ID))
async def restart(_, m: Message):
    restart_msg = await m.reply_text(text="`İntihar ediyom bekle...`")
    await restart_msg.edit("`Ölmek üzereyim...`")
    try:
        if HEROKU_API_KEY is not None:
            heroku_conn = heroku3.from_key(HEROKU_API_KEY)
            server = heroku_conn.app(HEROKU_APP_NAME)
            server.restart()
        else:
            await restart_msg.edit("`Heroku Api Key ve uygulama adını ekleyin.`")
    except Exception as e:
        await restart_msg.edit(f"**İntihar bile edemedim:** `{e}`")