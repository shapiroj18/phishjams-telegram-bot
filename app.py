import os
import logging
import datetime
import telegram
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)

from phish_bot.phishnet_api import PhishNetAPI
from phish_bot.phishin_api import PhishINAPI

auth_key = os.environ.get("BOT_TOKEN")
heroku_app_url = os.environ.get("HEROKU_APP_URL")

phishnet_api = PhishNetAPI()
phishin_api = PhishINAPI()

# Enable Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get("PORT", "8443"))

# Start message
def start(update, context):
    """Send a message when the command /start is issued."""
    welcome_message = """
    \U0001F420 Welcome to the Phish Bot!

    See commands and functionality below:
    `/start`: shows this fun menu you see in front of you
    `/logo`: returns the classic rainbow logo
    `/daily_jam`: sends you a daily random jam from phish.net's jamcharts 
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=welcome_message, parse_mode="Markdown"
    )


# Send logo
def send_logo(update, context):
    """Send ye old phish logo"""
    logo_url = "http://4.bp.blogspot.com/_2CnQWIZQ3NY/SoDbSGrZnxI/AAAAAAAABVQ/tZ6OTg-AzyM/s320/phi.jpg"
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=logo_url)


# Send daily jam
def random_jam(context):
    """Sends daily jam"""
    job = context.job
    context.bot.send_audio(job.context, audio="http://www.phish.in/audio/000/020/111/20111.mp3") 
    # "http://www.largesound.com/ashborytour/sound/brobob.mp3"
    
    # song= "Sand"
    # date = "1999-12-13"
    # response = phishin_api.get_song_url(song=song, date=date)
    # if response.startswith("http"):
    #     links_text = f"""[Show Info]({phishnet_api.get_show_url(date)})\n[Show Audio](phish.in/{date})"""
    #     context.bot.send_audio(job.context, audio=response)       
    #     context.bot.send_message(job.context, text=links_text, parse_mode = "Markdown")


def remove_job_if_exists(name, context):
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def daily_jam(update, context):
    """Add a job to the queue"""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        # due = int(context.args[0])
        # if due < 0:
        #     update.message.reply_text("Sorry, we can't go back to the future")
        #     return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(
            random_jam,
            first=datetime.datetime.now(), #+ datetime.timedelta(days=1),
            interval=datetime.timedelta(seconds=5),
            context=chat_id,
            name=str(chat_id),
        )

        text = (
            'Daily random jams successfully started! To unset use "/unset_daily_jam".'
        )
        if job_removed:
            text += " Old one was removed"
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text("Usage: /daily_jam")


def unset_daily_jam(update, context):
    """Remove the job if the user changed their mind"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = (
        "Daily jams successfully cancelled"
        if job_removed
        else "You have no active daily random jams"
    )
    update.message.reply_text(text)


def error(update, context):
    """Log errors caused by updates"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # initialize bot
    updater = Updater(auth_key, use_context=True)
    dispatcher = updater.dispatcher

    # handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("logo", send_logo))
    dispatcher.add_handler(CommandHandler("daily_jam", daily_jam))
    dispatcher.add_handler(CommandHandler("unset_daily_jam", unset_daily_jam))

    # error handler
    dispatcher.add_error_handler(error)

    # Start bot
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=auth_key)
    updater.bot.set_webhook(heroku_app_url + auth_key)


if __name__ == "__main__":
    main()


# app = Flask(__name__)


# @app.route("/")
# def index():
#     return "."


# @app.route("/phish")
# def phish():
#     return render_template("phish.html")


# @app.route(f"/{auth_key}", methods=["POST"])
# def respond():

#     chat_id = update.message.chat.id
#     msg_id = update.message.message_id

#     text = update.message.text.encode("utf-8").decode().lower()

#     print("got message: ", text)

#     if text.startswith("mp3"):

#         # text must be of the format "/mp3 YYYY-MM-DD song_name"
#         parsed_text = text.split(", ")
#         if len(parsed_text) == 3:
#             response = phishin_api.get_song_url(parsed_text[1], parsed_text[2])
#             if response.startswith("http"):
#                 links_text = f""" \
#                 Find info for the show at [phish.net]({phishnet_api.get_show_url(parsed_text[2])})\n\
#                 Find audio for the full show at [phish.in](phish.in/{parsed_text[2]})\
#                 """
#                 bot.send_chat_action(chat_id=chat_id, action="typing")
#                 bot.send_message(
#                     chat_id=chat_id,
#                     text=links_text,
#                     parse_mode="Markdown",
#                     reply_to_message_id=msg_id,
#                 )
#                 bot.send_audio(chat_id=chat_id, audio=response)
#             else:
#                 bot.send_message(
#                     chat_id=chat_id,
#                     text=response,
#                     parse_mode="Markdown",
#                     reply_to_message_id=msg_id,
#                 )
#         else:
#             response = "The command must look like \n`mp3, song name, YYYY-MM-DD`"
#             bot.send_message(
#                 chat_id=chat_id,
#                 text=response,
#                 parse_mode="Markdown",
#                 reply_to_message_id=msg_id,
#             )

#     elif text == "random":
#         # should be able to enter random or year or song name
#         # lookup jam chart
#         # random date in jam chart
#         # send info about show on phish.net and relisten and/or phish.in link to song
#         # for relisten: get url from inspect > network (refresh page) > year (YYYY-MM-DD) > source_id (maybe in sources['review_count']['sets']['source_id'])
#         response = phishnet_api.get_jamchart_songs()
#         relisten_url = "https://relisten.net/phish/1991/12/04/david-bowie?source=162594"
#         message = f"Your song is {response[1]}"
#         audio_url = "https://phish.in/audio/000/031/671/31671.mp3"
#         caption = "Ya Mar 1999-03-05"

#         bot.send_message(chat_id=chat_id, text=message, reply_to_message_id=msg_id)
#         bot.send_audio(chat_id=chat_id, audio=audio_url, caption=caption)

#     elif text == "sponsor":

#         sponsorship_text = """ \
#         If you want to support the development of this project, please consider [contributing!](https://github.com/sponsors/shapiroj18)!
#         """

#         bot.send_message(
#             chat_id=chat_id,
#             text=sponsorship_text,
#             parse_mode="Markdown",
#             reply_to_message_id=msg_id,
#         )

#     else:
#         try:
#             text = re.sub(r"/W", "_", text)
#             bot.send_message(
#                 chat_id=chat_id,
#                 text="Not a phishable command \U0001F420",
#                 reply_to_message_id=msg_id,
#             )
#         except Exception:
#             bot.send_message(
#                 chat_id=chat_id,
#                 text="There was a problem in the name you used, please use a different name",
#                 reply_to_message_id=msg_id,
#             )

#     return "ok"


# @app.route("/setwebhook", methods=["GET", "POST"])
# def set_webhook():
#     s = bot.setWebhook(f"{url}{auth_key}")

#     if s:
#         return "webhook setup ok"
#     else:
#         return "webhook setup failed"


# if __name__ == "__main__":
#     app.run(threaded=True)
