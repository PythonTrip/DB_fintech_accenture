import pandas as pd
from sklearn.linear_model import LinearRegression


LOW = 'low'
MEDIUM = 'medium'
HIGH = 'high'


class Security:
    """Base class for any Tickets: Stocks, Bonds, etc..."""
    def __init__(self, ticket_name, df):
        """
        :param ticket_name: ticket name + exchenge name in some cases
        :param df: pandas dataframe
        """
        self._ticket_name = ticket_name
        self._ticket = df
        assert self._ticket.shape[0] > 0, 'DataFrame for ticket: {0} is empty!!!'.format(ticket_name)

        self._ticket['Date'] = pd.to_datetime(self._ticket['Date'])
        min_dt = self._ticket['Date'].min()
        self._ticket['Days'] = (self._ticket['Date'] - min_dt).dt.days

        self._model = LinearRegression()
        self._model.fit(self._ticket[['Days']], self._ticket['Adj Close'])

        self._max_day = self._ticket['Days'].max()

    def get_expected_price(self, days_after: int) -> float:
        """
        :param days_after: number of days since today until the date we predict price for
        :return: prediction of ticket probable price
        """
        assert isinstance(days_after, int), 'Incorrect days_after dtype!!!'
        if days_after <= 0:
            return 0
        assert days_after <= 360,  'Could not predict for so long time for ticket: {0}!!!'.format(self._ticket_name)

        price = self._model.predict(pd.Series([self._max_day + days_after]).values.reshape(-1, 1))[0]
        return max(price, 0)

    def get_risk_level(self) -> str:
        """
        :return: security risk level ['low', 'medium', 'high']
        """
        coef = self._model.coef_[0]
        coef_abs = abs(coef)
        if coef >= 0.1 or coef_abs <= 0.01:
            return LOW
        elif coef > 0.01 and coef < 0.1:
            return MEDIUM
        return HIGH

    def get_risk_value(self) -> float:
        """
        :return: security relative value
        """
        return self._model.coef_[0]


# examples of usage:

# PATH_TO_TICKETS = '/home/evgeny-kon/Downloads/Telegram Desktop/TICKETS/'
# df1 = pd.read_csv(PATH_TO_TICKETS + 'AFLT.ME' + '.csv')
# aefl = Security('AFLT.ME', df1)
# print(aefl.get_expected_price(90))
# print(aefl.get_risk_level())
#
# df2 = pd.read_csv(PATH_TO_TICKETS + 'AMD' + '.csv')
# amd = Security('AMD', df2)
# print(amd.get_expected_price(90))
# print(amd.get_risk_level())
#
# df3 = pd.read_csv(PATH_TO_TICKETS + 'ROSN.ME' + '.csv')
# rosn = Security('ROSN.ME', df3)
# print(rosn.get_expected_price(90))
# print(rosn.get_risk_level())