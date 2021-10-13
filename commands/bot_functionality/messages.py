import os
import re
import logging

from telegram.ext import (
    ConversationHandler,
)

from commands.lib.api_requests import APIRequests
from commands.lib.regex import Regex


class Messages:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.api_requests = APIRequests()
        self.regex = Regex()
        self.heroku_flask_url = os.getenv("HEROKU_FLASK_URL")

    # Start message
    def start_message(self) -> str:
        """Initial Message"""
        message = (
            f"""\U0001F420 Welcome to the Phish Bot! Send /features for bot commands!"""
        )

        return message

    # features message
    def features_message(self):
        """Features of bot"""
        message = f"""
        You can send me commands like:
        /queue (let's you add a random or specific jam to the online player: {self.heroku_flask_url})
        /randomjam (sends a random Phish jam)
        /subscribedailyjam (random daily jam emails)
        /unsubscribedailyjam (remove daily jam emails)
        /subscribemjm (reminder when mystery jam monday is posted)
        /unsubscribemjm (remove MJM reminders)
        /code (links to code repositories and contributing)
        /help (help menu)
        """

        return message

    # help message
    def help_message(self):
        """Features of bot"""
        message = f"""Type /features for full bot commands."""

        return message

    # subscribe to daily jam cancel_functions
    SUBSCRIBE = range(1)

    def get_subscriber_email_daily_jam(self, update, context):
        """Get email from user"""
        update.message.reply_text(
            "Please send the email you would like to subscribe to daily random Phish Jams, or send /cancel."
        )

        return self.SUBSCRIBE

    def subscribe_daily_jam(self, update, context):
        """Subscribe for random daily jam emails"""
        user = update.message.from_user
        email = update.message.text
        chat_id = update.message.chat_id

        match = self.regex.email_basic_regex(email)
        while match is not None:

            self.logger.info(
                "Subscribe email sent by %s: %s",
                user.first_name + " " + user.last_name,
                email,
            )

            message_response = self.api_requests.post_subscribe_daily_jams(
                self.heroku_flask_url, email, chat_id
            )

            if "subscribed successfully" in message_response:
                message = f"You have successfully subscribed {email}!"
                update.message.reply_text(message)
            elif "error" in message_response:
                message = f"There was an error. Please try again later or reach out to shapiroj18@gmail.com to report a bug."
                update.message.reply_text(message)

            return ConversationHandler.END

        else:
            self.logger.info(
                "Subscribe email sent by %s: %s",
                user.first_name + " " + user.last_name,
                email,
            )
            message = f"Invalid email, please type again below, or send /cancel."
            update.message.reply_text(message)

    def cancel_sub_daily_jam(self, update, context):
        user = update.message.from_user
        self.logger.info("User %s cancelled the conversation.", user.first_name)
        update.message.reply_text(
            "Subscription skipped, type /subscribedailyjam if you want to start over."
        )

        return ConversationHandler.END

    # unsubscribe to daily jam cancel_functions
    UNSUBSCRIBE = range(1)

    def get_unsubscribe_email_daily_jam(self, update, context):
        """Get email from user"""
        update.message.reply_text(
            "Please send the email you would like to unsubscribe to daily random Phish Jams, or send /cancel."
        )

        return self.UNSUBSCRIBE

    def unsubscribe_daily_jam(self, update, context):

        """Subscribe for random daily jam emails"""
        user = update.message.from_user
        email = update.message.text

        match = self.regex.email_basic_regex(email)
        while match is not None:

            self.logger.info(
                "Unsubscribe email sent by %s: %s",
                user.first_name + " " + user.last_name,
                email,
            )
            message_response = self.api_requests.post_unsubscribe_daily_jams(
                self.heroku_flask_url, email
            )

            if "removed successfully" in message_response:
                message = f"You have successfully unsubscribed {email}. If you would like to resubscribe, send /subscribedailyjam."
                update.message.reply_text(message)
            elif "did not exist" in message_response:
                message = f"{email} was not found in the database."
                update.message.reply_text(message)
            elif "error" in message_response:
                message = f"There was an error. Please try again later or reach out to shapiroj18@gmail.com to report a bug."
                update.message.reply_text(message)

            return ConversationHandler.END

        else:
            self.logger.info(
                "Unsubscribe email sent by %s: %s",
                user.first_name + " " + user.last_name,
                email,
            )
            message = f"Invalid email, please type again below, or send /cancel."
            update.message.reply_text(message)

    # Jam Handler
    ADDJAM, ADDSPECIFICJAM = range(2)

    def add_queue_jam(self, update, context):
        """Get random or specific jam data from user"""

        chat_id = update.message.chat_id
        data = {
            "chat_id": chat_id,
        }
        r = httpx.post(f"{self.heroku_flask_url}/checkqueuestatus", data=data)
        print(r.json())

        if r.json()["response"] == "Maximums not hit":

            reply_keyboard = [["Random"], ["I had a specific one in mind"]]
            update.message.reply_text(
                f"Did you want to add a specific or random jam to the playlist?",
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True
                ),
            )

            return ADDJAM

        else:
            update.message.reply_text(r.json()["response"])
            return ConversationHandler.END
