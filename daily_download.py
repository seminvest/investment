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
        day = 'daily_data'
        subdir = os.path.join(root, day,symbol + '.csv')
        print(subdir)
        data.to_csv(subdir, index=False)
        print(symbol,"finish")
        return data

if __name__ == "__main__":
    sizeoption = 'full'
    API_URL = "https://www.alphavantage.co/query"
    #SaaS big names
    symbolg1 = ['CRM','NOW','WDAY','NEWR','HUBS']
    #SaaS watch list
    symbolg2 = ['TWLO','ZEN','ADBE','OKTA','AYX']
    #SaaS watch list2
    symbolg3 = ['INTU','UPWK','CBLK','ZS','DOCU']
    symbolg4 = ['DATA','COUP','MDB','ZUO','DBX'] 
    #semi I like and EDA
    symbolg5 = ['XLNX','NVDA','ANSS','SNPS','CDNS'] 
    #MAGA,FANG 
    symbolg6 = ['MSFT','FB','AMZN','AAPL','GOOGL'] 
    # payment stocks
    symbolg7 = ['V','PYPL','AXP','MA','SQ'] 
    # consumer stock
    symbolg8 = ['TSLA','HD','IRBT','DIS','COST'] 
    # platform stock
    symbolg9 = ['CME','OLED','STNE','DFS','TWTR']
    # China name
    symbolga = ['BABA','BILI','NTES','JD','CTRP']
    # Index 
    symbolgb = ['QQQ','SPY','IWM','XBI','IBB']
    # Healthcare and medical
    symbolgc = ['ILMN','ISRG','UNH','PFE','CVS']    
    # Cyclic stock
    symbolgd = ['MU','WDC','AMD','AVGO','QRVO']   
    # holding and previous own
    symbolge = ['RDFN','PMF','MTN','WFC','QCOM'] 
    # keep adding
    symbolgf = ['ANET','LOW','SWKS','ADI','TMUS'] 
    # keep adding
    symbolgg = ['PXLW','WFC','JPM','BAC','MET']    
    # keep adding
    symbolgh = ['MO','JNJ','CSCO','FFIV','ABT']       
    symbolgi = ['CLDR','MOBL','ALRM','TTD','PAYC']
    symbolgj = ['VEEV','MOBL'] 
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
    time.sleep(60)    
    for symbol in symbolge:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolgf:
        stock_daily=get_stock_daily(symbol,sizeoption)
    time.sleep(60)    
    for symbol in symbolgg:
        stock_daily=get_stock_daily(symbol,sizeoption)        
    time.sleep(60)    
    for symbol in symbolgh:
        stock_daily=get_stock_daily(symbol,sizeoption)                
    time.sleep(60)    
    for symbol in symbolgi:
        stock_daily=get_stock_daily(symbol,sizeoption)                        