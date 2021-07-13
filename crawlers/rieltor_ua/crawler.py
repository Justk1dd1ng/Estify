from typing import List, Union

from abstract import Crawler, Driver
from rieltor_ua.locators import URL_PAGE_PLACEHOLDER
from rieltor_ua.pages.flats_list import RieltorsPage
from rieltor_ua.pages.flat import RieltorFlat, RielorFlatPremium


class RieltorDriver(Driver):

    def __init__(self):

        super().__init__()
        self.url_page_placeholder = URL_PAGE_PLACEHOLDER


class RieltorCrawler(Crawler):

    def __init__(self):

        super().__init__()
        self.driver = RieltorDriver()
        self.flats_page: Union[RieltorsPage, None] = None
        self.crawled_flats = []

    def crawl_page(self, page_num: int):

        self.driver.get_page_url(page_num)
        self.driver.get_url(self.driver.url_page_placeholder)

        self.flats_page = RieltorsPage(self.driver.get_soup())
        self.crawl_flats()

    def crawl_flats(self):

        n = 1
        for flat_link in self.flats_page.flats_link_list:
            print(n)
            self.driver.get_url(flat_link)

            flat_soup = self.driver.get_soup()

            # Need to check if ad is premium, cause premium and non-premium markups are different
            if flat_soup.select_one('div.prem_offer_header_title'):
                self.crawled_flats.append(RielorFlatPremium(flat_soup, flat_link))
            else:
                self.crawled_flats.append(RieltorFlat(flat_soup, flat_link))

            n += 1

