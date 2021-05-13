import logging
import os

from bot.telegram_bot import TelegramBot
from utils import utils

if __name__ == '__main__':
    # INIT
    utils.init_logger()
    logger = logging.getLogger(os.path.basename(__file__))
    config = utils.load_yaml("../config.yaml")
    logger.info("Configuration loaded")

    # DB
    authChatIds = dict()

    # Makeup
    face_aligner = None  # FaceAligner(desired_face_width=512)
    face_segmenter = None  # FaceSegmenter(512)

    # BOT
    telegram_bot = TelegramBot(config, authChatIds, face_aligner, face_segmenter)
    telegram_bot.start_polling()
