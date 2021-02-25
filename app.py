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
    <b>You can send me commands like:</b>
    /randomjam (sends a random Phish jam)
    /subscribedailyjam (random daily jam emails)
    /unsubscribedailyjam (remove daily jam emails)
    /subscribemjm (reminder when mystery jam monday is posted)
    /unsubscribemjm (remove MJM reminders)
    /code (links to code repositories and contributing)
    /support (information on supporting development)
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


def get_subscriber_email_daily_jam(update, context):
    """Get email from user"""
    update.message.reply_text(
        "Please send the email you would like to subscribe to daily random Phish Jams, or send /cancel."
    )

    return SUBSCRIBE


def subscribedailyjam(update, context):
    """Subscribe for random daily jam emails"""
    heroku_flask_url = os.getenv("HEROKU_FLASK_URL")
    user = update.message.from_user
    email = update.message.text
    chat_id = update.message.chat_id

    match = re.search(r"\S+@\S+", email)
    while match is not None:

        logger.info(
            "Subscribe email sent by %s: %s",
            user.first_name + " " + user.last_name,
            email,
        )
        data = {"email": email, "platform": "Telegram", "chat_id": chat_id}
        r = httpx.post(f"{heroku_flask_url}/subscribedailyjams", data=data)
        print(f"flask response: {r.json()}")
        message_resp = r.json()["message"]
        if "subscribed successfully" in message_resp:
            message = f"You have successfully subscribed {email}!"
            update.message.reply_text(message)
        elif "error" in message_resp:
            message = f"There was an error. Please try again later or reach out to shapiroj18@gmail.com to report a bug."
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


def cancel_sub_daily_jam(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Subscription skipped, type /subscribe if you want to start over."
    )

    return ConversationHandler.END


# Unsubscribe Handler
UNSUBSCRIBE = range(1)


def get_unsubscribe_email_daily_jam(update, context):
    """Get email from user"""
    update.message.reply_text(
        "Please send the email you would like to unsubscribe to daily random Phish Jams, or send /cancel."
    )

    return UNSUBSCRIBE


def unsubscribedailyjam(update, context):

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
        r = httpx.post(f"{heroku_flask_url}/unsubscribedailyjams", data=data)
        print(f"flask response: {r.json()}")
        message_resp = r.json()["message"]
        if "removed successfully" in message_resp:
            message = f"You have successfully unsubscribed {email}. If you would like to resubscribe, send /subscribedailyjam."
            update.message.reply_text(message)
        elif "did not exist" in message_resp:
            message = f"{email} was not found in the database."
            update.message.reply_text(message)
        elif "error" in message_resp:
            message = f"There was an error. Please try again later or reach out to shapiroj18@gmail.com to report a bug."
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


def cancel_unsub_daily_jam(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Subscription skipped, type /unsubscribe if you want to start over."
    )

    return ConversationHandler.END


# subscribe to MJM
def subscribemjm(update, context):
    """Subscribe for mjm notifications"""
    heroku_flask_url = os.getenv("HEROKU_FLASK_URL")
    user = update.message.from_user
    chat_id = update.message.chat_id

    logger.info(
        "MJM subscription sent by %s",
        user.first_name + " " + user.last_name,
    )

    data = {"platform": "Telegram", "chat_id": chat_id}
    r = httpx.post(f"{heroku_flask_url}/subscribemjm", data=data)
    print(f"flask response: {r.json()}")
    message_resp = r.json()["message"]
    if "subscribed successfully" in message_resp:
        message = f"You have successfully subscribed to MJM reminders!"
        update.message.reply_text(message)
    elif "error" in message_resp:
        message = f"There was an error. Please try again later or reach out to shapiroj18@gmail.com to report a bug."
        update.message.reply_text(message)


