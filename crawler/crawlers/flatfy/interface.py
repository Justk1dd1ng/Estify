from flatfycrawler import FlatfyCrawler
from pages.rent_flat_page import FlatsPage


def scrape_page():
    crawler = FlatfyCrawler('https://flatfy.ua/uk/search?geo_id=1&page=1&section_id=2')
    soup = crawler.get_soup()
    flats = FlatsPage(soup)

    return flats


crawler = FlatfyCrawler()
origins = []
for page in range(50):
    print(page)
    crawler.get_page(page)
    origins.extend([flat.origin_site for flat in crawler.page.flats_preview_list])
