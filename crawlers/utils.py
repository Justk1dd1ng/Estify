import requests
import re
import boto3

from bs4 import BeautifulSoup

from thirdparty_locators import MinfinLocators as MFLoc
from exceptions import CurrencyError


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


def validate_aws_credentials():
    client = boto3.client('s3')
    try:
        client.list_buckets()
        return True
    except:
        return False
