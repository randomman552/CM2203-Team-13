from machine_learning.models import Stock
from machine_learning.api import fetch_stock
from machine_learning.naive_bayes import summarise_by_class, classify, SUMMARIES_STORAGE_PATH

import json
import time


def get_stock(base_path: str, class_label: str, symbol: str) -> Stock:
    try:
        stock = Stock.load(f"{base_path}/{symbol}.json")
        stock.class_val = class_label
        return stock
    except FileNotFoundError:
        new_stock = fetch_stock(symbol)
        new_stock.class_val = class_label
        new_stock.save(f"{base_path}")
        return new_stock


def main():
    base_path = "./data"
    stocks = []

    # All using this website: https://csimarket.com/screening/performance.php?days=ytd&sort=asc&page=1 Picked 40 of
    # the highest performing stocks, and 30 of the lowest performing ones (from year to date). Limited selection of
    # lowest performing stocks, as they start to become positively performing once at a certain point
    test_labels = {
        "good": [
            "GME", "TMST", "XXII", "RFP", "CAR",
            "TDC", "RRD", "VRTV", "TGLS", "ANF",
            "LPX", "MTW", "SALM", "GT", "GPS",
            "WSM", "KNL", "LB", "DDS", "BIG",
            "MDP", "AA", "AMAT", "MBI", "SLM",
            "MRO", "CAL", "UEC", "BCEI", "IVZ",
            "STX", "GCI", "NUE", "ATI", "UFPI",
            "MHK", "CIT", "BTU", "DLX", "SSP"
        ],
        "bad": [
            "SHW", "FTI", "CS", "LSI", "CLW",
            "JD", "FSLR", "PCG", "AGI", "AMD",
            "PKI", "CHWY", "QCOM", "CLX", "NKE",
            "CL", "XLNX", "WMT", "SAIC", "PG",
            "MRK", "NYT", "MKC", "GLT", "COST",
            "NOV", "DVA", "CERN", "EIX", "NFLX"
        ]
    }

    for class_label in test_labels:
        labels = test_labels[class_label]
        for label in labels:
            while True:
                try:
                    stock = get_stock(base_path, class_label, label)
                    stocks.append(stock)
                    print(f"Retrieved data for {stock}")
                    break
                except TimeoutError:
                    print(f"We have been rate limited on request for {label}: Waiting 70 seconds...")
                    time.sleep(70)
                except TypeError:
                    print(f"Data for {label} unavailable")

    summaries = summarise_by_class(stocks)

    for stock in stocks:
        print(stock, end=": ")
        print(classify(summaries, stock))

    with open(SUMMARIES_STORAGE_PATH, "w") as f:
        json.dump(summaries, f, indent=4)


if __name__ == "__main__":
    main()
