from django.shortcuts import render
from deals.models import Deal
from django.http import HttpResponse
from intefraces import utils, portfolio
from datetime import datetime, timedelta


def all_stocks(all_pos, tickers):
    def calc_g(ticker):
        ticker_pos = all_pos.filter(ticker=ticker)

        summ = 0
        vol = 0
        for deal in ticker_pos:
            summ += deal.adj * deal.volume
            vol += deal.volume

        prof = (ticker_pos.order_by('-id')[0].adj * vol - summ) / summ * 100
        stock = {
            "ticker": ticker,
            "adj": ticker_pos.order_by('-id')[0].adj,
            "volume": ticker_pos.order_by('-id')[0].volume,
            "sum": ticker_pos.order_by('-id')[0].adj * ticker_pos.order_by(
                '-id')[0].volume,
            "prof": round(prof, 2)
        }

        return stock

    return [calc_g(ticker) for ticker in tickers]


def get_pos_df(tickers):
    df = {}
    for ticker in tickers:
        dataset = utils.Data()
        dataset.download(ticker, datetime.now() - timedelta(31 * 12))
        df.update({ticker: dataset.ticker_data.reset_index()})

    return df


def index(request):
    # person_id = request.GET.get("id")

    all_pos = Deal.objects.filter(person_id=1)

    tickers = [x["ticker"] for x in all_pos.values("ticker").distinct()]

    port = portfolio.Portfolio(get_pos_df(tickers))

    stocks = all_stocks(all_pos, tickers)

    sum_stocks = 0
    exp_price = 0
    exp_stocks = port.get_expected_prices(90)
    for stock in stocks:
        sum_stocks += stock["sum"]
        exp_price += exp_stocks[stock["ticker"]] * stock["volume"] - stock[
            "adj"]

    data = {
        "stocks": stocks,
        "risk": [port.get_risk_level(),
                 port.get_risk_value()],
        "exp": round(exp_price, 2),
        "sum": round(sum_stocks, 2),
    }

    return render(request, "index.html", data)
