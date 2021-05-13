import logging
import os

from telegram import Update, File, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from bot.conversation.fsm import bot_states, bot_events
from bot.conversation.makeup.utils import get_color_keyboard, COLORS, get_image_from_bytearray, image_to_bytearray
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

    @staticmethod
    def show_hair_colors(update: Update, _context: CallbackContext):
        update.callback_query.answer()
        text = "Select a color"
        kb_markup = get_color_keyboard('hair')
        update.callback_query.edit_message_text(text=text, reply_markup=kb_markup)
        return bot_states.MAKEUP

    def hair_makeup_context(self, update: Update, _context: CallbackContext):
        makeup_config = self.auth_chat_ids[update.effective_chat.id]['makeup']
        update.callback_query.answer()
        color = update.callback_query.data
        color = color.split(':')[1]
        makeup_config['hair-color'] = color
        text = 'Send me a good photo\n\nIncrease effect with: "intensity 0.x"'
        update.callback_query.edit_message_text(text=text)
        return bot_states.HAIR

    def apply_makeup(self, update: Update, context: CallbackContext):
        makeup_config = self.auth_chat_ids[update.effective_chat.id]['makeup']
        if update.message.text:
            message_text = update.message.text
            saturate_value = float(message_text.split(' ')[1])
            makeup_config['hair-intensity'] = saturate_value
            logger.info(makeup_config['hair-intensity'])
            return bot_states.HAIR
        if update.message.photo:
            file: File = context.bot.getFile(update.message.photo[-1].file_id)
            if file is not None:
                image_bytearray: bytes = file.download_as_bytearray()  # temporarily dump image to file and read as OpenCV frame
                image = get_image_from_bytearray(image_bytearray)

                image, landmarks = self.face_aligner.align(image)
                masks = self.face_segmenter.segment_image_keep_aspect_ratio(image)
                color = COLORS[makeup_config['hair-color']]
                force = makeup_config['hair-intensity']
                dark_hair = force > 0
                hair_makeup_image = hair(image, masks, color, dark_hair=dark_hair, force=force)

                temp_file = image_to_bytearray(hair_makeup_image)
                update.message.reply_photo(temp_file)

                keyboard = [
                    [InlineKeyboardButton(text="Send me another photo", callback_data=str(bot_events.STAY_HERE))],
                    [InlineKeyboardButton(text="Change hair color", callback_data=str(bot_events.HAIR_COLOR))],
                    [InlineKeyboardButton(text="❌", callback_data=str(bot_events.EXIT_CLICK))]
                    ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text(text="What do you want to do?", reply_markup=reply_markup)
                return bot_states.HAIR
        else:
            return bot_states.HAIR

    @staticmethod
    def apply_makeup_menu(update: Update, _context: CallbackContext):
        update.callback_query.answer()
        data = update.callback_query.data
        if data == bot_events.STAY_HERE:
            return bot_states.HAIR
        elif data == bot_events.HAIR_COLOR:
            text = "Select a color"
            kb_markup = get_color_keyboard('hair')
            update.callback_query.edit_message_text(text=text, reply_markup=kb_markup)
            return bot_states.MAKEUP
        else:
            update.callback_query.message.delete()
            return bot_states.LOGGED
