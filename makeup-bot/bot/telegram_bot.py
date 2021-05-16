import logging
import os

from telegram.ext import CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram.ext import Updater

from bot.conversation import root
from bot.conversation.fsm import bot_states, bot_events
from bot.conversation.makeup.hair_makeup import HairMakeup
from bot.conversation.makeup.lips_makeup import LipsMakeup
from bot.utils import bot_utils

logger = logging.getLogger(os.path.basename(__file__))


class TelegramBot:
    def __init__(self, config, auth_chat_ids, face_aligner, face_segmenter):
        # Constructor
        self.config = config
        self.auth_chat_ids = auth_chat_ids
        self.updater = Updater(token=config["token"], use_context=True)
        self.bot = self.updater.bot
        self.dispatcher = self.updater.dispatcher

        # Makeup
        self.face_aligner = face_aligner
        self.face_segmenter = face_segmenter

        # Commands
        self.utils = bot_utils.BotUtils(config, auth_chat_ids, self.bot)
        self.root = root.RootCommand(config, auth_chat_ids, self.utils)
        self.hair_makeup = HairMakeup(config, auth_chat_ids, self.utils, self.face_aligner, self.face_segmenter)
        self.lips_makeup = LipsMakeup(config, auth_chat_ids, self.utils, self.face_aligner, self.face_segmenter)

        # FSM
        # Level 1 only callback (no warning)
        self.menu_handler = ConversationHandler(
            entry_points=[
                CallbackQueryHandler(self.hair_makeup.show_hair_colors,
                                     pattern='^' + str(bot_events.CHANGE_HAIR) + '$'),
                CallbackQueryHandler(self.lips_makeup.show_lip_colors,
                                     pattern='^' + str(bot_events.CHANGE_LIPS) + '$'),
            ],
            states={
                bot_states.MAKEUP: [
                    CallbackQueryHandler(self.hair_makeup.hair_makeup_context, pattern='^hair_color:\S+$'),
                    CallbackQueryHandler(self.lips_makeup.lips_makeup_context, pattern='^lips_color:\S+$')],
                bot_states.HAIR: [
                    MessageHandler(Filters.regex('^intensity 0.\d$') | Filters.photo, self.hair_makeup.apply_makeup),
                    CallbackQueryHandler(self.hair_makeup.apply_makeup_menu, pattern='^[{}{}{}]$'.format(
                        str(bot_events.STAY_HERE), str(bot_events.HAIR_COLOR), str(bot_events.EXIT_CLICK)))],
                bot_states.LIPS: [
                    MessageHandler(Filters.regex('^intensity 0.\d$') | Filters.photo, self.lips_makeup.apply_makeup),
                    CallbackQueryHandler(self.lips_makeup.apply_makeup_menu, pattern='^[{}{}{}]$'.format(
                        str(bot_events.STAY_HERE), str(bot_events.LIPS_COLOR), str(bot_events.EXIT_CLICK)))],
            },
            fallbacks=[CallbackQueryHandler(self.root.exit, pattern='^' + str(bot_events.EXIT_CLICK) + '$'),
                       CallbackQueryHandler(self.root.show_logged_menu, pattern='^' + str(bot_events.BACK_CLICK) + '$')],
            map_to_parent={
                bot_states.END: bot_states.LOGGED,
                bot_states.LOGGED: bot_states.LOGGED,
                bot_states.NOT_LOGGED: bot_states.NOT_LOGGED
            }
        )
        # Level 0
        self.conversationHandler = ConversationHandler(
            entry_points=[CommandHandler('start', callback=self.root.start)],
            states={
                bot_states.NOT_LOGGED: [CommandHandler('start', callback=self.root.start)],
                bot_states.CREDENTIALS: [MessageHandler(callback=self.root.credentials, filters=Filters.text)],
                bot_states.LOGGED: [CommandHandler('menu', callback=self.root.show_logged_menu), self.menu_handler],
            },
            fallbacks=[CallbackQueryHandler(self.root.exit, pattern='^' + str(bot_events.EXIT_CLICK) + '$')]
        )
        # Init handlers
        self.dispatcher.add_handler(self.conversationHandler)

    def start_polling(self):
        logger.info("Started Polling bot")
        self.updater.start_polling()

    def get_bot(self):
        return self.bot
