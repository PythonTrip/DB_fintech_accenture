import portfolio as p
import stock as s
import ticket as t
from collections import namedtuple

Atom = namedtuple(
    'Atom',
    [
        'ticket_name',
        'df',
        'volume',
        'buy_price',
        'projected_price',
    ]
)


class Analyzer:
    """
    Class to analyse client portfolio, tickets, profit, etc...
    The main target is to make consistent group of methods for backend
    """

    def __init__(self, atoms: list[Atom]):
        self._atoms = atoms

    # так я представлял тот класс в котором ты будешь использовать
    # какие-то методы, которые тебе будут интересны можно определить в нем и крутить в беке
