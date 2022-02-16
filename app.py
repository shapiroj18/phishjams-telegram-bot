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
    queue_jam_handler = commands.queue_jam_handler()
    
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
    dispatcher.add_handler(queue_jam_handler)

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
