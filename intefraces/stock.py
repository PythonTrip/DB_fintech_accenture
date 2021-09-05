from pathlib import Path
import pandas as pd
from typing import List


DIR_TO_FILES = '/home/evgeny-kon/Downloads/Telegram Desktop/TICKETS/'
STOCKS_NAMES = [
    'AFLT.ME',
    'AMD',
    'MTSS.ME',
    'ROSN.ME',
    'SBER.ME',
    'VTBR.ME',
]


class Stock:
    """
    Upload stocks to back end memory
    """
    def __init__(self, names: List[str], dir: str):
        self._dframes = {}
        for name in names:
            file_name = dir + name + '.csv'
            assert Path(file_name).exists(), 'File by path {0} not found. Cant douwnload dataframe'.format({file_name})

            self._dframes[name] = pd.read_csv(file_name)

    @staticmethod
    def create(names, dir):
        return Stock(names, dir)


STOCK = Stock.create(STOCKS_NAMES, DIR_TO_FILES)
