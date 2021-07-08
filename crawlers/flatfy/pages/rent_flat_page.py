from typing import List
from bs4 import BeautifulSoup

from parsers.flat_parser import FlatParser
from locators.flats_page_locators import FlatsPageLocators as FPLoc
from locators.flat_locators import FlatLocators as FLoc


class FlatsPage:
    def __init__(self, page_soup: BeautifulSoup):
        self.soup = page_soup

    @property
    def flats_list(self) -> List[FlatParser]:
        flat_tags = [tag for tag in self.soup.select(FPLoc.FLAT) if self.check_is_not_ad(tag)]

        return [FlatParser(flat) for flat in flat_tags]

    @staticmethod
    def check_is_not_ad(flat_tag: BeautifulSoup) -> bool:
        if 'realty-block__wrapper--top-nb' in flat_tag.attrs.get('class'):
            return False

        preview = flat_tag.select_one(FLoc.REALTY_PREVIEW)
        if not preview or 'ad_card' in preview.attrs.get('data-event-category'):
            return False

        return True
