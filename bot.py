import logging.config

from telegramtaskbot import TelegramTaskBot

from Task.DigitecTask import DigitecTask

logging.config.fileConfig('logging.conf')


class DigitecTaskBot(TelegramTaskBot):
    def start(self, update, context):
        self.TASKS[0].start_command(update, context)


bot = DigitecTaskBot([DigitecTask])
bot.run()
logging.info('Bot running!')
