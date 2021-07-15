from typing import List, Union
from io import BytesIO
from datetime import datetime

import boto3
import pandas as pd

from abstract import Crawler, Driver, FlatImage
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
        self.crawled_imgs: List[FlatImage] = []

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
                flat = RielorFlatPremium(flat_soup, flat_link)
            else:
                flat = RieltorFlat(flat_soup, flat_link)

            self.crawled_flats.append(flat)
            self.crawled_imgs.extend(flat.get_imgs_list())
            flat.image_crawler.driver.chrome.close()

            n += 1

    def put_images_into_s3(self):

        s3 = boto3.client('s3')
        n = 0
        for ix, img in enumerate(self.crawled_imgs):
            n += 1
            s3.put_object(
                Bucket='flatsimages',
                Key=f'rieltor_ua/{img.flat_id}/{ix}.png',
                Body=img.img_binary
            )
            print(n)

    def make_flats_dataframe(self) -> pd.DataFrame:

        data = [
            [
                flat.id,
                flat.address,
                flat.total_rooms,
                flat.total_area,
                flat.district,
                flat.floor,
                flat.building_total_floors,
                flat.url,
                flat.source,
                flat.price,
                flat.timestamp
            ]
            for flat in self.crawled_flats
        ]

        return pd.DataFrame(
            data,
            columns=[
                'id',
                'address',
                'total_rooms',
                'total_area',
                'district',
                'floor',
                'total_floors',
                'url',
                'source',
                'price',
                'timestamp'
            ]
        )

    def put_csv_df_into_s3(self):

        df = self.make_flats_dataframe()
        buffer = BytesIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)

        s3 = boto3.client('s3')
        s3.put_object(
            Bucket='flats',
            Key=f'rieltor_ua/{datetime.utcnow()}.csv',
            Body=buffer
        )

