import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime, csv, os, urllib, re;
from pandas_datareader.data import Options
start = datetime.datetime(2010,12,31)
end = datetime.date.today()
current_stock = web.DataReader('TRIP', "yahoo", start, end)
current_stock["200d"]=pd.rolling_mean(current_stock['Adj Close'], 200)
current_stock["50d"]=pd.rolling_mean(current_stock['Adj Close'], 50)
current_stock["20d"]=pd.rolling_mean(current_stock['Adj Close'], 20)
current_stock["5d"]=pd.rolling_mean(current_stock['Adj Close'], 5)
data = current_stock[['Adj Close','200d','50d','20d','5d']]
data['Long Term'] = 'hold'
data['Long Term'][(data['50d'] > data['200d']) & (data['200d'] < data['Adj Close'])] = 'buy'
data['Long Term'][(data['50d'] < data['200d']) & (data['200d'] > data['Adj Close'])] = 'sell'
data['Medium Term'] = 'hold'
data['Medium Term'][(data['20d'] > data['50d']) & (data['50d'] < data['Adj Close'])] = 'buy'
data['Medium Term'][(data['20d'] < data['50d']) & (data['50d'] > data['Adj Close'])] = 'sell'
data['Short Term'] = 'hold'
data['Short Term'][(data['5d'] > data['20d']) & (data['20d'] < data['Adj Close'])] = 'buy'
data['Short Term'][(data['5d'] < data['20d']) & (data['20d'] > data['Adj Close'])] = 'sell'

data.to_csv('TRIP.csv')
current_stock.to_csv('AMZN.csv')