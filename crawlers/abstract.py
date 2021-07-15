import re
import requests

from typing import Union, List
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from utils import get_minfin_currency_rate


class FlatsListLocators:

    FLAT = None


class FlatPreviewLocators:

    FLAT_LINK = None


class FlatLocators:

    ADRESS = None
    PRICE = None
    DISTRICT = None
    AREA = None


class ImageLocators:

    CONTAINER = None
    LINK = None


class Driver:

    def __init__(self):

        self.url_page_placeholder: Union[None, str] = None
        self.options = Options()
        self.options.headless = True
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.chrome = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)

    def get_url(self, url: str):
        self.chrome.get(url)

    def get_html(self) -> str:

        return self.chrome.page_source

    def get_soup(self) -> BeautifulSoup:

        return BeautifulSoup(self.get_html(), 'html.parser')

    def get_page_url(self, page_num: int) -> str:

        return self.url_page_placeholder.format(page_num)


class Crawler:

    def __init__(self):

        self.driver: Union[None, Driver] = None


class Flat:

    def __init__(self, flat_soup: BeautifulSoup, url: str):

        self.soup = flat_soup
        self.url = url
        self.locators: Union[FlatLocators, None] = None

    @property
    def address(self) -> str:
        return

    @property
    def price(self) -> Union[int, float]:
        return

    @property
    def district(self) -> str:
        return

    @property
    def total_area(self) -> int:
        return

    @property
    def total_rooms(self) -> int:
        return

    @property
    def floor(self) -> int:
        return

    @property
    def building_total_floors(self) -> int:
        return

    @property
    def timestamp(self) -> datetime:

        return datetime.utcnow()

    @staticmethod
    def convert_price(price_string: str):

        price_num = int(''.join([c for c in price_string if c.isdigit()]))
        if '$' in price_string:

            return round(price_num * get_minfin_currency_rate('dollar'))

        elif '€' in price_string:

            return round(price_num * get_minfin_currency_rate('euro'))

        return price_num


class FlatPreview:

    def __init__(self, flat_soup: BeautifulSoup):

        self.soup = flat_soup
        self.locators: Union[FlatPreviewLocators, None] = None

    @staticmethod
    def convert_price(price_string: str):

        price_num = int(''.join([c for c in price_string if c.isdigit()]))
        if '$' in price_string:

            return round(price_num * get_minfin_currency_rate('dollar'))

        elif '€' in price_string:

            return round(price_num * get_minfin_currency_rate('euro'))

        return price_num

    @property
    def flat_link(self):
        pass


class FlatsPage:

    def __init__(self, page_soup: BeautifulSoup):

        self.soup = page_soup
        self.locators: Union[FlatsListLocators, None] = None
        self.flat_preview_parser = FlatPreview

    @property
    def flats_preview_list(self) -> List[FlatPreview]:
        return [self.flat_preview_parser(tag) for tag in self.soup.select(self.locators.FLAT)]


class ImageDriver(Driver):

    def __init__(self):
        super().__init__()


class ImageCrawler:

    def __init__(self, url: str):

        self.url = url
        self.locators = ImageLocators
        self.driver: Union[None, ImageDriver] = None


class FlatImage:

    def __init__(self, img_binary: bytes, flat_id: str):

        self.img_binary = img_binary
        self.flat_id = flat_id

