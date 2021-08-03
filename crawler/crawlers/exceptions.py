class CurrencyError(Exception):

    def __init__(self, currency: str):

        self.currency = currency
        self.message = f'Invalid currency name: "{currency}". Only "dollar" and "euro" are supported.'
        super().__init__(self.message)
