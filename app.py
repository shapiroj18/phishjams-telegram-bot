import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from phish_bot.phishnet_api import PhishNetAPI
from phish_bot.phishin_api import PhishINAPI

auth_key = os.environ.get("BOT_TOKEN")
app_name = os.environ.get("HEROKU_APP_NAME")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    
def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main():
    updater = Updater(auth_key, use_context=True)
    
    dispatcher = updater.dispatcher
    
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    
    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
    PORT = os.environ.get('PORT')
    

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=auth_key)
    updater.bot.setWebhook(f"https://{app_name}.herokuapp.com/{auth_key}")
    updater.idle()
    
if __name__ == '__main__':
    main()