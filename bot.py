import logging.config
import os

from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup
from telegramtaskbot import TelegramTaskBot

from Task.DigitecTask import DigitecTask

logging.config.fileConfig('logging.conf')
load_dotenv()


class DigitecTaskBot(TelegramTaskBot):
    def start(self, update, context):
        self.TASKS[0].handle_start(context=context, chat_id=update.effective_chat.id, with_message=False)
        reply_markup = InlineKeyboardMarkup(self.build_menu(self.default_button_list, n_cols=1))
        context.bot.send_message(chat_id=update.effective_chat.id, text=os.getenv('START_MESSAGE'),
                                 reply_markup=reply_markup)


bot = DigitecTaskBot([DigitecTask])
bot.run()
logging.info('Bot running!')
