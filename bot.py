import logging

from telegramtaskbot import TelegramTaskBot

from Task.DigitecTask import DigitecTask


class DigitecTaskBot(TelegramTaskBot):
    def start(self, update, context):
        self.TASKS[0].start([], update, context)


bot = DigitecTaskBot([DigitecTask])

bot.run()
logging.info('Bot running!')
