import logging
import os

from telegram import Bot, Update, Message

logger = logging.getLogger(os.path.basename(__file__))


class BotUtils:
    def __init__(self, config, auth_chat_ids, bot: Bot):
        # Constructor
        self.config = config
        self.auth_chat_ids = auth_chat_ids
        self.bot = bot

    @staticmethod
    def check_last_and_delete(_, context, message):
        if "last_message" in context.user_data and message is not None:
            context.user_data["last_message"].delete()
            context.user_data["last_message"] = message
        elif "last_message" in context.user_data and message is None:
            context.user_data["last_message"].delete()
            del context.user_data["last_message"]
        elif "last_message" not in context.user_data and message is not None:
            context.user_data["last_message"] = message
        else:
            pass  # message not present or not passed

    def init_user(self, chat_id, username):
        if chat_id not in self.auth_chat_ids:
            self.auth_chat_ids[chat_id] = dict()
            self.auth_chat_ids[chat_id]["username"] = username
            self.auth_chat_ids[chat_id]["active"] = True
            self.auth_chat_ids[chat_id]["makeup"] = dict()
            self.auth_chat_ids[chat_id]["makeup"]['hair-intensity'] = 0.0
            self.auth_chat_ids[chat_id]["makeup"]['hair-color'] = 'blue'
            self.auth_chat_ids[chat_id]["makeup"]['lip-intensity'] = 0.0
            self.auth_chat_ids[chat_id]["makeup"]['lip-color'] = 'blue'


    def log_admin(self, msg, update: Update, context):
        def is_admin(username):
            return username == self.config["admin"]

        if not is_admin(update.effective_user.username):
            for k1, v1 in self.auth_chat_ids.items():
                if v1["username"] == self.config["admin"]:
                    context.bot.send_message(k1, text=msg)
