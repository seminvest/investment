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

def get_stock_time_frame(symbol, start_date, end_date):
    dates=pd.date_range(start_date,end_date)
    df1=pd.DataFrame(index=dates)
    print(symbol,"start")
    df_temp=pd.read_csv("{}.csv".format(symbol),index_col="date",parse_dates=True,na_values=['nan'])
    df1=df1.join(df_temp,how='inner')
    print(symbol,"finish")
    df1.to_csv('tmp.csv')
    return df1
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
        data.to_csv(symbol + '.csv', index=False)
        print(symbol,"finish")
        return data
def compute_returns_general(df,general):
    """Compute and return the daily return values."""
    # TODO: Your code here
    # Note: Returned DataFrame must have the same number of rows
    daily_returns = df.copy()
    #daily_returns = 0
    daily_returns[general:] = (df[general:]/df[:-general].values)-1
    daily_returns = daily_returns.rename(columns={"close":general})
    daily_returns.iloc[0:general] = 0
    #daily_returns.round(3)
    return daily_returns.round(3)  

if __name__ == "__main__":
    symbols = ['AAPL','AMZN']
    sizeoption = 'full'
    API_URL = "https://www.alphavantage.co/query" 
    start_date='2017-12-29'
    end_date='2019-01-17'
    for symbol in symbols:
        stock_daily=get_stock_daily(symbol,sizeoption)
        df= get_stock_time_frame(symbol,start_date,end_date)
        df1=df.loc[start_date:end_date,'adjusted close']
        df1=df1.to_frame(name='close')
        fiveday_return=compute_returns_general(df1,5)
        tenday_return=compute_returns_general(df1,10)
        twentyday_return=compute_returns_general(df1,20)
        fb_return=fiveday_return.copy()
        fb_return=fb_return.join(tenday_return,how='inner')
        fb_return=fb_return.join(twentyday_return,how='inner')
        fb_return.to_csv("{}_return.csv".format(symbol), index=True)
        fb_return_10=fb_return[fb_return>0.1]
        print(fb_return_10.dropna(thresh=1))
