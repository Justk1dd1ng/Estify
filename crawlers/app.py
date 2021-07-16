from rieltor_ua.crawler import RieltorCrawler
from pyvirtualdisplay import Display
from utils import validate_aws_credentials

if validate_aws_credentials():
    crawler = RieltorCrawler()
    display = Display(
        size=(1920, 1080)
    )

    display.start()
    crawler.crawl_page(1)
    crawler.put_csv_df_into_s3()
    crawler.put_images_into_s3()
    display.stop()
else:
    print('CredError')