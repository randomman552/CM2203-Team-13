import json


# TODO: Check which attributes would be best to compare
class Stock:
    """
    Class that wraps around the dicts given to us by the API and represents a stock.
    Contains a number of convenience getters to make the underlying data easier to deal with.
    """

    def __init__(self, overview: dict, class_: str = "unknown"):
        if len(overview) == 0:
            raise TypeError("Overview dict cannot be empty")

        if "class" in overview:
            self.overview = overview.get("overview")
            self.__class = overview.get("class")
        else:
            self.overview = overview
            self.__class = class_

    def as_tuple(self) -> tuple:
        """
        Get this stock as a tuple for use in machine learning functions.
        :return: Tuple containing information useful to machine learning.
        """
        return tuple([
            self.rolling_average_percent_inc,
            self.earnings_per_share,
            self.revenue_growth_yoy,
            self.profit_margin
        ])

    def save(self, base_path: str = "./data"):
        combined = {
            "overview": self.overview,
            "class": self.class_val
        }

        with open(f"{base_path}/{self.symbol}.json", "w+") as f:
            json.dump(combined, f, indent=4)

    @staticmethod
    def load(path: str):
        """
        Create new Stock object with json at the given file path.
        """
        with open(path, "r") as f:
            data = json.load(f)
        return Stock(data)

    @property
    def symbol(self) -> str:
        return self.overview.get("Symbol")

    @property
    def description(self) -> str:
        return self.overview.get("Description")

    @property
    def name(self) -> str:
        return self.overview.get("Name")

    @property
    def industry(self) -> str:
        return self.overview.get("Industry")

    @property
    def rolling_avg50(self) -> float:
        return float(self.overview.get("50DayMovingAverage"))

    @property
    def rolling_avg200(self) -> float:
        return float(self.overview.get("200DayMovingAverage"))

    @property
    def rolling_average_percent_inc(self) -> float:
        try:
            return self.rolling_avg50 / self.rolling_avg200
        except ZeroDivisionError:
            return 0

    @property
    def earnings_per_share(self) -> float:
        return float(self.overview.get("EPS", 0))

    @property
    def revenue_growth_yoy(self) -> float:
        return float(self.overview.get("QuarterlyRevenueGrowthYOY"))

    @property
    def profit_margin(self) -> float:
        return float(self.overview.get("ProfitMargin"))

    @property
    def class_val(self):
        return self.__class

    @class_val.setter
    def class_val(self, val):
        self.__class = val

    def __repr__(self):
        return f"Stock: {self.symbol}"
