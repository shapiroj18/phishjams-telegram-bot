from telegram import Update
from telegram.ext import (
    CallbackContext,
)

class BaseCommands:
    
    def __init__(self) -> None:
        ...
        
    def send_basic_message(self, update: Update, context: CallbackContext, message: str) -> None:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=message, parse_mode="Markdown"
        )