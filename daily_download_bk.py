#https://stackoverflow.com/questions/48071949/how-to-use-the-alpha-vantage-api-directly-from-python
#https://www.profitaddaweb.com/2018/07/alpha-vantage-preprocessed-free-apis-in.html
#1/19/2019, download latest stock pricing of my watchlist
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
    symbolg1 = ['CRM','NOW','WDAY','AYX','HUBS']
    symbolg2 = ['TWLO','DOCU','ADBE','OKTA','NEWR']
    symbolg3 = ['INTU','PLAN','DBX','ZS','ZEN']
    symbolge = ['SMAR','COUP','APPF','ZUO','TENB']   
    symbolg4 = ['AVGO','AMD','ANSS','SNPS','CDNS']  
    symbolg5 = ['MSFT','TWTR','ATVI','ADSK','WDC'] 
    symbolg6 = ['V','PYPL','AXP','DFS','SQ'] 
    symbolg7 = ['CME','TRIP','NFLX','DIS','COST'] 
    symbolg8 = ['MORN','NTES','ILMN','ISRG','HD'] 
    symbolg9 = ['RDFN','NTNX','LRCX','AMAT','SPY'] 
    symbolga = ['TSLA','BABA','XLNX','NVDA','XBI']
    symbolgb = ['QQQ','JD','MA','MTN','OLED']
    symbolgc = ['PYPL','SFIX','EA','GOOGL','MU']
    symbolgd = ['FB','AAPL','AMZN','IWM','PMF']
    for symbol in symbolg1:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolg2:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolg3:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolg4:    
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)           
    for symbol in symbolg5:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolg6:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolg7:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolg8:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolg9:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolga:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolgb:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolgc:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolgd:
        stock_daily=get_stock_daily(symbol,sizeoption)                                                                                        