from datetime import timedelta, time

import requests
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
        # get actual offer
        self.logger.debug('Handle response')
        soup = BeautifulSoup(response.text, 'html.parser')
        article: Tag = soup.find_all('article')[0]
        href = [child for child in article.children if child.name == 'a'][0]['href']
        link = (self.host + href).replace('/de/', '/en/')
        result = f'Todays new offer: {link}'

        # get prices
        price_string = None
        try:
            price_response = requests.get('https://'+link)
            price_soup = BeautifulSoup(price_response.text, 'html.parser')
            prices = price_soup.find_all('div', class_=['productDetail'])[
                0].find('span', class_=['appendix'])

            new_price = prices.parent.strong.text.strip()
            original_price = prices.text.split()[-1]

            if new_price and original_price:
                price_string = f'\n{new_price} instead of {original_price}'
        except Exception as e:
            self.logger.debug(
                f'Exception while getting prices for \"{result}\"')
            self.logger.debug(e)

        finally:
            self.logger.debug(f'Result is: \"{result}\"')
            return result + (price_string or '')

    def get_inline_keyboard(self):
        return [InlineKeyboardButton(f"Get actual Daily Offer", callback_data=self.job_actual_value)]
