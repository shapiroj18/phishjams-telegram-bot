import os
import logging
import datetime
import httpx
import re
from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

from commands.bot_functionality.final_commands import FinalCommands


def setup():

    # load environment variables
    load_dotenv()
    auth_key = os.getenv("TELEGRAM_BOT_TOKEN")
    app_url = os.getenv("APP_URL")

    # Enable Logging
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)

    PORT = int(os.environ.get("PORT", "8443"))
    logging.info(PORT)

    # load commands
    commands = FinalCommands()

    return auth_key, app_url, logger, PORT, commands


auth_key, app_url, logger, PORT, commands = setup()

# Jam Handler
ADDJAM, ADDSPECIFICJAM = range(2)


def add_queue_jam(update, context):
    """Get random or specific jam data from user"""

    heroku_flask_url = os.getenv("HEROKU_FLASK_URL")
    chat_id = update.message.chat_id
    data = {
        "chat_id": chat_id,
    }
    r = httpx.post(f"{heroku_flask_url}/checkqueuestatus", data=data)
    print(r.json())

    if r.json()["response"] == "Maximums not hit":

        reply_keyboard = [["Random"], ["I had a specific one in mind"]]
        update.message.reply_text(
            f"Did you want to add a specific or random jam to the playlist?",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )

        return ADDJAM

    else:
        update.message.reply_text(r.json()["response"])
        return ConversationHandler.END


def queue_jam(update, context):
    """Get random or specific jam and add to playlist"""

    heroku_flask_url = os.getenv("HEROKU_FLASK_URL")

    if update.message.text.lower() == "random":
        while True:
            user = update.message.from_user.first_name
            chat_id = update.message.chat_id
            data = {
                "platform": "Telegram",
                "chat_id": chat_id,
                "user_first_name": user,
            }
            r = httpx.post(f"{heroku_flask_url}/addtoqueue", data=data)
            if r.json()["jam_url"]:
                break

        song = r.json()["song"]
        date = r.json()["date"]
        logger.info("User %s has added %s %s.", user, song, date)
        update.message.reply_text(
            f"{song} from {date} has been added! Please find the playlist at {heroku_flask_url}",
        )

        return ConversationHandler.END

    else:
        update.message.reply_text(
            "Please enter the jam you would like to add.\nFor example: 2000-06-14 Twist"
        )

        return ADDSPECIFICJAM


def queue_specific_jam(update, context):
    """Adds specific jam if user inputs correctly. Otherwise, ends conversation."""
    response = update.message.text
    user = update.message.from_user
    chat_id = update.message.chat_id
    jam_date = response.split()[0]
    match_jam_date = re.search(r"\d\d\d\d-\d\d-\d\d", jam_date)
    song_list = response.split()[1:]
    song = " ".join(song_list)
    heroku_flask_url = os.getenv("HEROKU_FLASK_URL")

    while match_jam_date is not None:
        logger.info(
            "Jam sent by %s: %s",
            user.first_name + " " + user.last_name,
            jam_date + " " + song,
        )

        data = {
            "platform": "Telegram",
            "chat_id": chat_id,
            "user_first_name": user.first_name,
            "song": song,
            "jam_date": jam_date,
        }
        r = httpx.post(f"{heroku_flask_url}/addtoqueue", data=data)
        json_resp = r.json()

        if "response" in json_resp:
            update.message.reply_text(json_resp["response"])

            return ADDSPECIFICJAM

        else:
            logger.info(
                "User %s has added %s %s.",
                user.first_name + " " + user.last_name,
                song,
                jam_date,
            )
            update.message.reply_text(
                f"{jam_date} {song} has been added! Please find the playlist at {heroku_flask_url}",
            )

            return ConversationHandler.END

    else:
        logger.info(
            "Jam sent by %s: %s",
            user.first_name + " " + user.last_name,
            jam_date + " " + song,
        )
        message = (
            f'Invalid format, please type again as "YYYY-MM-DD song" , or send /cancel.'
        )
        update.message.reply_text(message)


def cancel_queue_jam(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Skipped adding a song to the queue, type /queue if you want to start over."
    )

    return ConversationHandler.END

def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Command not recognized. Send /cancel to exit a process or /features for possible commands.",
    )

def error(update, context):
    """Log errors caused by updates"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # initialize bot
    updater = Updater(auth_key, use_context=True)
    dispatcher = updater.dispatcher

    sub_conv_handler = commands.subscription_conversation_handler()
    unsub_conv_handler = commands.unsubscription_conversation_handler()
    random_jam_handler = commands.random_jam_handler()

    queue_jam_handler = ConversationHandler(
        entry_points=[CommandHandler("queue", add_queue_jam)],
        states={
            ADDJAM: [MessageHandler(Filters.text & ~Filters.command, queue_jam)],
            ADDSPECIFICJAM: [
                MessageHandler(Filters.text & ~Filters.command, queue_specific_jam)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_queue_jam)],
        conversation_timeout=60.0,
    )

    # define handlers
    dispatcher.add_handler(CommandHandler("start", commands.start))
    dispatcher.add_handler(CommandHandler("features", commands.features))
    dispatcher.add_handler(CommandHandler("help", commands.help))
    dispatcher.add_handler(
        CommandHandler(
            "subscribemjm", commands.subscribe_mystery_jam_monday_notifications
        )
    )
    dispatcher.add_handler(
        CommandHandler(
            "unsubscribemjm", commands.unsubscribe_mystery_jam_monday_notifications
        )
    )
    dispatcher.add_handler(CommandHandler("code", commands.code))
    dispatcher.add_handler(sub_conv_handler)
    dispatcher.add_handler(unsub_conv_handler)
    dispatcher.add_handler(random_jam_handler)
    # dispatcher.add_handler(queue_jam_handler)

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
