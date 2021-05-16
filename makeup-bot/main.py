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
    # Download models
    utils.download_models("1u4Zq6-mM3xsEswaaa3KeRqjytMSxxHOw", "unet-256.tflite")
    utils.download_models("1wNfbyCJ-8Z2XFGCbuL_heg5JrnVkSr5u", "shape_predictor_68_face_landmarks.dat")
    logger.info("Models downloaded")

    # DB
    authChatIds = dict()

    # Makeup
    face_aligner = FaceAligner(desired_face_width=256)
    face_segmenter = FaceSegmenter(256)

    # BOT
    telegram_bot = TelegramBot(config, authChatIds, face_aligner, face_segmenter)
    telegram_bot.start_polling()
