from Finance_Pull import Apigenfetch, Apihistfetch, Apioverfetch
from .models import Stock


def fetch_stock(stock_symbol: str):
    """
    Convenience method to get an instance of a Stock object
    based on data retrieved from the API
    :param stock_symbol: The symbol of the stock
    :return:
    """
    # general = Apigenfetch(stock_symbol)
    # history = Apihistfetch(stock_symbol)
    overview = Apioverfetch(stock_symbol)

    return Stock(overview)
