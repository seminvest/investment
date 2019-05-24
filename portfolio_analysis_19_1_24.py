#https://towardsdatascience.com/efficient-frontier-optimize-portfolio-with-scipy-57456428323e
import requests
import alpha_vantage
import json
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import time
import os
from scipy.optimize import minimize

def combine_stocks(symbols):
        start_date ='2017-12-28'
        end_date='2019-01-23'
        dates=pd.date_range(start_date,end_date)
	#print(dates[0])
        df1=pd.DataFrame(index=dates)
        for symbol in symbols:
                print(symbol,"start")
                root = '/Users/ruitang/Dropbox/Program/Stock_Analysis'
                day = 'daily_data'
                subdir = os.path.join(root, day,symbol + '.csv')
                df_temp=pd.read_csv(subdir,index_col="date",parse_dates=True,usecols=['date','adjusted close'],na_values=['nan'])
                df_temp = df_temp.rename(columns={"adjusted close":symbol})
                df1=df1.join(df_temp,how='inner')
                print(symbol,"finish")
        print(df1)
        df1.to_csv('Bei_IRA.csv')
        return df1
def get_risk(prices):
    return (prices / prices.shift(1) - 1).dropna().std().values

def get_return(prices):
    return ((prices / prices.shift(1) - 1).dropna().mean() * np.sqrt(250)).values

symbols = ['TSLA','FB','BABA','AMZN']
BeiIRA_data=combine_stocks(symbols)
prices = BeiIRA_data.dropna()
risk_v = get_risk(prices)
return_v = get_return(prices)
fig, ax = plt.subplots()
ax.scatter(x=risk_v, y=return_v, alpha=0.5)
ax.set(title='Return and Risk', xlabel='Risk', ylabel='Return')
for i, symbol in enumerate(symbols):
    ax.annotate(symbol, (risk_v[i], return_v[i]))
plt.show()


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


