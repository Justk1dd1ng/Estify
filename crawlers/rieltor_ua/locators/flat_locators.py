from abstract import FlatPreviewLocators, FlatLocators


class RieltorFlatPreviewLocators(FlatPreviewLocators):

    FLAT_LINK = 'div.catalog-item__img a'


class RieltorFlatLocators(FlatLocators):

    ADRESS = 'h1.catalog-view-header__title.ov-title'
    PRICE = 'div.ov-price'
    DISTRICT = f'{ADRESS} a.not-important'
    AREA = 'dl.ov-params-list dd'
    TOTAL_ROOMS = f'{AREA} a'





