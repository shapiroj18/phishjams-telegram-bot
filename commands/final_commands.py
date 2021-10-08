from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    Filters
)

from commands.base_commands import BaseCommands
from commands.messages import Messages

class FinalCommands:
    
    def __init__(self) -> None:
        # load libraries
        self.basic_commands = BaseCommands()
        self.messages = Messages()
    
    
    # Start message
    def start(self, update, context) -> None:
        message = self.messages.start_message()
        self.basic_commands.send_basic_message(update, context, message)
        
    def features(self, update, context) -> None:
        message = self.messages.features_message()
        self.basic_commands.send_basic_message(update, context, message)
        
    def help(self, update, context) -> None:
        message = self.messages.help_message()
        self.basic_commands.send_basic_message(update, context, message)
        
    def subscription_conversation_handler(self) -> ConversationHandler:
        sub_conversation_handler = self.basic_commands.create_conversation_handler(
            entry_points = [
                CommandHandler("subscribedailyjam", self.messages.get_subscriber_email_daily_jam)
            ],
            states = {
                self.messages.SUBSCRIBE: [
                    MessageHandler(Filters.text & ~Filters.command, self.messages.subscribe_daily_jam)
                ]
            },
            fallbacks= [CommandHandler("cancel", self.messages.cancel_sub_daily_jam)]
        )
        
        return sub_conversation_handler