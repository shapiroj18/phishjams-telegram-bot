import os
import logging
import datetime
import httpx
import re
import json
from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

load_dotenv()

auth_key = os.getenv("TELEGRAM_BOT_TOKEN")
app_url = os.getenv("APP_URL")

# Enable Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get("PORT", "8443"))

# Start message
def start(update, context):
    """Initial Message"""
    welcome_message = """
    \U0001F420 Welcome to the Phish Bot! Send "/features" for bot commands!
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=welcome_message, parse_mode="Markdown"
    )


def features(update, context):
    """Features of bot"""
    features_message = """
    <b>You can send me messages like:</b>
    /subscribe (random daily jam emails)
    /unsubscribe (remove daily jam emails)
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=features_message, parse_mode="HTML"
    )


def help(update, context):
    """Features of bot"""
    features_message = """
    <b>You can send me messages like:</b>
    /subscribe (random daily jam emails)
    /unsubscribe (remove daily jam emails)
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=features_message, parse_mode="HTML"
    )


# Subscription Handler
SUBSCRIBE = range(1)


def get_subscriber_email(update, context):
    """Get email from user"""
    update.message.reply_text(
        "Please send the email you would like to subscribe to daily random Phish Jams, or send /cancel."
    )

    return SUBSCRIBE


def subscribe(update, context):

    """Subscribe for random daily jam emails"""
    heroku_flask_url = os.getenv("HEROKU_FLASK_URL")
    user = update.message.from_user
    email = update.message.text

    match = re.search(r"\S+@\S+", email)
    while match is not None:

        logger.info(
            "Subscribe email sent by %s: %s",
            user.first_name + " " + user.last_name,
            email,
        )
        data = {"email": email, "platform": "Telegram"}
        r = httpx.post(f"{heroku_flask_url}/subscribe", data=data)
        print(r.json())
        message = f"You have successfully subscribed {email}!"
        update.message.reply_text(message)

        return ConversationHandler.END

    else:
        logger.info(
            "Subscribe email sent by %s: %s",
            user.first_name + " " + user.last_name,
            email,
        )
        message = f"Invalid email, please type again below, or send /cancel."
        update.message.reply_text(message)


def cancel_sub(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Subscription skipped, type /subscribe if you want to start over."
    )

    return ConversationHandler.END


# End Subscription Handler

# Unsubscribe Handler
UNSUBSCRIBE = range(1)


def get_unsubscribe_email(update, context):
    """Get email from user"""
    update.message.reply_text(
        "Please send the email you would like to unsubscribe to daily random Phish Jams, or send /cancel."
    )

    return SUBSCRIBE


def unsubscribe(update, context):

    """Subscribe for random daily jam emails"""
    heroku_flask_url = os.getenv("HEROKU_FLASK_URL")
    user = update.message.from_user
    email = update.message.text

    match = re.search(r"\S+@\S+", email)
    while match is not None:

        logger.info(
            "Unsubscribe email sent by %s: %s",
            user.first_name + " " + user.last_name,
            email,
        )
        data = {"email": email, "platform": "Telegram"}
        r = httpx.post(f"{heroku_flask_url}/unsubscribe", data=data)
        print(r.json())
        message = f"You have successfully unsubscribed {email}!"
        update.message.reply_text(message)

        return ConversationHandler.END

    else:
        logger.info(
            "Unsubscribe email sent by %s: %s",
            user.first_name + " " + user.last_name,
            email,
        )
        message = f"Invalid email, please type again below, or send /cancel."
        update.message.reply_text(message)


def cancel_unsub(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Subscription skipped, type /unsubscribe if you want to start over."
    )

    return ConversationHandler.END


# # Send daily jam
# def get_random_jam_keyboard():

#     song, date = phishnet_api.get_random_jamchart()
#     relisten_formatted_date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime(
#         "%Y/%m/%d"
#     )
#     keyboard = [
#         [
#             InlineKeyboardButton(
#                 "Jam Link", url=phishin_api.get_song_url(song=song, date=date)
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 "Show Link (Phish.in)", url=f"https://phish.in/{date}"
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 "Show Link (Relisten)",
#                 url=f"https://relisten.net/phish/{relisten_formatted_date}",
#             ),
#         ],
#         [
#             InlineKeyboardButton("Show Info", url=phishnet_api.get_show_url(date)),
#         ],
#     ]

#     reply_markup = song, date, InlineKeyboardMarkup(keyboard)

#     return reply_markup


# def random_jam(update, context):
#     """Sends random jam"""

#     song, date, reply_markup = get_random_jam_keyboard()
#     logging.info(f"Pulled {song}, {date}")
#     try:
#         context.bot.send_message(
#             chat_id=update.effective_chat.id,
#             text=f"*Random Jam \U0001F420*\n{song} {date}",
#             parse_mode="Markdown",
#             reply_markup=reply_markup,
#         )
#     except:
#         random_jam(update, context)


# def random_jam_daily(context):
#     """Sends daily jam"""
#     job = context.job

#     song, date, reply_markup = get_random_jam_keyboard()
#     logging.info(f"Pulled {song}, {date}")
#     try:
#         context.bot.send_message(
#             job.context,
#             text=f"*Daily Squeeze \U0001F420*\n{song} {date}",
#             parse_mode="Markdown",
#             reply_markup=reply_markup,
#         )
#     except:
#         random_jam_daily(context)


# def remove_job_if_exists(name, context):
#     """Remove job with given name. Returns whether job was removed."""
#     current_jobs = context.job_queue.get_jobs_by_name(name)
#     if not current_jobs:
#         return False
#     for job in current_jobs:
#         job.schedule_removal()
#     return True


# def daily_jam(update, context):
#     """Add a job to the queue"""
#     chat_id = update.message.chat_id
#     try:
#         job_removed = remove_job_if_exists(str(chat_id), context)

#         # run daily at noon
#         context.job_queue.run_daily(
#             random_jam_daily,
#             time=datetime.time(17),
#             context=chat_id,
#             name=str(chat_id),
#         )

#         text = "Daily random jams successfully started! You will receive them each day at 12pm EST.\nTo unset use /unset."
#         update.message.reply_text(text)

#     except (IndexError, ValueError):
#         update.message.reply_text("Usage: /daily_jam")


# def unset_daily_jam(update, context):
#     """Remove the job if the user changed their mind"""
#     chat_id = update.message.chat_id
#     job_removed = remove_job_if_exists(str(chat_id), context)
#     text = (
#         "Daily jams successfully cancelled"
#         if job_removed
#         else "You have no active daily random jams"
#     )
#     update.message.reply_text(text)


# def sponsor(update, context):
#     sponsorship_text = """ \
#         If you want to support the development of this project, please consider contributing!\n[Patreon](https://www.patreon.com/shapiroj18)\n[GitHub](https://github.com/sponsors/shapiroj18)
#         """

