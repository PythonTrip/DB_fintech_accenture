import pandas as pd
import intefraces.ticket as t
from typing import Dict


class Portfolio:
    """
    Base class for stocks portfolio analytics
    Main target is to summarize individual tickets
    """

    def __init__(self, tickets_dict: Dict[str, pd.core.frame.DataFrame]):
        """
        :param tickets_dict: dict of ticket names associated with pandas dataframes such ticket
        """
        assert tickets_dict, "Portfolio can't be empty"

        self._tickets = {
            name: t.Security(name, df)
            for name, df in tickets_dict.items()
        }

    def update_portfolio(self, ticket_name: str, df: pd.core.frame.DataFrame):
        """Method to add new or update ticket in portfolio"""
        self._tickets[ticket_name] = t.Security(ticket_name, df)

    def get_expected_prices(self, days_after: int) -> Dict[str, int]:
        """
        :param days_after: number of days since today until the date we predict prices for
        :return: list of expected predicted prices after days_after days for given tickets
        """
        assert 0 <= days_after <= 360, 'Prediction period should be less than 360 days'
        self._prices = {}
        for name, ticket in self._tickets.items():
            self._prices[name] = ticket.get_expected_price(days_after)

        return self._prices

    def get_risk_level(self) -> str:
        """
        :return: average portfolio risk level
        """
        weights = {t.LOW: 1, t.MEDIUM: 2, t.HIGH: 3}
        total = sum(
            weights[risk]
            for risk in [
                ticket.get_risk_level()
                for ticket
                in self._tickets.values()
            ]
        )
        risk = total / len(self._tickets)
        if risk <= 1.5:  # Вариативно
            return t.LOW
        elif risk >= 2.25:  # Вариативно
            return t.HIGH
        return t.MEDIUM

    def get_risk_value(self) -> float:
        """
        Вот здесь можно придумать какую-то интегральную метрику рискованности
        портфеля на основе рисков по каждому активу, но это неточно
        """
        return sum(
            ticket.get_risk_value() for ticket in self._tickets.values())

# examples of usage:

# PATH_TO_TICKETS = '/home/evgeny-kon/Downloads/Telegram Desktop/TICKETS/'
# df1 = pd.read_csv(PATH_TO_TICKETS + 'AFLT.ME' + '.csv')
# df2 = pd.read_csv(PATH_TO_TICKETS + 'AMD' + '.csv')
#
# tickets = {'AFLT.ME': df1, 'AMD': df2}
# port = Portfolio(tickets)
#
# print(port.get_expected_prices(90))
# print(port.get_risk_level())
# print(port.get_risk_value())
