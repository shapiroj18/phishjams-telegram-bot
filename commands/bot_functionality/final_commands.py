from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from commands.bot_functionality.base_commands import BaseCommands
from commands.bot_functionality.messages import Messages


class FinalCommands:
    def __init__(self) -> None:
        # load libraries
        self.base_commands = BaseCommands()
        self.messages = Messages()

    # Start message
    def start(self, update, context) -> None:
        message = self.messages.start_message()
        self.base_commands.send_basic_message(update, context, message)

    def features(self, update, context) -> None:
        message = self.messages.features_message()
        self.base_commands.send_basic_message(update, context, message)

    def help(self, update, context) -> None:
        message = self.messages.help_message()
        self.base_commands.send_basic_message(update, context, message)

    def code(self, update, context) -> None:
        buttons, urls = self.messages.code_keyboard()
        keyboard = self.base_commands.create_inline_keyboard(buttons, urls)
        message = self.messages.code_message()
        self.base_commands.send_basic_message(
            update, context, message, reply_markup=keyboard
        )

    def subscribe_mystery_jam_monday_notifications(self, update, context) -> None:
        self.messages.subscribemjm(update, context)

    def unsubscribe_mystery_jam_monday_notifications(self, update, context) -> None:
        self.messages.unsubscribemjm(update, context)

    def subscription_conversation_handler(self):
        sub_conversation_handler = self.base_commands.create_conversation_handler(
            entry_points=[
                CommandHandler(
                    "subscribedailyjam", self.messages.get_subscriber_email_daily_jam
                )
            ],
            states={
                self.messages.SUBSCRIBE: [
                    MessageHandler(
                        Filters.text & ~Filters.command,
                        self.messages.subscribe_daily_jam,
                    )
                ]
            },
            fallbacks=[CommandHandler("cancel", self.messages.cancel_sub_daily_jam)],
        )

        return sub_conversation_handler

    def unsubscription_conversation_handler(self):
        unsub_conversation_handler = self.base_commands.create_conversation_handler(
            entry_points=[
                CommandHandler(
                    "unsubscribedailyjam", self.messages.get_unsubscribe_email_daily_jam
                )
            ],
            states={
                self.messages.UNSUBSCRIBE: [
                    MessageHandler(
                        Filters.text & ~Filters.command,
                        self.messages.unsubscribe_daily_jam,
                    )
                ]
            },
            fallbacks=[CommandHandler("cancel", self.messages.cancel_sub_daily_jam)],
        )

        return unsub_conversation_handler
