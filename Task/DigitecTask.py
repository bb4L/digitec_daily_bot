import logging
import time as timer
from datetime import timedelta, time
from typing import List

import requests
import telegram
from bs4 import BeautifulSoup
from telegram.ext import JobQueue
from telegramtaskbot import Task


class DigitecTask(Task):
    repeat_time = timedelta(days=1)
    first_time = time(hour=0, minute=30)

    job_name = 'digitec_daily'
    job_start_name = 'start_' + job_name
    job_stop_name = 'stop_' + job_name
    url = 'https://www.digitec.ch/de/LiveShopping/81'
    host = 'www.digitec.ch'
    filename = 'digitec_subscriptions'

    def __init__(self, job_queue: JobQueue):
        self._start([], job_queue, 'General Digitec Task')

    def callback(self, context: telegram.ext.CallbackContext):
        logging.info(f'Run {self.job_name}')
        count = 0
        users = self.load_users()
        response = requests.get(self.url)
        if response.status_code != 200:
            while response.status_code != 200:
                timer.sleep(2)
                resp = requests.get(self.url)
                count += 1
                response = resp
        logging.info(f'Digitec tried for {count} times')
        soup = BeautifulSoup(response.text, 'html.parser')
        all_a = soup.find_all('a', class_='ZZ7j ZZ7l', href=True)
        href = all_a[0]['href']
        link = (self.host + href).replace('/de/', '/en/')
        logging.info(f'Notifying {len(users)} users')
        for user in users:
            context.bot.send_message(chat_id=user, text=f'Todays new offer: {link}', disable_notification=True)

    def start(self, jobs: List[telegram.ext.Job], update: telegram.Update, context: telegram.ext.CallbackContext):
        self.save_user(update.callback_query.message.chat_id)
        logging.info(f'User {update.callback_query.message.chat_id} subscribed')

    def stop(self, jobs: List[telegram.ext.Job], update: telegram.Update, context: telegram.ext.CallbackContext):
        users = self.load_users()
        users.remove(update.callback_query.message.chat_id)
        self.save_to_json(users)
        logging.info(f'User {update.callback_query.message.chat_id} unsubscribed')
        context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                 text=f'You sucesfully unsubscribed')

    def get_inline_keyboard(self):
        return [
            # InlineKeyboardButton(f"Start subscription for daily updates", callback_data=self.job_start_name),
            # InlineKeyboardButton(f"Stop  subscription for daily update", callback_data=self.job_stop_name),
        ]
