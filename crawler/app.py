import sys

from crawlers.rieltor_ua.crawler import RieltorCrawler
from pyvirtualdisplay import Display
from crawlers.utils import validate_aws_credentials
from config_dev import Config
from exceptions import PlatformError
from db.cloud.aws.s3handler.bucket.flats_source import FlatsSource
from db.cloud.aws.s3handler.bucket.bucket import S3Bucket

config = Config()


def run_crawler(cfg: Config):
    if validate_aws_credentials():
        crawler = RieltorCrawler()

        if 'linux' in cfg.platform.lower():
            display = Display(
                size=(1920, 1080)
            )

            display.start()
            crawler.crawl_page(1)
            crawler.upload_data_to_s3()
            display.stop()
        elif 'windows' in cfg.platform.lower():
            crawler.crawl_page(1)
            crawler.upload_data_to_s3()
        else:
            raise PlatformError(config.platform)

    else:
        print('CredError')


def process_s3_data():
    bucket = S3Bucket('flats')
    bucket.process_new_data('rieltor_ua')


if __name__ == '__main__':
    run_crawler(config)
    process_s3_data()