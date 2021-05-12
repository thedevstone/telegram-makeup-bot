import logging
import os

from bot.telegram_bot import TelegramBot
from file_manager.path_utilities import ROOT_DIR
from utils import utils

if __name__ == '__main__':
    # INIT
    utils.init_logger()
    logger = logging.getLogger(os.path.basename(__file__))
    config = utils.load_yaml("../config.yaml")
    logger.info("Configuration loaded")

    # DB
    authChatIds = dict()

    # BOT
    telegram_bot = TelegramBot(config, authChatIds)
    telegram_bot.start_polling()