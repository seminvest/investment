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

end_date_2013='2013-12-31'
end_date_2014='2014-12-31'
end_date_2015='2015-12-31'
end_date_2016='2016-12-30'
end_date_2017='2017-12-29'
end_date_2018='2018-12-31'

def get_stock_time_frame(symbol, start_date, end_date):
    dates=pd.date_range(start_date,end_date)
    df1=pd.DataFrame(index=dates)
    root = '/Users/ruitang/Dropbox/Program/Stock_Analysis'
    day = 'daily_data'
    subdir = os.path.join(root, day,symbol + '.csv')
    df_temp=pd.read_csv(subdir,index_col="date",parse_dates=True,na_values=['nan'])
    df1=df1.join(df_temp,how='inner')
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
    symbols = ['TSLA','AMZN','GOOGL','MA','PYPL','V','SQ']
    start_date='2017-12-29'
    end_date='2019-01-25'
    gain_threshold=0.05
    volume_multi=2.5
    for symbol in symbols:
        print(symbol,"start")
        #root = '/Users/ruitang/Dropbox/Program/Stock_Analysis'
        #day = 'daily_data'
        #subdir = os.path.join(root, day,symbol + '.csv')
        #df_temp=pd.read_csv(subdir,index_col="date",parse_dates=True,na_values=['nan'])       
        df= get_stock_time_frame(symbol,start_date,end_date)
        #print(df[df['volume']>volume_multi*df["volume"].median()])
        print("median vlume", df["volume"].median())
        recent_year_median=df["volume"].median()
        df1=df.loc[start_date:end_date,'adjusted close']
        df1=df1.to_frame(name='close')
        fiveday_return=compute_returns_general(df1,5)
        #fiveday_return2=df1.rolling_mean(D, 5)
        tenday_return=compute_returns_general(df1,10)
        twentyday_return=compute_returns_general(df1,20)
        fiftyday_return=compute_returns_general(df1,50)
        fb_return=df1.copy()
        fb_return=fb_return.join(fiveday_return,how='inner')
        fb_return=fb_return.join(tenday_return,how='inner')
        fb_return=fb_return.join(twentyday_return,how='inner')
        fb_return=fb_return.join(fiftyday_return,how='inner')
        root = '/Users/ruitang/Dropbox/Program/Stock_Analysis'
        day = 'daily_data'
        subdir = os.path.join(root, day,symbol + '_return.csv')
        fb_return.to_csv(subdir, index=True)
        fb_return_tradeable=fb_return[(fb_return['5days']>gain_threshold)&(fb_return['50days']<0)]
        #fb_return_tradeable.to_csv("{}_trade_return.csv".format(symbol), index=True)
        df_new=df.reset_index()
        df_new=df_new.rename(columns={"index":"date"})
        print(fb_return_tradeable)
        fb_return_tradeable=fb_return_tradeable.reset_index()
        fb_return_tradeable= fb_return_tradeable.rename(columns={"index":"date"})
        #print(fb_return_tradeable)
        #for loopdate in fb_return_tradeable['date']
        for loopdate in fb_return_tradeable['date']:
            print(loopdate)
            #df_tmp=df.loc[:loopdate].tail(1)
            df_tmp=df.loc[loopdate:loopdate]
            #print(df_tmp)
            if df_tmp.iloc[0]["volume"]>1.2*recent_year_median:
                print(df_tmp)
        print(symbol,"finish")

        #df.loc[:'2018-05-08'].tail(12)
        #df.index[df==df.loc['2018-05-08']]
