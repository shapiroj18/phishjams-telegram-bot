import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from phish_bot.phishnet_api import PhishNetAPI
from phish_bot.phishin_api import PhishINAPI

auth_key = os.environ.get("BOT_TOKEN")
app_name = os.environ.get("HEROKU_APP_NAME")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    welcome_message = """
    \U0001F420 Welcome to the Phish Bot!

    See commands below!
    `logo`: returns the classic rainbow logo
    `mp3, song, YYYY-MM-DD`: returns the audio of a track on a specific date 
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=welcome_message, parse_mode="Markdown"
    )


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")


def echo(update, context):
    """Echo the user message."""
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Not a very phishy command \U0001F420. Type "/help" if you need some ideas.',
    )


def main():
    updater = Updater(auth_key, use_context=True)

    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    PORT = os.environ.get("PORT")

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=auth_key)
    updater.bot.setWebhook(f"https://{app_name}.herokuapp.com/{auth_key}")
    updater.idle()


if __name__ == "__main__":
    main()
