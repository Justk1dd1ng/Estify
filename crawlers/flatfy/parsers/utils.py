import requests
import re

from bs4 import BeautifulSoup

from locators.third_party_locators import MinfinLocators as MFLoc
from parsers.exceptions import CurrencyError


def get_minfin_currency_rate(currency: str) -> float:
    url = MFLoc.URL
    data_title = {
        'dollar': 'Доллар',
        'euro': 'Евро'
    }.get(currency)

    if not data_title:
        raise CurrencyError(currency)

    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    tag = [tag for tag in soup.select(MFLoc.EXCHANGE_RATE) if tag.attrs.get('data-title') == data_title][0]

    exchange_rate = float(re.findall(r'[0-9\.]+', tag.text)[0])

    return round(exchange_rate, 2)



