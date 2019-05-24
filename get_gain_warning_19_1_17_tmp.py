#https://stackoverflow.com/questions/48071949/how-to-use-the-alpha-vantage-api-directly-from-python
#https://www.profitaddaweb.com/2018/07/alpha-vantage-preprocessed-free-apis-in.html
import requests
import alpha_vantage
import json
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import time
def get_stock_daily(symbol):
        data = { "function": "TIME_SERIES_DAILY_ADJUSTED", 
        "symbol": symbol,
        "outputsize" : "compact",       
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

def combine_stocks(symbols):
	start_date ='2018-08-15'
	end_date='2019-01-08'
	dates=pd.date_range(start_date,end_date)
	#print(dates[0])
	df1=pd.DataFrame(index=dates)
	for symbol in symbols:
		print(symbol,"start")
		df_temp=pd.read_csv("{}.csv".format(symbol),index_col="date",parse_dates=True,usecols=['date','adjusted close'],na_values=['nan'])
		df_temp = df_temp.rename(columns={"adjusted close":symbol})
		df1=df1.join(df_temp,how='inner')
		print(symbol,"finish")
	print(df1)
	df1.to_csv('SAAS_100_daily.csv')
	return df1

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    # TODO: Your code here
    # Note: Returned DataFrame must have the same number of rows
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:]/df[:-1].values)-1
    daily_returns.iloc[0,:] = 0
    return daily_returns

def compute_returns_general(df,general):
    """Compute and return the daily return values."""
    # TODO: Your code here
    # Note: Returned DataFrame must have the same number of rows
    daily_returns = df.copy()
    #daily_returns = 0
    daily_returns[general:] = (df[general:]/df[:-general].values)-1
    daily_returns = daily_returns.rename(columns={"close":general})
    daily_returns.iloc[0:general] = 0
    return daily_returns   


API_URL = "https://www.alphavantage.co/query" 
symbols = ['CRM','NOW','WDAY','AYX','HUBS']
symbols2 = ['TWLO','DOCU','ADBE','OKTA','NEWR']
symbols3 = ['INTU','PLAN','DBX','ZS','ZEN']
for symbol in symbols:
	get_stock_daily(symbol)

time.sleep(60)

for symbol in symbols2:
	get_stock_daily(symbol)

time.sleep(60)

for symbol in symbols3:
	get_stock_daily(symbol)

symbols = ['CRM','NOW','WDAY','AYX','HUBS','TWLO','DOCU','ADBE','OKTA','NEWR','INTU','DBX','ZS','ZEN']
saas_data=combine_stocks(symbols)

fiveday_return=compute_returns_general(df1,5)
tenday_return=compute_returns_general(df1,10)
twentyday_return=compute_returns_general(df1,20)
fb_return=fiveday_return.copy()
fb_return=fb_return.join(tenday_return,how='inner')
fb_return=fb_return.join(twentyday_return,how='inner')
fb_return_5=fb_return[fb_return[1]>0.05]
