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
    fvlimit=0.8
    dvlimit=0.65
    ovlimit=1.2

    for j in range(len(data)):
        symbol=data.loc[j,'symbol']
        FV=data.loc[j,'FV']
        MarketCap = data.loc[j,'CAP']
        df= get_stock_time_frame(symbol,start_date,end_date)
        df1=df.loc[start_date:end_date,'adjusted close']
        end_price=df1.iloc[-1]
        if MarketCap == 'L':
            factor=0.9
            #print(Fore.GREEN + symbol,factor)
        elif MarketCap == 'M':
            factor=1
            #print(Fore.GREEN + symbol,factor)  
        elif MarketCap == 'S':
            factor=1.1
            #print(Fore.GREEN + symbol,factor)
        print (symbol,factor)    
        fvthreshold=fvlimit/factor
        dvthreshold=dvlimit/factor
        ovthreshold=ovlimit*factor
        print (symbol,factor, round(float(FV)*ovthreshold,2), FV, round(float(FV)*fvthreshold,2), round(float(FV)*dvthreshold,2))  
        #print(dvthreshold,fvthreshold,ovthreshold)
        if float(end_price)< float(FV)*dvthreshold:
            #DV=round(float(FV)*threshold)
            print(Fore.GREEN + symbol,'current price',end_price,'<under value threshold',round(float(FV)*dvthreshold),'strong buy')
            print(Style.RESET_ALL)
        elif float(FV)*fvthreshold>=float(end_price)> float(FV)*dvthreshold:
            print(Fore.BLUE + symbol,'current price',end_price,'<fair value threshold',round(float(FV)*fvthreshold),':','>under value threshold',round(float(FV)*dvthreshold),'buy')
            print(Style.RESET_ALL)                
        elif float(FV)>=float(end_price)> float(FV)*fvthreshold:
            print(Fore.BLACK + symbol,end_price,'within the fair value bound',FV,'hold')
            print(Style.RESET_ALL)    
        elif float(FV)*ovthreshold >= float(end_price)> float(FV):
            print(Fore.MAGENTA + symbol,end_price,FV,'sell')
            print(Style.RESET_ALL)
        elif float(end_price)> float(FV)*ovthreshold:
            print(Fore.RED+ symbol,end_price,FV,'strong sell')
            print(Style.RESET_ALL)    

