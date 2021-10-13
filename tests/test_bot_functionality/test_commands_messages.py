import os
from dotenv import load_dotenv
from commands.bot_functionality.messages import Messages

load_dotenv()

messages = Messages()


def test_start_message():
    assert (
        messages.start_message()
        == f"""\U0001F420 Welcome to the Phish Bot! Send /features for bot commands!"""
    )


def test_features_message():
    heroku_flask_url = os.getenv("HEROKU_FLASK_URL")
    assert (
        messages.features_message()
        == f"""
        You can send me commands like:
        /queue (let's you add a random or specific jam to the online player: {heroku_flask_url})
        /randomjam (sends a random Phish jam)
        /subscribedailyjam (random daily jam emails)
        /unsubscribedailyjam (remove daily jam emails)
        /subscribemjm (reminder when mystery jam monday is posted)
        /unsubscribemjm (remove MJM reminders)
        /code (links to code repositories and contributing)
        /help (help menu)
        """
    )
    
def test_help_message():
    assert messages.help_message() == f"""Type /features for full bot commands."""
    
def test_code_keyboard():
    assert messages.code_keyboard() == (["Telegram Bot", "Web App"], ["https://github.com/shapiroj18/phish-telegram-bot", "https://github.com/shapiroj18/phish-bot"])
    
def test_code_message():
    assert messages.code_message() == f"You can find the source code for this project below. If you want to contribute, please reach out to shapiroj18@gmail.com!"


def test_help_message():
    assert messages.help_message() == f"""Type /features for full bot commands."""


def test_subscribe_range():
    assert messages.SUBSCRIBE == range(1)
