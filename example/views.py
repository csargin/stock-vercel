# example/views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages


import yfinance as yf #https://pypi.org/project/yfinance/
import pandas as pd
import numpy as np
import requests
import json
import os

# Create your views here.
# https://theautomatic.net/yahoo_fin-documentation
# https://algotrading101.com/learn/yahoo-finance-api-guide/

def tr_stock(stock):
    if (len(stock)>= 6 ) and (stock[-3:]==".IS"):
        return True
    else:
        return False


def tr_stock_name(stock):
    if tr_stock(stock):
        return stock[:-3]
    else:
        return stock

def home(request):
    ticker_list = tuple(Stock.objects.values_list('ticker', flat = True))
       
    if len(ticker_list)>0:
        try:
            api = ticker_list
        except Exception as e:
            api = "Error"
        return render(request, 'home.html',{'api': api })
    else:
        return render(request, 'home.html',{'api': "" })

def about(request):
    return render(request, "about.html", {})

def generator(request):
    return render(request, "generator.html", {})

def search(request):

    if request.method == 'POST':
        ticker = request.POST['ticker']

        if ticker:

            try:
                try:
                    temp = yf.Ticker(ticker)                
                    api= temp.info 
                    symbol_check_error = api["symbol"]
                    ticker = ticker.upper()
                    
                except:
                    ticker = ticker + ".IS"
                    temp = yf.Ticker(ticker)
                    api= temp.info 
                    symbol_check_error = api["symbol"]
                    ticker = ticker.upper()
    
            except Exception as e:
                api = "Error"
                ticker = "Error"
            
            return render(request, 'search.html',{'api': api, 'ticker': ticker   })

        else:
            return render(request, 'search.html',{'ticker': "Error" })
    else:
        return render(request, 'search.html',{'ticker': "Enter a ticker symbol" })

def add_stock(request):

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added"))
            return redirect('home')
    else:
        return redirect('home')

def delete(request, stock_name):
    item = Stock.objects.filter(ticker = stock_name)
    item.delete()
    messages.success(request, ("Stock has been deleted"))
    return redirect('home')

def analysis(request, stock_name): #https://canvasjs.com/javascript-stockcharts/simple-moving-average-stockchart/
    from datetime import date
    import yahoo_fin.stock_info as si

    try:
        symbol = ""
        #https://tr.tradingview.com/widget/
        if tr_stock(stock_name):
            symbol = "BIST:" + stock_name[:-3]
        elif stock_name in si.tickers_dow():
            # get list of Dow stocks
            symbol = stock_name
        elif stock_name in si.tickers_nasdaq():
            # get list of NASDAQ stocks
            symbol = "NASDAQ:" + stock_name
        elif stock_name in si.tickers_sp500():
            # get list of S&P 500 tickers
            symbol = stock_name
        else:
            symbol = stock_name
    except:
        symbol = stock_name

    try:
        temp = si.get_data(stock_name,  index_as_date = False, interval = "1d")
        api = pd.DataFrame(data=temp).drop(['ticker'], axis=1)

        chart_data = []
        for d,v in api.iterrows():
            dct ={}
            dct["date"] = v.date.strftime("%Y-%m-%d")
            dct["open"] = v.open
            dct["high"] = v.high
            dct["low"] = v.low
            dct["close"] = v.close
            dct["adjclose"] = v.adjclose
            dct["volume"] = v.volume
            if (pd.isnull([v.date.strftime("%Y-%m-%d"), v.open, v.high, v.low, v.close, v.adjclose, v.volume]).any()) == False:
                chart_data.append(dct)

    except Exception as e:
        api = "Error"
    return render(request, 'analysis.html', {'api': api, 'ticker': symbol, 'tr_stock': tr_stock_name(stock_name), 'chart_data': chart_data  })

def calendar(request):
    return render(request, 'calendar.html' , {})

def forecast(request, stock_name):
    # https://canvasjs.com/javascript-stockcharts/line-stockchart-json/
    # https://canvasjs.com/python-charts/python-charts-data-binding/line-chart-data-csv/
    return render(request, 'forecast.html', {'ticker': stock_name, 'tr_stock': tr_stock_name(stock_name)})

def test(request):
    import yahoo_fin.stock_info as si
    temp = si.get_data("MSFT",  index_as_date = False, interval = "1d")
    api = pd.DataFrame(data=temp).drop(['ticker'], axis=1)

    chart_data = []
    for d,v in api.iterrows():
        dct ={}
        dct["date"] = v.date.strftime("%Y-%m-%d")
        dct["open"] = v.open
        dct["high"] = v.high
        dct["low"] = v.low
        dct["close"] = v.close
        dct["adjclose"] = v.adjclose
        dct["volume"] = v.volume
        if (pd.isnull([v.date.strftime("%Y-%m-%d"), v.open, v.high, v.low, v.close, v.adjclose, v.volume]).any()) == False:
            chart_data.append(dct)
    return render(request, 'test.html',{'btc_usd_data': chart_data })
    
