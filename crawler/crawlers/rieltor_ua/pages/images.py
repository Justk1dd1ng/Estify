from typing import List

import requests

from crawlers.abstract import ImageCrawler, ImageDriver
from crawlers.rieltor_ua.locators.flat_locators import RieltorImageLocators


class RieltorImageDriver(ImageDriver):

    def __init__(self):
        super().__init__()


class RieltorImageCrawler(ImageCrawler):

    def __init__(self, url: str):

        super().__init__(url)
        self.locators = RieltorImageLocators
        self.driver = RieltorImageDriver()

    def get_links(self) -> List[str]:

        self.driver.get_url(self.url)
        soup = self.driver.get_soup()

        return [tag.attrs.get('href') for tag in soup.select(self.locators.LINK)]

    def get_images_binary(self) -> List:

        images = []

        for link in self.get_links():
            img_binary = requests.get(link).content
            images.append(img_binary)

        return images
