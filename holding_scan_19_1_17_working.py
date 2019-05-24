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
        day = 'daily_data'
        subdir = os.path.join(root, day,symbol + '.csv')
        print(subdir)
        data.to_csv(subdir, index=False)
        print(symbol,"finish")
        return data

if __name__ == "__main__":
    sizeoption = 'full'
    API_URL = "https://www.alphavantage.co/query"
    symbolg1 = ['TSLA','BABA','XLNX','NVDA','XBI']
    symbolg2 = ['QQQ','JD','MA','MTN','OLED']
    symbolg3 = ['PYPL','SFIX','EA','GOOGL','MU']
    for symbol in symbolg1:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolg2:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolg3:
        stock_daily=get_stock_daily(symbol,sizeoption)

