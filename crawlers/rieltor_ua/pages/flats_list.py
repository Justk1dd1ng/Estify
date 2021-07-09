from typing import List
from bs4 import BeautifulSoup

from rieltor_ua.locators.flats_list_locators import RieltorFlatsListLocators
from rieltor_ua.pages.flat import RieltorsFlatPreview
from abstract import FlatsPage


class RieltorsPage(FlatsPage):

    def __init__(self, page_soup: BeautifulSoup):

        super().__init__(page_soup)
        self.locators = RieltorFlatsListLocators
        self.flat_preview_parser = RieltorsFlatPreview

    @property
    def flats_link_list(self) -> List[str]:

        return [flat.flat_link for flat in self.flats_preview_list]







