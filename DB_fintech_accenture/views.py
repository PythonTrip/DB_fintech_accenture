from django.shortcuts import render, redirect
from deals.models import Deal
from django.http import HttpResponse
from intefraces import utils, portfolio
from datetime import datetime, timedelta
import pandas as pd


def all_stocks(all_pos, tickers):
    stock = []
    portf = {}
    for ticker in tickers:
        ticker_pos = all_pos.filter(ticker=ticker)

        summ = 0
        vol = 0

        for deal in ticker_pos:
            summ += deal.adj * deal.volume
            vol += deal.volume
            if not deal.type in portf:
                portf.update({deal.type: deal.volume})
            else:
                portf[deal.type] += deal.volume

        prof = (ticker_pos.order_by('-id')[0].adj * vol - summ) / summ * 100
        stock.append({
            "ticker": ticker,
            "adj": ticker_pos.order_by('-id')[0].adj,
            "volume": vol,
            "sum": ticker_pos.order_by('-id')[0].adj * ticker_pos.order_by(
                '-id')[0].volume,
            "prof": round(prof, 2)
        })

    portf = pd.DataFrame({"Vol": portf.values()}, index=portf.keys())

    portf = portf["Vol"] / portf["Vol"].sum() * 100

    portf = {
        "labels": list(portf.index),
        "values": list(map(round, portf.values))
    }

    return stock, portf


def get_pos_df(tickers):
    df = {}
    for ticker in tickers:
        dataset = utils.Data()
        dataset.download(ticker, datetime.now() - timedelta(days=31 * 12))
        df.update({ticker: dataset.ticker_data.reset_index()})

    return df


def index(request):
    # person_id = request.GET.get("id")

    all_pos = Deal.objects.filter(person_id=1)

    tickers = [x["ticker"] for x in all_pos.values("ticker").distinct()]

    port = portfolio.Portfolio(get_pos_df(tickers))

    stocks, portf = all_stocks(all_pos, tickers)

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
                 port.get_risk_value() * 44.4],
        "exp": round(exp_price, 2),
        "sum": round(sum_stocks, 2),
        "portf": portf  # portf
    }

    return render(request, "index.html", data)


def add_new(request):
    ticker = request.GET.get("ticker")
    vol = request.GET.get("vol")

    new_data = utils.Data()
    new_data.download(ticker, datetime.now() - timedelta(days=31 * 12),
                      update=True)

    print(new_data.ticker_data.iloc[-1])
    redirect("/")