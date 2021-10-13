from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler


class BaseCommands:
    def __init__(self) -> None:
        ...

    def send_basic_message(
        self, update: Update, context: CallbackContext, message: str, reply_markup=None
    ) -> None:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode="Markdown",
            reply_markup=reply_markup,
        )

    def create_inline_keyboard(self, buttons: list, urls: list):
        # check buttons and urls lists are the same length
        if len(buttons) != len(urls):
            raise RuntimeError("Length of buttons and urls must be equivalent")
        else:
            keyboard = []
            for i in range(len(buttons)):
                keyboard.append([InlineKeyboardButton(buttons[i], url=urls[i])])

            reply_markup = InlineKeyboardMarkup(keyboard)

            return reply_markup

    def create_conversation_handler(
        self,
        entry_points: list,
        states: dict,
        fallbacks: list,
        conversation_timeout: float = 20.0,
    ):
        sub_conv_handler = ConversationHandler(
            entry_points=entry_points,
            states=states,
            fallbacks=fallbacks,
            conversation_timeout=conversation_timeout,
        )

        return sub_conv_handler
