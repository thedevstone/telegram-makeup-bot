import logging
import os

from telegram import Update, File, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from bot.conversation.fsm import bot_states, bot_events
from bot.conversation.makeup.utils import get_color_keyboard, get_image_from_bytearray, COLORS, image_to_bytearray
from bot.utils.bot_utils import BotUtils
from makeup.makeup import lips

logger = logging.getLogger(os.path.basename(__file__))


class LipsMakeup(object):
    # Constructor
    def __init__(self, config, auth_chat_ids, conversation_utils: BotUtils, face_aligner, face_segmenter):
        self.config = config
        self.auth_chat_ids = auth_chat_ids
        self.utils = conversation_utils
        # Makeup
        self.face_aligner = face_aligner
        self.face_segmenter = face_segmenter

    @staticmethod
    def show_lip_colors(update: Update, _context: CallbackContext):
        update.callback_query.answer()
        text = "Select a color"
        kb_markup = get_color_keyboard('lips')
        update.callback_query.edit_message_text(text=text, reply_markup=kb_markup)
        return bot_states.MAKEUP

    def lips_makeup_context(self, update: Update, context: CallbackContext):
        makeup_config = self.auth_chat_ids[update.effective_chat.id]['makeup']
        update.callback_query.answer()
        color = update.callback_query.data
        color = color.split(':')[1]
        makeup_config['lip-color'] = color
        text = 'Send me a good photo\n\nIncrease effect with: "intensity 0.x"'
        message = update.callback_query.edit_message_text(text=text)
        self.utils.check_last_and_delete(update, context, message)
        return bot_states.LIPS

    def apply_makeup(self, update: Update, context: CallbackContext):
        self.utils.check_last_and_delete(update, context, None)
        makeup_config = self.auth_chat_ids[update.effective_chat.id]['makeup']
        if update.message.text:
            message_text = update.message.text
            intensity = float(message_text.split(' ')[1])
            makeup_config['lip-intensity'] = intensity
            update.message.reply_text(text="Saturate lips mode 'on', intensity = {}".format(intensity))
            return bot_states.LIPS
        if update.message.photo:
            file: File = context.bot.getFile(update.message.photo[-1].file_id)
            if file is not None:
                image_bytearray: bytes = file.download_as_bytearray()  # temporarily dump image to file and read as OpenCV frame
                image = get_image_from_bytearray(image_bytearray)

                image, landmarks = self.face_aligner.align(image)
                masks = self.face_segmenter.segment_image_keep_aspect_ratio(image)
                color = COLORS[makeup_config['lip-color']]
                force = makeup_config['lip-intensity']
                pronounced = force > 0
                lips_makeup_image = lips(image, masks, color, pronounced=pronounced, force=force)

                temp_file = image_to_bytearray(lips_makeup_image)
                update.message.reply_photo(temp_file)

                keyboard = [
                    [InlineKeyboardButton(text="Stay here", callback_data=str(bot_events.STAY_HERE))],
                    [InlineKeyboardButton(text="Change lips color", callback_data=str(bot_events.LIPS_COLOR))],
                    [InlineKeyboardButton(text="⬅", callback_data=str(bot_events.BACK_CLICK))]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text(text="What do you want to do?", reply_markup=reply_markup)
                return bot_states.LIPS
        else:
            return bot_states.LOGGED

    def apply_makeup_menu(self, update: Update, _context: CallbackContext):
        update.callback_query.answer()
        data = update.callback_query.data
        if data == bot_events.STAY_HERE:
            self.utils.delete_user_message(update.callback_query.message)
            return bot_states.LIPS
        elif data == bot_events.LIPS_COLOR:
            text = "Select a color"
            kb_markup = get_color_keyboard('lips')
            update.callback_query.edit_message_text(text=text, reply_markup=kb_markup)
            return bot_states.MAKEUP
        else:
            self.utils.delete_user_message(update.callback_query.message)
            return bot_states.LOGGED
