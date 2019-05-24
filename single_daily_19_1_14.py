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


def combine_stocks(symbols, start_date, end_date):
	dates=pd.date_range(start_date,end_date)
	#print(dates[0])
	df1=pd.DataFrame(index=dates)
	for symbol in symbols:
		print(symbol,"start")
		df_temp=pd.read_csv("{}.csv".format(symbol),index_col="date",parse_dates=True,usecols=['date','adjusted close'],na_values=['nan'])
		df_temp = df_temp.rename(columns={"adjusted close":symbol})
		df1=df1.join(df_temp,how='inner')
		df1["50d"]=df1[symbol].rolling(window=50,center=False).mean()
		df1["20d"]=df1[symbol].rolling(window=20,center=False).mean()
		df1["5d"]=df1[symbol].rolling(window=5,center=False).mean()
		#df1["20d"].shift(1)
		#df1["50d"].shift(1)
		df1["20d_1"]=df1['20d'].shift(1)
		df1["5d_1"]=df1['5d'].shift(1)
		df1['Medium Term'] = 'hold'
		df1.loc[(df1['5d_1']> df1['20d_1']) & (df1['20d'] >= df1['5d']), 'Medium Term'] = 'sell'
		df1.loc[(df1['5d_1']< df1['20d_1']) & (df1['20d']<= df1['5d']), 'Medium Term'] = 'buy'
		print(symbol,"finish")
	print(df1)
	df1.to_csv('tmp.csv')
	return df1

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    # TODO: Your code here
    # Note: Returned DataFrame must have the same number of rows
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:]/df[:-1].values)-1
    daily_returns.iloc[0,:] = 0
    return daily_returns


start_date ='2018-08-31'
end_date='2019-01-11'
symbols = ['FB']
for symbol in symbols:
	get_stock_daily(symbol)
stock_data=combine_stocks(symbols,start_date,end_date)


