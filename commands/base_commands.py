from telegram import Update
from telegram.ext import (
    CallbackContext,
    ConversationHandler
)

class BaseCommands:
    
    def __init__(self) -> None:
        ...
        
    def send_basic_message(self, update: Update, context: CallbackContext, message: str) -> None:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=message, parse_mode="Markdown"
        )
        
    def create_conversation_handler(self, entry_points: list, states: dict, fallbacks: list, conversation_timeout: float = 20.0) -> ConversationHandler:
        sub_conv_handler = ConversationHandler(
            entry_points=entry_points,
            states=states,
            fallbacks=fallbacks,
            conversation_timeout=conversation_timeout,
        )
        
        return sub_conv_handler