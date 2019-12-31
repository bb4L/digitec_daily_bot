from datetime import timedelta, time

from bs4 import BeautifulSoup, Tag
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
        self.logger.debug('Handle response')
        soup = BeautifulSoup(response.text, 'html.parser')
        article: Tag = soup.find_all('article')[0]
        href = [child for child in article.children if child.name == 'a'][0]['href']
        link = (self.host + href).replace('/de/', '/en/')
        result = f'Todays new offer: {link}'
        self.logger.debug(f'Result is: \"{result}\"')
        return result

    def get_inline_keyboard(self):
        return [InlineKeyboardButton(f"Get actual Daily Offer", callback_data=self.job_actual_value)]
