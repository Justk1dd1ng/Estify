import re

from typing import Union, List
from bs4 import BeautifulSoup

from rieltor_ua.locators import URL_GLOBAL
from abstract import FlatPreview, Flat
from rieltor_ua.locators.flat_locators import RieltorFlatPreviewLocators, RieltorFlatLocators


class RieltorsFlatPreview(FlatPreview):

    def __init__(self, flat_soup: BeautifulSoup):

        super().__init__(flat_soup)
        self.locators = RieltorFlatPreviewLocators

    @property
    def flat_link(self):

        link = self.soup.select_one(self.locators.FLAT_LINK)
        if not link:

            return None

        return f"{URL_GLOBAL}{link.attrs.get('href')}"


class RieltorFlat(Flat):

    def __init__(self, flat_soup: BeautifulSoup, url: str):

        super().__init__(flat_soup, url)
        self.locators = RieltorFlatLocators

    @property
    def address(self) -> str:

        link = self.soup.select_one(self.locators.ADRESS)

        return link.text.strip().replace('Здам квартиру ', '')

    @property
    def price(self) -> Union[int, float]:

        price_string = self.soup.select_one(self.locators.PRICE).text

        return self.convert_price(price_string)

    @property
    def district(self) -> str:

        link = self.soup.select_one(self.locators.DISTRICT)

        return link.string.replace(' р-н', '')

    @property
    def total_area(self) -> int:

        links = self.soup.select(self.locators.AREA)
        for link in links:
            if 'м²' in link.text:
                area_text = link.text
                break
        else:
            return 0

        try:
            areas = [int(area) for area in re.findall(r'[\d]+', area_text)]

        except ValueError:
            return 0

        return max(areas)

    @property
    def total_rooms(self) -> int:

        text = self.soup.select_one(self.locators.TOTAL_ROOMS).text

        return int(''.join(c for c in text if c.isdigit()))

    @property
    def floor(self) -> int:

        return min(self._get_floors()) if self._get_floors() else 0

    @property
    def building_total_floors(self) -> int:

        return max(self._get_floors()) if self._get_floors() else 0

    def _get_floors(self) -> Union[List[int], None]:

        properties = self.soup.select(self.locators.AREA)
        for link in properties:
            if 'поверх' in link.text:

                floors_text = link.text
                break
        else:
            return

        try:
            return [int(floor) for floor in re.findall(r'[\d]+', floors_text)]

        except ValueError:
            return











