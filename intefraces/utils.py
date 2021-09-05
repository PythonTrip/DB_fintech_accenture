# -*- encoding: utf-8 -*-
from datetime import datetime
from pycbrf.toolbox import ExchangeRates
import pandas as pd
import yfinance as yf
import os


pd.set_option('display.max_columns', None)


def get_now():
    return datetime.now().strftime("%Y-%m-%d")


def save_db(name, db: pd.DataFrame):
    with open(name, "w", encoding='utf8') as f:
        db.to_csv(name)


class Data:
    def __init__(self):
        self.ticker_name = ""
        self.ticker = None
        self.ticker_data: pd.DataFrame = pd.DataFrame()

    def download(self, ticker_name, from_, end=datetime.now(), update=False):
        self.ticker_name = ticker_name
        self.ticker = yf.Ticker(f"{ticker_name}")

        if not update and f"{ticker_name}.csv" in os.listdir("datasets"):
            self.ticker_data = pd.read_csv(f"datasets/{ticker_name}.csv",
                                           index_col="Date")
        else:
            self.ticker_data = yf.download(self.ticker.info['symbol'], from_,
                                           end
                                           ).loc[:, ["Adj Close", "Volume"]]
            self.save_data()

    def save_data(self):
        self.ticker_data.to_csv(f"datasets/{self.ticker_name}.csv")

    @property
    def profitability(self) -> pd.DataFrame:
        if self.ticker_data is None:
            raise Exception("Empty data")
        else:
            return self.ticker_data["Adj Close"] / self.ticker_data[
                "Adj Close"].shift(1) - 1


class Currency:
    def __init__(self):
        self.translate = {
            "USD": 1,
            "EUR": self.get_currency("USD") / self.get_currency("EUR"),
            "RUB": 1 / self.get_currency("USD"),
        }

    @staticmethod
    def get_currency(name="USD", _time=None):
        rates = ExchangeRates(_time if _time is not None else get_now())
        return rates[name].value

    def update_courses(self, _time):
        self.translate = {
            "USD": 1,
            "EUR": self.get_currency("USD", _time) / self.get_currency("EUR",
                                                                       _time),
            "RUB": 1 / self.get_currency("USD", _time),
        }
