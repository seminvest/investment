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
    data = pd.read_csv("/Users/ruitang/Dropbox/Program/Stock_Analysis/watchlist.csv") 
    start_date='2017-12-29'
    end_date=sys.argv[1]
    threshold=0.81
    for j in range(len(data)):
        symbol=data.loc[j,'symbol']
        FV=data.loc[j,'FV']
        df= get_stock_time_frame(symbol,start_date,end_date)
        df1=df.loc[start_date:end_date,'adjusted close']
        end_price=df1.iloc[-1]
        if float(end_price)< float(FV)*0.65:
            #DV=round(float(FV)*threshold)
            print(Fore.GREEN + symbol,end_price,FV,'strong buy')
            print(Style.RESET_ALL)
        elif float(FV)*0.81>=float(end_price)> float(FV)*0.65:
            print(Fore.BLUE + symbol,end_price,FV,'buy')
            print(Style.RESET_ALL)                
        elif float(FV)>=float(end_price)> float(FV)*0.81:
            print(Fore.BLACK + symbol,end_price,FV,'hold')
            print(Style.RESET_ALL)    
        elif float(FV)*1.2 >= float(end_price)> float(FV):
            print(Fore.MAGENTA + symbol,end_price,FV,'sell')
            print(Style.RESET_ALL)
        elif float(end_price)> float(FV)*1.2:
            print(Fore.RED+ symbol,end_price,FV,'strong sell')
            print(Style.RESET_ALL)    

