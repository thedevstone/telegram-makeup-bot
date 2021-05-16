import logging
import os

from bot.telegram_bot import TelegramBot
from face_alignment.face_aligner import FaceAligner
from file_manager.path_utilities import ROOT_DIR
from segmentation.face_segmenter import FaceSegmenter
from utils import utils

if __name__ == '__main__':
    # INIT
    utils.init_logger()
    logger = logging.getLogger(os.path.basename(__file__))
    config = utils.load_yaml(os.path.join(ROOT_DIR, "config.yaml"))
    logger.info("Configuration loaded")

    # DB
    authChatIds = dict()

    # Makeup
    face_aligner = FaceAligner(desired_face_width=256)
    face_segmenter = FaceSegmenter(256)

    # BOT
    telegram_bot = TelegramBot(config, authChatIds, face_aligner, face_segmenter)
    telegram_bot.start_polling()
