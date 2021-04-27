from Finance_Pull import Apigenfetch, Apihistfetch, Apioverfetch
from .models import Stock


def fetch_stock(stock_name: str):
    # general = Apigenfetch(stock_name)
    # history = Apihistfetch(stock_name)
    overview = Apioverfetch(stock_name)

    if "You have exceeded the rate limit" in overview.get("message", ""):
        raise TimeoutError("Exceeded rate limit")
    else:
        return Stock(overview)
