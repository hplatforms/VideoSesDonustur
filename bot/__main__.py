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
        if owner != 0:
            try:
                await self.send_message(text="`SENİN GÜCÜN SAYESİNDE YENİDEN DOĞDUM SAHİP.`",
                    chat_id=owner)
            except Exception as t:
                LOGGER.error(str(t))

    async def stop(self, *args):
        if owner != 0:
            texto = f"BUGÜN BENİM ÖLÜM GÜNÜM.\nYAŞADIĞIM SÜRE: `{ReadableTime(time.time() - botStartTime)}`"
            try:
                if send_logs_when_dying:
                    await self.send_document(document='log.txt', caption=texto, chat_id=owner)
                else:
                    await self.send_message(text=texto, chat_id=owner)
            except Exception as t:
                LOGGER.warning(str(t))
        await super().stop()
        LOGGER.info(msg="App Stopped.")
        exit()

app = Bot()
app.run()
