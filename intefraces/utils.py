# -*- encoding: utf-8 -*-
from datetime import datetime
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
