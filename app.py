import os
import telegram
import re
from time import sleep

from flask import Flask, request, render_template

from phish_bot.phishnet_api import PhishNetAPI
from phish_bot.phishin_api import PhishINAPI

auth_key = os.environ.get('BOT_TOKEN')
url = os.environ.get('URL')

bot = telegram.Bot(token=auth_key)
phishnet_api = PhishNetAPI()
phishin_api = PhishINAPI()

welcome_message = """
\U0001F420 Welcome to the Phish Bot!

See commands below!
`logo`: returns the classic rainbow logo
`mp3, song, YYYY-MM-DD`: returns the audio of a track on a specific date 
"""

# Generously created based on https://www.toptal.com/python/telegram-bot-tutorial-python

app = Flask(__name__)

@app.route("/")
def index():
    return '.'

@app.route("/phish")
def phish():
    return render_template("base.html")

@app.route(f"/{auth_key}", methods=["POST"])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    
    text = update.message.text.encode('utf-8').decode().lower()
    
    print("got message: ", text)
    
    if text == "/start":
        bot_welcome = welcome_message
        bot.send_message(chat_id=chat_id, text=bot_welcome, parse_mode='Markdown', reply_to_message_id=msg_id)
        
    elif text == "logo":
        logo_url = 'http://4.bp.blogspot.com/_2CnQWIZQ3NY/SoDbSGrZnxI/AAAAAAAABVQ/tZ6OTg-AzyM/s320/phi.jpg'
        bot.send_photo(chat_id=chat_id, photo=logo_url, reply_to_message_id=msg_id)
        
    elif text.startswith('mp3'):
        
        # text must be of the format "/mp3 YYYY-MM-DD song_name"
        parsed_text = text.split(', ')
        if len(parsed_text) == 3:
            response = phishin_api.get_song_url(parsed_text[1], parsed_text[2])
            if response.startswith('http'):
                links_text = f""" \
                You can find info for the show at [phish.net]({phishnet_api.get_show_url(parsed_text[2])}) \
                You can find audio for the full show at [phish.in](phish.in/{parsed_text[2]}) \
                """
                bot.send_message(chat_id=chat_id, text=links_text, parse_mode='Markdown', reply_to_message_id=msg_id)
                bot.send_audio(chat_id=chat_id, audio=response)
            else:
                bot.send_message(chat_id=chat_id, text=response, parse_mode='Markdown', reply_to_message_id=msg_id)
        else:
            response = 'The command must look like \n`mp3, song name, YYYY-MM-DD`'
            bot.send_message(chat_id=chat_id, text=response, parse_mode='Markdown', reply_to_message_id=msg_id)
        
    elif text == "random":
        # should be able to enter random or year or song name
        # lookup jam chart
        # random date in jam chart
        # send info about show on phish.net and relisten and/or phish.in link to song
            # for relisten: get url from inspect > network (refresh page) > year (YYYY-MM-DD) > source_id (maybe in sources['review_count']['sets']['source_id'])
        response = phishnet_api.get_jamchart_songs()
        relisten_url = 'https://relisten.net/phish/1991/12/04/david-bowie?source=162594'
        message = f"Your song is {response[1]}"
        audio_url = 'https://phish.in/audio/000/031/671/31671.mp3'
        caption = "Ya Mar 1999-03-05"
        
        bot.send_message(chat_id=chat_id, text=message, reply_to_message_id=msg_id)
        bot.send_audio(chat_id=chat_id, audio=audio_url, caption=caption)
        
    else:
        try:
            text = re.sub(r"/W", "_", text)
            bot.send_message(chat_id=chat_id, text="Not a phishable command \U0001F420", reply_to_message_id=msg_id)
        except Exception:
            bot.send_message(chat_id=chat_id, text="There was a problem in the name you used, please use a different name", reply_to_message_id=msg_id)
    
    return 'ok'

@app.route("/setwebhook", methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook(f'{url}{auth_key}')
    
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"
    

# @app.route("/<name>")
# def hello_name(name):
#     return f"hello {name}"

if __name__ == '__main__':
    app.run(threaded=True)