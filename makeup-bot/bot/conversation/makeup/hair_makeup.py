import logging
import os
from io import BytesIO

import PIL.Image
import numpy as np
from telegram import Update, File
from telegram.ext import CallbackContext

from bot.conversation.fsm import bot_states
from bot.conversation.makeup.utils import get_color_keyboard, COLORS
from bot.utils.bot_utils import BotUtils
from makeup.makeup import hair

logger = logging.getLogger(os.path.basename(__file__))


class HairMakeup(object):
    # Constructor
    def __init__(self, config, auth_chat_ids, conversation_utils: BotUtils, face_aligner, face_segmenter):
        self.config = config
        self.auth_chat_ids = auth_chat_ids
        self.utils = conversation_utils
        # Makeup
        self.face_aligner = face_aligner
        self.face_segmenter = face_segmenter

    def show_hair_colors(self, update: Update, context: CallbackContext):
        update.callback_query.answer()
        text = "Select a color"
        kb_markup = get_color_keyboard('hair')
        update.callback_query.edit_message_text(text=text, reply_markup=kb_markup)
        return bot_states.MAKEUP

    def hair_makeup_context(self, update: Update, context: CallbackContext):
        makeup_config = self.auth_chat_ids[update.effective_chat.id]['makeup']
        update.callback_query.answer()
        color = update.callback_query.data
        color = color.split(':')[1]
        makeup_config['hair-color'] = color
        logger.info(makeup_config['hair-color'])
        text = 'Send me a good photo\n\nPS If you have dark hair send: "saturation 0.x"'
        update.callback_query.edit_message_text(text=text)
        return bot_states.HAIR

    def apply_makeup(self, update: Update, context: CallbackContext):
        makeup_config = self.auth_chat_ids[update.effective_chat.id]['makeup']
        if update.message.text:
            message_text = update.message.text
            saturate_value = message_text.split(' ')[1]
            makeup_config['hair-saturate'] = saturate_value
            logger.info(makeup_config['hair-saturate'])
        if update.message.photo:
            file: File = context.bot.getFile(update.message.photo[-1].file_id)
            if file is not None:
                image: bytes = file.download_as_bytearray()  # temporarily dump image to file and read as OpenCV frame
                temp_file = BytesIO(image)
                image = PIL.Image.open(temp_file)
                image = np.array(image)

                image, landmarks = self.face_aligner.align(image)
                masks = self.face_segmenter.segment_image_keep_aspect_ratio(image)
                color = COLORS[makeup_config['hair-color']]
                hair_makeup_image = hair(image, masks, color, dark_hair=False, force=0.2)

                temp_file = BytesIO()
                temp_file.name = 'Segmented: {}.png'.format(color)
                im = PIL.Image.fromarray(hair_makeup_image)
                im.save(temp_file, format="png")
                temp_file.seek(0)
                update.message.reply_photo(temp_file)
