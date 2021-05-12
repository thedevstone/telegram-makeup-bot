from telegram import Update

from bot.conversation.fsm import bot_states
from bot.conversation.makeup.utils import get_color_keyboard
from bot.utils.bot_utils import BotUtils, logger


class LipsMakeup(object):
    # Constructor
    def __init__(self, config, auth_chat_ids, conversation_utils: BotUtils):
        self.config = config
        self.auth_chat_ids = auth_chat_ids
        self.utils = conversation_utils

    def lips_makeup_click(self, update: Update, context):
        update.callback_query.answer()
        text = "Select a color"
        kb_markup = get_color_keyboard('lips')
        update.callback_query.edit_message_text(text=text, reply_markup=kb_markup)
        return bot_states.MAKEUP

    def lips_makeup_context(self, update: Update, context):
        logger.info(update.callback_query.data)
