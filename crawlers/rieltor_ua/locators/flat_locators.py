from abstract import FlatPreviewLocators, FlatLocators


class RieltorFlatPreviewLocators(FlatPreviewLocators):

    FLAT_LINK = 'div.catalog-item__img a'


class RieltorFlatLocators(FlatLocators):

    ADRESS = 'h1.catalog-view-header__title.ov-title'
    PRICE = 'div.ov-price'
    DISTRICT = f'{ADRESS} a.not-important'
    AREA = 'dl.ov-params-list dd'
    TOTAL_ROOMS = f'{AREA} a'


class RieltorPremiumFlatLocators(RieltorFlatLocators):

    ADRESS = 'div.prem_offer_header_title'
    PRICE = 'div.prem_offer_header_total_price'
    DISTRICT = f'{ADRESS} a.not-important'
    PARAMS = 'div.prem_offer_param'
    PARAM_IMG = f'{PARAMS}_img'
    PARAM_TEXT = f'{PARAMS}_text'






