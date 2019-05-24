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
	start_date ='2018-09-28'
	end_date='2019-01-11'
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
	df1.to_csv('Bei_IRA.csv')
	return df1

symbols = ['TSLA','FB','BABA','AMZN']
for symbol in symbols:
	get_stock_daily(symbol)

BeiIRA_data=combine_stocks(symbols)
stock_number = [100,111,100,23]
total_stock_value = BeiIRA_data*stock_number


weights = [0.2468,0.1702,0.1536,0.4294]
weights = np.asarray(weights)

#the rest of the code compute annualized return
portfolio1 = BeiIRA_data
returns = np.log(portfolio1 / portfolio1.shift(1))
port_returns=np.sum(returns.mean()*weights)*252
port_variance=np.sqrt(np.dot(weights.T,np.dot(returns.cov()*252,weights)))
sharpe_ratio_p1 = port_returns/port_variance
print(port_returns)
print(sharpe_ratio_p1)


