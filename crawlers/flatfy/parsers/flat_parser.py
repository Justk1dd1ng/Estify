import re
import numpy as np

from typing import Union
from bs4 import BeautifulSoup

from locators.flat_locators import FlatLocators as FLoc
from utils import get_minfin_currency_rate


class FlatParser:
    def __init__(self, flat_soup: BeautifulSoup):
        self.soup = flat_soup

    @property
    def price(self) -> Union[int, float]:
        link = self.soup.select_one(FLoc.PRICE_LOCATOR)
        if not link:
            return np.nan

        price_string = link.string

        return self.convert_price(price_string)

    @property
    def address(self) -> Union[str, float]:
        link = self.soup.select_one(FLoc.ADDRESS_LOCATOR)

        if not link:
            return np.nan

        return link.text

    @property
    def total_rooms(self) -> Union[int, float]:
        link = self.soup.select_one(FLoc.ROOM_NUMBER_LOCATOR)
        num_string = re.findall(r'[\d]', link.string)
        if not num_string:
            return np.nan

        return int(num_string[0])

    @property
    def slide_button(self):
        link = self.soup.select_one(FLoc.SLIDE_BUTTON)

        return link

    @property
    def origin_site(self) -> str:
        link = self.soup.select_one(FLoc.ORIGIN_SITE)

        return link.text

    @staticmethod
    def convert_price(price_string: str):
        price_num = int(''.join([c for c in price_string if c.isdigit()]))
        if '$' in price_string:
            return round(price_num * get_minfin_currency_rate('dollar'))

        elif '€' in price_string:
            return round(price_num * get_minfin_currency_rate('euro'))

        return price_num


