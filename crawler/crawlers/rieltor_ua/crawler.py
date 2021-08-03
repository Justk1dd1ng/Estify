from datetime import datetime
from io import BytesIO
from typing import List, Union, Tuple

import boto3
import pandas as pd

from crawlers.abstract import Crawler, Driver, FlatImage
from db.cloud.aws.s3handler.bucket.flats_source import FlatsSource
from crawlers.rieltor_ua.locators import URL_PAGE_PLACEHOLDER
from crawlers.rieltor_ua.pages.flat import RieltorFlat, RielorFlatPremium
from crawlers.rieltor_ua.pages.flats_list import RieltorsPage
from db.cloud.aws.s3handler.utils import put_df_into_s3_as_csv


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
        cached_ids = self.get_cached_last_flat_ids()

        n = 0
        for flat_link in self.flats_page.flats_link_list:
            print(n)
            self.driver.get_url(flat_link)

            flat_soup = self.driver.get_soup()

            # Need to check if ad is premium, cause premium and non-premium markups are different
            if flat_soup.select_one('div.prem_offer_header_title'):
                flat = RielorFlatPremium(flat_soup, flat_link)
            else:
                flat = RieltorFlat(flat_soup, flat_link)

            # Checking if flat is already in database so there's no need to crawl it again
            if int(flat.id) in cached_ids:
                break

            self.crawled_flats.append(flat)
            self.crawled_imgs.extend(flat.get_imgs_list())
            flat.image_crawler.driver.chrome.close()

            n += 1
        self.driver.chrome.quit()
        print(f'Succesfully crawled {n} new flats from "rieltor_ua"')

    @staticmethod
    def get_cached_last_flat_ids() -> Tuple[int]:
        flats_source = FlatsSource('rieltor_ua')
        last_csv = flats_source.get_last_csv_objects()
        df = flats_source.get_dataframe_from_csv(last_csv.name)

        return tuple(df['id'])

    def put_images_into_s3(self):

        s3 = boto3.client('s3')
        for img in self.crawled_imgs:
            s3.put_object(
                Bucket='flatsimages',
                Key=f'rieltor_ua/{img.flat_id}/{img.image_id}.png',
                Body=img.img_binary
            )
        print(f'Succesfully uploaded {len(self.crawled_imgs)} images')

    @staticmethod
    def make_flats_dataframe_from_list(data: List[List]) -> pd.DataFrame:

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

    def upload_data_to_s3(self):
        data_for_csv = []

        # TODO: Consider providing more safe and beautiful way to stop the process when adding new crawlers
        if not self.crawled_flats:
            print('No new flats found at "rieltor.ua"')
            raise SystemExit
        for flat in self.crawled_flats:
            data_for_csv.append(
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
            )

        df = self.make_flats_dataframe_from_list(data_for_csv)
        put_df_into_s3_as_csv(
            df=df,
            bucket_name='flats',
            key_name=f'rieltor_ua/{datetime.utcnow()}.csv'
        )
        self.put_images_into_s3()
