import os
from pyrogram import Client
from dotenv import load_dotenv

if os.path.exists('config.env'):
  load_dotenv('config.env')

api_id = int(os.environ.get("API_ID"))
heroku_app_name = os.environ.get('HEROKU_APP_NAME', None)
heroku_api_key = os.environ.get('HEROKU_API_KEY', None)
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
download_dir = os.environ.get("DOWNLOAD_DIR", "downloads/")
sudo_users = list(set(int(x) for x in os.environ.get("SUDO_USERS").split()))
send_logs_when_dying = str(os.environ.get("SEND_LOGS_WHEN_DYING", "True")).lower() == 'true'
owner = int(os.environ.get("OWNER"))

app = Client(":memory:", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

data = []

if not download_dir.endswith("/"):
  download_dir = str(download_dir) + "/"
if not os.path.isdir(download_dir):
  os.makedirs(download_dir)
