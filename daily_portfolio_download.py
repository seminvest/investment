#https://stackoverflow.com/questions/48071949/how-to-use-the-alpha-vantage-api-directly-from-python
#https://www.profitaddaweb.com/2018/07/alpha-vantage-preprocessed-free-apis-in.html
#1/19/2019, download latest stock pricing of my watchlist
# total 75 equity, take 15 minutes to run
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
import pandas_datareader.data as web

def get_stock_daily(symbol,sizeoption):
        data = { "function": "TIME_SERIES_DAILY_ADJUSTED", 
        "symbol": symbol,
        "outputsize" : sizeoption,       
        "datatype": "json", 
        "apikey": "AXTFJ8VGFWQ1PWZD" } 
        response = requests.get(API_URL, data) 
        data = response.json()
        print(symbol,"start")
        data=data['Time Series (Daily)'];
        df=pd.DataFrame(columns=['date','open','high','low','close','adjusted close','volume']) 
        for d,p in data.items():
            date=datetime.datetime.strptime(d,'%Y-%m-%d')
            data_row=[date,float(p['1. open']),float(p['2. high']),float(p['3. low']),float(p['4. close']), float(p['5. adjusted close']), int(p['6. volume'])]
            df.loc[-1,:]=data_row
            df.index=df.index+1
        data=df.sort_values('date')
        root = '/Users/ruitang/Dropbox/Program/Stock_Analysis'
        day = 'portfolio_data'
        subdir = os.path.join(root, day,symbol + '.csv')
        print(subdir)
        data.to_csv(subdir, index=False)
        print(symbol,"finish")
        return data

if __name__ == "__main__":
    sizeoption = 'full'
    API_URL = "https://www.alphavantage.co/query"
    #SaaS big names
    symbolg1 = ['NEWR','HUBS','TSLA','NVDA','CBLK']
    #SaaS watch list
    symbolg2 = ['XLNX','JD','BILI','GOOGL','MA'] 
    #MAGA,FANG 
    symbolg3 = ['RDFN','STNE','AMZN','AAPL','BABA'] 
    # payment stocks
    for symbol in symbolg1:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolg2:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolg3:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    