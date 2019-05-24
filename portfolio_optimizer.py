#https://stackoverflow.com/questions/48071949/how-to-use-the-alpha-vantage-api-directly-from-python
#https://www.profitaddaweb.com/2018/07/alpha-vantage-preprocessed-free-apis-in.html
import requests
import alpha_vantage
import json
import pandas as pd
import datetime
import numpy as np
import time
from mpl_finance import candlestick_ohlc
import matplotlib
import matplotlib.dates as mdates
import matplotlib.path as mpath
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib import style
import os
from scipy.optimize import minimize
import pandas_datareader.data as web

def get_stock_time_frame(symbol, start_date, end_date):
    dates=pd.date_range(start_date,end_date)
    df1=pd.DataFrame(index=dates)
    root = '/Users/ruitang/Dropbox/Program/Stock_Analysis'
    day = 'daily_data'
    subdir = os.path.join(root, day,symbol + '.csv')
    df_temp=pd.read_csv(subdir,index_col="date",parse_dates=True,na_values=['nan'])
    df1=df1.join(df_temp,how='inner')
    df1.to_csv('tmp.csv')
    return df1

def get_risk(prices):
    return (prices / prices.shift(1) - 1).dropna().std().values

def get_return(prices):
    return ((prices / prices.shift(1) - 1).dropna().mean() * np.sqrt(250)).values
symbols = ['BA', 'C', 'AAL', 'NFLX']
prices = pd.DataFrame(index=pd.date_range(start_date, end_date))
for symbol in symbols:
    portfolio = web.DataReader(name=symbol, data_source='quandl', start=start_date, end=end_date)
    close = portfolio[['AdjClose']]
    close = close.rename(columns={'AdjClose': symbol})
    prices = prices.join(close)
prices = prices.dropna()
risk_v = get_risk(prices)
return_v = get_return(prices)
fig, ax = plt.subplots()
ax.scatter(x=risk_v, y=return_v, alpha=0.5)
ax.set(title='Return and Risk', xlabel='Risk', ylabel='Return')
for i, symbol in enumerate(symbols):
    ax.annotate(symbol, (risk_v[i], return_v[i]))
plt.show()
