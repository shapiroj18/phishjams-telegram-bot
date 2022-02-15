import os
import re
import logging
import datetime
import httpx

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
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

    def code_keyboard(self):
        """Shows information for codebase of this project"""
        buttons = ["Telegram Bot", "PhishJams Backend", "PhishJams Frontend"]
        urls = [
            "https://github.com/shapiroj18/phishjams-telegram-bot",
            "https://github.com/shapiroj18/phishjams-backend",
            "https://github.com/shapiroj18/phishjams-frontend"
        ]

        return buttons, urls

    def code_message(self):
        """Message to send with information of codebase for this project"""
        message = f"You can find the source code for this project below. If you want to contribute, please reach out to shapiroj18@gmail.com!"
        return message

    # subscribe to mystery jam monday notifications
    def subscribemjm(self, update, context):
        """Subscribe for mjm notifications"""
        user = update.message.from_user
        chat_id = update.message.chat_id

        self.logger.info(
            "MJM subscription sent by %s",
            user.first_name + " " + user.last_name,
        )

        message_response = self.api_requests.post_subscribe_mjm(
            self.heroku_flask_url, chat_id
        )

        if "subscribed successfully" in message_response:
            message = f"You have successfully subscribed to MJM reminders!"
            update.message.reply_text(message)
        elif "error" in message_response:
            message = f"There was an error. Please try again later or reach out to shapiroj18@gmail.com to report a bug."
            update.message.reply_text(message)

    # unsubscribe to mystery jam monday notifications
    def unsubscribemjm(self, update, context):
        """Subscribe for mjm notifications"""
        user = update.message.from_user
        chat_id = update.message.chat_id

        self.logger.info(
            "MJM unsubscription sent by %s",
            user.first_name + " " + user.last_name,
        )

        message_response = self.api_requests.post_unsubscribe_mjm(
            self.heroku_flask_url, chat_id
        )
        if "removed successfully" in message_response:
            message = f"You have successfully unsubscribed from MJM reminders. If you would like to resubscribe, send /subscribemjm. "
            update.message.reply_text(message)
        elif "did not exist" in message_response:
            message = f"You were not found in the database."
            update.message.reply_text(message)
        elif "error" in message_response:
            message = f"There was an error. Please try again later or reach out to shapiroj18@gmail.com to report a bug."
            update.message.reply_text(message)

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
            
    # Random Jam Handler
    RANDOMJAM, TRUE_RANDOM, YEAR_RANDOM, SONG_RANDOM, YEARSONG_RANDOM = range(5)
    
    def random_jam(self, update, context):
        """Get random jam by year or song name"""

        reply_keyboard = [["Random"], ["Year"], ["Song"], ["Year and Song"]]
        update.message.reply_text(
            f"Do you want a truly random jam, or a jam by year and/or song?",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )

        return self.RANDOMJAM
    
    def get_random_jam_keyboard(self, song=None, year=None):
        heroku_flask_url = os.getenv("HEROKU_FLASK_URL")

        data = {"song": song, "year": year}
        print(data)

        r = httpx.post(f"{heroku_flask_url}/randomjam", data=data)
        print(r.json())
        json_resp = r.json()

        if "response" in json_resp:
            return json_resp["response"], None
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

            return json_resp, reply_markup
        
    def random_jam_response(self, update, context):
        """Gets random jam for user."""
        response = update.message.text
        user = update.message.from_user
        chat_id = update.message.chat_id

        if response.lower() == "random":
            json_resp, reply_markup = self.get_random_jam_keyboard()
            update.message.reply_text(
                f"Random Jam:\n{json_resp['song']} {json_resp['date']}",
                reply_markup=reply_markup,
            )
            return ConversationHandler.END
        elif response.lower() == "year":
            update.message.reply_text("Which year?")
            return self.YEAR_RANDOM
        elif response.lower() == "song":
            update.message.reply_text("Which song?")
            return self.SONG_RANDOM
        elif response.lower() == "year and song":
            update.message.reply_text(
                "Which year and song (make sure you specify the year and then the song (e.g. 2003 Scents and Subtle Sounds)?"
            )
            return self.YEARSONG_RANDOM
        else:
            update.message.reply_text(
                "Something went wrong, please try again by typing /randomjam."
            )
            return ConversationHandler.END


    def year_random(self, update, context):
        response = update.message.text
        year = response
        match_year = re.search("^\d{4}$", year)
        while match_year is not None:

            json_resp, reply_markup = self.get_random_jam_keyboard(year=year)
            print(json_resp)
            if json_resp == "No jams found for that entry":
                update.message.reply_text(
                    "Not a valid year. Please try again with /randomjam and a valid year (jamcharts start in 1984)",
                )
                return ConversationHandler.END
            else:
                update.message.reply_text(
                    f"Random Jam:\n{json_resp['song']} {json_resp['date']}",
                    reply_markup=reply_markup,
                )
                return ConversationHandler.END

        else:
            update.message.reply_text(
                "Incorrect format. Make sure you correctly use a four digit year."
            )

    def song_random(self, update, context):
        response = update.message.text
        song = response
        json_resp, reply_markup = self.get_random_jam_keyboard(song=song)
        update.message.reply_text(
            f"Random Jam:\n{json_resp['song']} {json_resp['date']}",
            reply_markup=reply_markup,
        )
        return ConversationHandler.END


    def yearsong_random(self, update, context):
        response = update.message.text
        match_year_song = re.search(r"^\d{4}\s.*$", response)
        while match_year_song is not None:

            year = response.split()[0]
            song_list = response.split()[1:]
            song = " ".join(song_list)
            print(year, song)

            json_resp, reply_markup = self.get_random_jam_keyboard(song=song, year=year)
            update.message.reply_text(
                f"Random Jam:\n{json_resp['song']} {json_resp['date']}",
                reply_markup=reply_markup,
            )
            return ConversationHandler.END

        else:
            update.message.reply_text(
                "Incorrect format. Make sure you specify the year and then the song (e.g. 2003 Scents and Subtle Sounds)."
            )
            
    def cancel_random_jam(self, update, context):
        user = update.message.from_user
        self.logger.info("User %s canceled the conversation.", user.first_name)
        update.message.reply_text(
            "Skipped getting random jam, type /randomjam if you want to start over."
        )

        return ConversationHandler.END