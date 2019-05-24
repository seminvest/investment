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
    symbols = ['CRM','NOW','WDAY','NEWR','HUBS','TWLO','ZEN','ADBE','OKTA','DATA','XLNX','NVDA','ANSS','SNPS','CDNS','MSFT','FB','AAPL', 'V','PYPL','AXP','MA','SQ','TSLA','HD','IRBT','DIS','COST','CME','OLED','BABA','NTES','ILMN','ISRG','UNH','AVGO','QRVO','WD','MTN','WFC','QCOM']
    start_date='2017-12-29'
    end_date=sys.argv[1]
    gain_threshold=0.05
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
        tmp=fb_return.tail(1)
        print(tmp)
        if float(tmp['5days'])>gain_threshold:
            fb_return_tradeable=tmp[tmp['5days']>gain_threshold]
        #fb_return_tradeable=fb_return[fb_return['10days']>gain_threshold]
        #fb_return_tradeable.to_csv("{}_trade_return.csv".format(symbol), index=True)
            print('trending_stock')
            print(fb_return_tradeable)
        #print(symbol,"finish")
        #df.loc[:'2018-05-08'].tail(12)
        #df.index[df==df.loc['2018-05-08']]
