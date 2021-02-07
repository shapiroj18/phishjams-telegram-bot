import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN =  os.environ.get("TELEGRAM_BOT_TOKEN")
APP_URL = os.environ.get("APP_URL")
PORT = int(os.environ.get('PORT', 5000))

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(APP_URL + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()



# import os
# import logging
# import datetime
# from dotenv import load_dotenv
# from telegram import InlineKeyboardMarkup, InlineKeyboardButton
# from telegram.ext import (
#     Updater,
#     CommandHandler,
#     MessageHandler,
#     Filters,
# )

# load_dotenv()

# auth_key = os.environ.get("TELEGRAM_BOT_TOKEN")
# print(auth_key)
# app_url = os.environ.get("APP_URL")
# print(app_url)

# # Enable Logging
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )
# logger = logging.getLogger(__name__)

# PORT = int(os.environ.get("PORT", "8443"))

# # Start message
# def start(update, context):
#     """Send a message when the command /start is issued."""
#     welcome_message = """
#     Welcome to the Phish Bot!

#     See commands and functionality below:
#     `/start` Shows full menu of commands
#     `/randomjam` Sends random jam from phish.net's jamcharts
#     `/dailyjam` Schedules daily random jam sends
#     `/unset` Undoes daily random jam sends
#     `/logo` Sends photo of the classic logo
#     """
#     context.bot.send_message(
#         chat_id=update.effective_chat.id, text=welcome_message, parse_mode="Markdown"
#     )


# # Send logo
# def send_logo(update, context):
#     """Send ye old phish logo"""
#     logo_url = "http://4.bp.blogspot.com/_2CnQWIZQ3NY/SoDbSGrZnxI/AAAAAAAABVQ/tZ6OTg-AzyM/s320/phi.jpg"
#     context.bot.send_photo(chat_id=update.effective_chat.id, photo=logo_url)


# # # Send daily jam
# # def get_random_jam_keyboard():

# #     song, date = phishnet_api.get_random_jamchart()
# #     relisten_formatted_date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime(
# #         "%Y/%m/%d"
# #     )
# #     keyboard = [
# #         [
# #             InlineKeyboardButton(
# #                 "Jam Link", url=phishin_api.get_song_url(song=song, date=date)
# #             ),
# #         ],
# #         [
# #             InlineKeyboardButton(
# #                 "Show Link (Phish.in)", url=f"https://phish.in/{date}"
# #             ),
# #         ],
# #         [
# #             InlineKeyboardButton(
# #                 "Show Link (Relisten)",
# #                 url=f"https://relisten.net/phish/{relisten_formatted_date}",
# #             ),
# #         ],
# #         [
# #             InlineKeyboardButton("Show Info", url=phishnet_api.get_show_url(date)),
# #         ],
# #     ]

# #     reply_markup = song, date, InlineKeyboardMarkup(keyboard)

# #     return reply_markup


# # def random_jam(update, context):
# #     """Sends random jam"""

# #     song, date, reply_markup = get_random_jam_keyboard()
# #     logging.info(f"Pulled {song}, {date}")
# #     try:
# #         context.bot.send_message(
# #             chat_id=update.effective_chat.id,
# #             text=f"*Random Jam \U0001F420*\n{song} {date}",
# #             parse_mode="Markdown",
# #             reply_markup=reply_markup,
# #         )
# #     except:
# #         random_jam(update, context)


# # def random_jam_daily(context):
# #     """Sends daily jam"""
# #     job = context.job

# #     song, date, reply_markup = get_random_jam_keyboard()
# #     logging.info(f"Pulled {song}, {date}")
# #     try:
# #         context.bot.send_message(
# #             job.context,
# #             text=f"*Daily Squeeze \U0001F420*\n{song} {date}",
# #             parse_mode="Markdown",
# #             reply_markup=reply_markup,
# #         )
# #     except:
# #         random_jam_daily(context)


# # def remove_job_if_exists(name, context):
# #     """Remove job with given name. Returns whether job was removed."""
# #     current_jobs = context.job_queue.get_jobs_by_name(name)
# #     if not current_jobs:
# #         return False
# #     for job in current_jobs:
# #         job.schedule_removal()
# #     return True


# # def daily_jam(update, context):
# #     """Add a job to the queue"""
# #     chat_id = update.message.chat_id
# #     try:
# #         job_removed = remove_job_if_exists(str(chat_id), context)

# #         # run daily at noon
# #         context.job_queue.run_daily(
# #             random_jam_daily,
# #             time=datetime.time(17),
# #             context=chat_id,
# #             name=str(chat_id),
# #         )

# #         text = "Daily random jams successfully started! You will receive them each day at 12pm EST.\nTo unset use /unset."
# #         update.message.reply_text(text)

# #     except (IndexError, ValueError):
# #         update.message.reply_text("Usage: /daily_jam")


# # def unset_daily_jam(update, context):
# #     """Remove the job if the user changed their mind"""
# #     chat_id = update.message.chat_id
# #     job_removed = remove_job_if_exists(str(chat_id), context)
# #     text = (
# #         "Daily jams successfully cancelled"
# #         if job_removed
# #         else "You have no active daily random jams"
# #     )
# #     update.message.reply_text(text)


# # def sponsor(update, context):
# #     sponsorship_text = """ \
# #         If you want to support the development of this project, please consider contributing!\n[Patreon](https://www.patreon.com/shapiroj18)\n[GitHub](https://github.com/sponsors/shapiroj18)
# #         """

# #     context.bot.send_message(
# #         chat_id=update.effective_chat.id,
# #         text=sponsorship_text,
# #         parse_mode="Markdown",
# #     )


# def unknown(update, context):
#     context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text="Command not recognized. Write /start for possible commands.",
#     )


# def error(update, context):
#     """Log errors caused by updates"""
#     logger.warning('Update "%s" caused error "%s"', update, context.error)


# def main():
#     # initialize bot
#     updater = Updater(auth_key, use_context=True)
#     dispatcher = updater.dispatcher

#     # handlers
#     dispatcher.add_handler(CommandHandler("start", start))
#     dispatcher.add_handler(CommandHandler("logo", send_logo))
#     # dispatcher.add_handler(CommandHandler("randomjam", random_jam))
#     # dispatcher.add_handler(CommandHandler("dailyjam", daily_jam))
#     # dispatcher.add_handler(CommandHandler("unset", unset_daily_jam))
#     # dispatcher.add_handler(CommandHandler("sponsor", sponsor))

#     # non-understood commands
#     dispatcher.add_handler(MessageHandler(Filters.command, unknown))

#     # error handler
#     dispatcher.add_error_handler(error)

#     # Start bot
#     updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=auth_key)
#     updater.bot.set_webhook(app_url + auth_key)
#     updater.idle()


# if __name__ == "__main__":
#     main()
