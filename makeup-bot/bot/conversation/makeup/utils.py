from io import BytesIO

import PIL
import numpy as np
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.conversation.fsm import bot_events

COLORS = {'red': [255, 26, 26], 'green': [50, 150, 50], 'blue': [0, 0, 204], 'orange': [255, 51, 51],
          'purple': [204, 0, 204], 'yellow': [255, 255, 0], 'violet': [153, 51, 255], 'light_green': [50, 255, 50]}


def get_color_keyboard(makeup_type: str):
    color_keys = list(COLORS.keys())
    color_len = len(COLORS)
    elem_per_row = 4
    rows = int(color_len / elem_per_row)
    kb = [[InlineKeyboardButton("{}".format(color_keys[elem + elem_per_row * row]),
                                callback_data="{}_color:{}".format(makeup_type,
                                                                   color_keys[elem + elem_per_row * row]))
           for elem in range(elem_per_row)] for row in range(rows)]

    kb.append([InlineKeyboardButton(text="⬅️", callback_data=str(bot_events.BACK_CLICK))])
    kb_markup = InlineKeyboardMarkup(kb)
    return kb_markup


def get_image_from_bytearray(image: bytes) -> np.ndarray:
    temp_file = BytesIO(image)
    image = PIL.Image.open(temp_file)
    image = np.array(image)
    return image


def image_to_bytearray(image: np.ndarray):
    temp_file = BytesIO()
    temp_file.name = 'Segmented.png'
    im = PIL.Image.fromarray(image)
    im.save(temp_file, format="png")
    temp_file.seek(0)
    return temp_file