# unsubscribe to MJM
def unsubscribemjm(update, context):
    """Subscribe for mjm notifications"""
    heroku_flask_url = os.getenv("HEROKU_FLASK_URL")
    user = update.message.from_user
    chat_id = update.message.chat_id

    logger.info(
        "MJM unsubscription sent by %s",
        user.first_name + " " + user.last_name,
    )

    data = {"chat_id": chat_id}
    r = httpx.post(f"{heroku_flask_url}/unsubscribemjm", data=data)
    print(f"flask response: {r.json()}")
    message_resp = r.json()["message"]
    if "removed successfully" in message_resp:
        message = f"You have successfully unsubscribed from MJM reminders. If you would like to resubscribe, send /subscribemjm. "
        update.message.reply_text(message)
    elif "did not exist" in message_resp:
        message = f"You were not found in the database."
        update.message.reply_text(message)
    elif "error" in message_resp:
        message = f"There was an error. Please try again later or reach out to shapiroj18@gmail.com to report a bug."
        update.message.reply_text(message)


def get_random_jam_keyboard(update, context):
    heroku_flask_url = os.getenv("HEROKU_FLASK_URL")

    arguments = context.args
    song = " ".join(arguments)

    data = {"song": song}

    r = httpx.post(f"{heroku_flask_url}/randomjam", data=data)
    print(r.json())
    json_resp = r.json()

    if "response" in json_resp:
        update.message.reply_text(json_resp["response"])
    else:
        relisten_formatted_date = datetime.datetime.strptime(
            json_resp["date"], "%Y-%m-%d"
        ).strftime("%Y/%m/%d")

        if json_resp["jam_url"]:
            jam_url = json_resp["jam_url"]
        else:
            jam_url = f"https://phish.in/{json_resp['date']}"

        keyboard = [
            [
                InlineKeyboardButton("Jam Link", url=jam_url),
            ],
            [
                InlineKeyboardButton(
                    "Show Link (Phish.in)", url=f"https://phish.in/{json_resp['date']}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "Show Link (Relisten)",
                    url=f"https://relisten.net/phish/{relisten_formatted_date}",
                ),
            ],
            [
                InlineKeyboardButton("Show Info", url=json_resp["show_info"]),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(
            f"Random Jam:\n{json_resp['song']} {json_resp['date']}",
            reply_markup=reply_markup,
        )


def code(update, context):

    keyboard = [
        [
            InlineKeyboardButton(
                "Telegram Bot", url="https://github.com/shapiroj18/phish-telegram-bot"
            ),
        ],
        [
            InlineKeyboardButton(
                "Web Application", url="https://github.com/shapiroj18/phish-bot"
            ),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="You can find the source code for this project below. If you want to contribute, please reach out to shapiroj18@gmail.com!",
        reply_markup=reply_markup,
    )


def support(update, context):

    keyboard = [
        [
            InlineKeyboardButton("Ko-Fi", url="https://ko-fi.com/shapiroj18"),
        ],
        [
            InlineKeyboardButton(
                "GitHub", url="https://github.com/sponsors/shapiroj18"
            ),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="This bot is not cheap to build! If you want to support the development of this project, please consider contributing.",
        reply_markup=reply_markup,
    )


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

    sub_conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("subscribedailyjam", get_subscriber_email_daily_jam)
        ],
        states={
            SUBSCRIBE: [
                MessageHandler(Filters.text & ~Filters.command, subscribedailyjam)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel_sub_daily_jam)],
        conversation_timeout=20.0,
    )

    unsub_conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("unsubscribedailyjam", get_unsubscribe_email_daily_jam)
        ],
        states={
            UNSUBSCRIBE: [
                MessageHandler(Filters.text & ~Filters.command, unsubscribedailyjam)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_unsub_daily_jam)],
        conversation_timeout=20.0,
    )

    # handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("features", features))
    dispatcher.add_handler(CommandHandler("subscribemjm", subscribemjm))
    dispatcher.add_handler(CommandHandler("unsubscribemjm", unsubscribemjm))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("randomjam", get_random_jam_keyboard))
    dispatcher.add_handler(CommandHandler("code", code))
    dispatcher.add_handler(CommandHandler("support", support))
    dispatcher.add_handler(sub_conv_handler)
    dispatcher.add_handler(unsub_conv_handler)

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