#     context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text=sponsorship_text,
#         parse_mode="Markdown",
#     )


def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Command not recognized. Send "/features" for possible commands.',
    )


def error(update, context):
    """Log errors caused by updates"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # initialize bot
    updater = Updater(auth_key, use_context=True)
    dispatcher = updater.dispatcher

    sub_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("subscribe", get_subscriber_email)],
        states={
            SUBSCRIBE: [MessageHandler(Filters.text & ~Filters.command, subscribe)]
        },
        fallbacks=[CommandHandler("cancel", cancel_sub)],
    )

    unsub_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("unsubscribe", get_unsubscribe_email)],
        states={
            SUBSCRIBE: [MessageHandler(Filters.text & ~Filters.command, unsubscribe)]
        },
        fallbacks=[CommandHandler("cancel", cancel_unsub)],
    )

    # handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("features", features))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(sub_conv_handler)
    dispatcher.add_handler(unsub_conv_handler)
    # dispatcher.add_handler(CommandHandler("subscribe", subscribe))
    # dispatcher.add_handler(CommandHandler("randomjam", random_jam))
    # dispatcher.add_handler(CommandHandler("dailyjam", daily_jam))
    # dispatcher.add_handler(CommandHandler("unset", unset_daily_jam))
    # dispatcher.add_handler(CommandHandler("sponsor", sponsor))

    # non-understood commands
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # error handler
    dispatcher.add_error_handler(error)

    # Start bot
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=auth_key)
    updater.bot.set_webhook(app_url + auth_key)
    updater.idle()


if __name__ == "__main__":
    main()
