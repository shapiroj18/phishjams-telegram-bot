import os
import telegram
import re

from flask import Flask, request

from phish_bot.phishnet_api import test

auth_key = os.environ.get('BOT_TOKEN')
url = os.environ.get('URL')

bot = telegram.Bot(token=auth_key)

welcome_message = """
\U0001F420 Welcome to the Phish Bot. See command below!

1. /logo returns the classic rainbow logo
"""

# Generously created based on https://www.toptal.com/python/telegram-bot-tutorial-python

app = Flask(__name__)

@app.route("/")
def index():
    return '.'

@app.route("/Phish")
def phish():
    pass

@app.route(f"/{auth_key}", methods=["POST"])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    
    text = update.message.text.encode('utf-8').decode()
    
    print("got message: ", text)
    
    if text == "/start":
        bot_welcome = welcome_message
        
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
        
    elif text == "/logo":
        logo_url = 'http://4.bp.blogspot.com/_2CnQWIZQ3NY/SoDbSGrZnxI/AAAAAAAABVQ/tZ6OTg-AzyM/s320/phi.jpg'
        bot.sendPhoto(chat_id=chat_id, photo=logo_url, reply_to_message_id=msg_id)
        
    elif text == "/random":
        # should be able to enter random or year or song name
        # lookup jam chart
        # random date in jam chart
        # send info about show on phish.net and relisten and/or phish.in link to song
        message = test.test_fun()
        bot.sendMessage(chat_id=chat_id, text=message, reply_to_message_id=msg_id)
        
    else:
        try:
            text = re.sub(r"/W", "_", text)
            
            url = f"https://en.wikipedia.org/wiki/Brown_bear#/media/File:2010-kodiak-bear-1.jpg"
            bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id, caption="Not a phishable command \U0001F420")
        except Exception:
            bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please use a different name", reply_to_message_id=msg_id)
    
    return 'ok'

@app.route("/setwebhook", methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook(f'{url}{auth_key}')
    
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"
    

@app.route("/<name>")
def hello_name(name):
    return f"hello {name}"

if __name__ == '__main__':
    app.run(threaded=True)