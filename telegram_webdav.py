from webdav3.client import Client
import telegram
from telegram import *
from telegram.ext import *
import logging
import os
import shutil
token='your_token'
telegram_id=1234  #your unique telegram user id, see telegram.User

options = {
 'webdav_hostname': "your_webdav_url",
 'webdav_login':    "username",
 'webdav_password': "password"
}
client = Client(options)

def clear_dir():
    dir='your_local_dir'
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)
# downloads a folder from your webdav to your path
def down_and_zip(client):
    client.download_sync(remote_path="remote_dir", local_path="your_local_dir")
    os.system("zip filename.zip your_local_dir")
def rm_zip():
    os.system("rm filename.zip") 

def start(update, context):
    if(update.message.from_user.id==telegram_id):
        down_and_zip(client)
        context.bot.send_document(chat_id=update.effective_chat.id, document=open('./docs.zip','rb'),timeout=20)
        clear_dir()
        rm_zip()
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="not user",parse_mode=telegram.ParseMode.HTML)
  

updater = Updater(token=token)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
