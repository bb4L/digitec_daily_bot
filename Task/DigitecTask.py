from datetime import timedelta, time

from bs4 import BeautifulSoup
from requests import Response
from telegram import InlineKeyboardButton
from telegramtaskbot import UrlTask


class DigitecTask(UrlTask):
    repeat_time = timedelta(days=1)
    first_time = time(hour=0, minute=30)
    job_name = 'digitec_daily'
    url = 'https://www.digitec.ch/de/LiveShopping/81'
    host = 'www.digitec.ch'
    filename = 'digitec_subscriptions'

    def handle_response(self, response: Response):
        soup = BeautifulSoup(response.text, 'html.parser')
        all_a = soup.find_all('a', class_='ZZ7j ZZ7l', href=True)
        href = all_a[0]['href']
        link = (self.host + href).replace('/de/', '/en/')
        return f'Todays new offer: {link}'

    def get_inline_keyboard(self):
        return [InlineKeyboardButton(f"Get actual Daily Offer", callback_data=self.job_actual_value)]
