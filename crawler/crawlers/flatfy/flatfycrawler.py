from typing import Union

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from pages.rent_flat_page import FlatsPage


class FlatfyDriver:

    URL_PAGE_PLACEHOLDER = 'https://flatfy.ua/uk/search?geo_id=1&page={}&section_id=2'

    def __init__(self, page: int):

        self.url = self.switch_page(page)
        self.options = Options()
        self.options.headless = True
        self.chrome = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        self.chrome.set_window_size(1920, 1080)
        self.get_url()

    def get_url(self):
        self.chrome.get(self.url)

    def get_html(self) -> str:

        return self.chrome.page_source

    def get_soup(self) -> BeautifulSoup:

        return BeautifulSoup(self.get_html(), 'html.parser')

    def switch_page(self, page: int) -> str:

        return self.URL_PAGE_PLACEHOLDER.format(page)


class FlatfyCrawler:
    def __init__(self):

        self.driver: Union[None, FlatfyDriver] = None

    def get_page(self, page_num: int):
        self.driver = FlatfyDriver(page_num)

    @property
    def soup(self):

        return self.driver.get_soup()

    @property
    def page(self):

        return FlatsPage(self.driver.get_soup())

