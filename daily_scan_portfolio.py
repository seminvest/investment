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
import sys
import colorama
from colorama import Fore, Style

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

def compute_returns_general(df,general):
    """Compute and return the daily return values."""
    # TODO: Your code here
    # Note: Returned DataFrame must have the same number of rows
    daily_returns = df.copy()
    columnname = str(general)+"days"
    #daily_returns = 0
    daily_returns[general:] = (df[general:]/df[:-general].values)-1
    daily_returns = daily_returns.rename(columns={"close":columnname})
    daily_returns.iloc[0:general] = 0
    #daily_returns.round(3)
    return daily_returns.round(3)  

if __name__ == "__main__":
    print(sys.argv[1])
    sizeoption = 'full'
    API_URL = "https://www.alphavantage.co/query"
    #SaaS big names
    symbolg1 = ['NEWR','HUBS','TSLA','CLDR','NVDA']
    #SaaS watch list
    symbolg2 = ['XLNX','JD','BILI','GOOGL','MA'] 
    #MAGA,FANG 
    symbolg3 = ['FB','STNE','AMZN','AAPL','BABA'] 
    # payment stocks
    for symbol in symbolg1:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolg2:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolg3:
        stock_daily=get_stock_daily(symbol,sizeoption)        
    symbols = ['NEWR','HUBS','TSLA','CLDR','XLNX','JD','BILI','GOOGL','MA','STNE','AMZN','AAPL','BABA','FB','NVDA']
    start_date='2017-12-29'
    end_date=sys.argv[1]
    pos_threshold=0.05
    neg_threshold=-0.05   
    volume_multi=2.5
    for symbol in symbols:
        print(symbol,"start")
        df= get_stock_time_frame(symbol,start_date,end_date)
        #print(df[df['volume']>volume_multi*df["volume"].median()])
        #print("median value", df["volume"].median())
        df1=df.loc[start_date:end_date,'adjusted close']
        df1=df1.to_frame(name='close')
        fiveday_return=compute_returns_general(df1,5)
        tenday_return=compute_returns_general(df1,10)
        twentyday_return=compute_returns_general(df1,20)
        fb_return=df1.copy()
        fb_return=fb_return.join(fiveday_return,how='inner')
        fb_return=fb_return.join(tenday_return,how='inner')
        fb_return=fb_return.join(twentyday_return,how='inner')
        root = '/Users/ruitang/Dropbox/Program/Stock_Analysis'
        day = 'daily_data'
        subdir = os.path.join(root, day,symbol + '_return.csv')
        fb_return.to_csv(subdir, index=True)
        most_recent_return=fb_return.tail(1)
        print(most_recent_return)
        if float(most_recent_return['5days'])>pos_threshold:
            #fb_return_tradeable=most_recent_return[most_recent_return['5days']>gain_threshold]
            print(Fore.GREEN + symbol,'is trending higher')
            print(Style.RESET_ALL)
        if float(most_recent_return['5days'])<neg_threshold:
            #fb_return_tradeable=most_recent_return[most_recent_return['5days']>gain_threshold]
            print(Fore.RED + symbol,'is trending lower')
            print(Style.RESET_ALL)

