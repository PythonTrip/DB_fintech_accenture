from django.shortcuts import render
from deals.models import Deal
from django.http import HttpResponse


def index(request):
    # person_id = request.GET.get("id")

    all_pos = Deal.objects.filter(person_id=1)

    tickers = [x["ticker"] for x in all_pos.values("ticker").distinct()]

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
            "prof": round(prof, 2)
        }

        return stock

    data = {
        "stocks": [calc_g(ticker) for ticker in tickers],
    }

    return render(request, "index.html", data)
