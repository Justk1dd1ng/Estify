import re

from typing import Union, List
from bs4 import BeautifulSoup

from rieltor_ua.locators import URL_GLOBAL
from abstract import FlatPreview, Flat, ImageCrawler, FlatImage
from rieltor_ua.locators.flat_locators import RieltorFlatPreviewLocators, RieltorFlatLocators, \
    RieltorPremiumFlatLocators, RieltorImageLocators
from rieltor_ua.pages.images import RieltorImageCrawler


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
        self.source = URL_GLOBAL
        self.image_crawler = RieltorImageCrawler(self.url)

    @property
    def address(self) -> str:

        link = self.soup.select_one(self.locators.ADRESS)

        return link.text.strip().replace('Сдам квартиру ', '')

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

    @property
    def id(self) -> str:

        return self.url.split(r'/')[-2]

    def get_imgs_list(self) -> List[FlatImage]:

        return [FlatImage(img_bin, self.id) for img_bin in self.image_crawler.get_images_binary()]

    def _get_floors(self) -> Union[List[int], None]:

        properties = self.soup.select(self.locators.AREA)
        for link in properties:
            if 'этаж' in link.text:

                floors_text = link.text
                break
        else:
            return

        try:
            return [int(floor) for floor in re.findall(r'[\d]+', floors_text)]

        except ValueError:
            return


class RielorFlatPremium(RieltorFlat):

    def __init__(self, flat_soup: BeautifulSoup, url: str):

        super().__init__(flat_soup, url)
        self.locators = RieltorPremiumFlatLocators

    @property
    def total_area(self) -> int:

        for param in self._get_params():
            if 'площадь' in param.select_one(self.locators.PARAM_TEXT).text.lower():

                return int(param.select_one(self.locators.PARAM_IMG).text.replace('м2', ''))

    @property
    def total_rooms(self) -> int:

        for param in self._get_params():
            if 'квартира' in param.select_one(self.locators.PARAM_TEXT).text.lower():

                return int(''.join([c for c in param.select_one(self.locators.PARAM_IMG).text if c.isdigit()]))

    def _get_floors(self) -> Union[List[int], None]:

        for param in self._get_params():
            if 'этаж' in param.select_one(self.locators.PARAM_TEXT).text.lower():

                return [int(floor) for floor in param.select_one(self.locators.PARAM_IMG).text.split(r'/')]

    def _get_params(self) -> List[BeautifulSoup]:

        return self.soup.select(self.locators.PARAMS)

