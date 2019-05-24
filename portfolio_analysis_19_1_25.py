#Refer to https://towardsdatascience.com/efficient-frontier-optimize-portfolio-with-scipy-57456428323e
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
import matplotlib
import matplotlib.dates as mdates
import matplotlib.path as mpath
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib import style

def combine_stocks(symbols):
        start_date ='2016-12-30'
        end_date='2017-12-29'
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
        #print(df1)
        df1.to_csv('Bei_IRA.csv')
        return df1
def get_risk(prices):
    return (prices / prices.shift(1) - 1).dropna().std().values

def get_return(prices):
    return ((prices / prices.shift(1) - 1).dropna().mean() * np.sqrt(250)).values

stocks = ['TSLA','FB','BABA','AMZN']
BeiIRA_data=combine_stocks(stocks)
prices = BeiIRA_data.dropna()

returns = prices.pct_change()
mean_daily_returns = returns.mean()
cov_matrix = returns.cov()
 
#set number of runs of random portfolio weights
num_portfolios = 25000
 
#set up array to hold results
#We have increased the size of the array to hold the weight values for each stock
results = np.zeros((4+len(stocks)-1,num_portfolios))
 
for i in range(num_portfolios):
    #select random weights for portfolio holdings
    weights = np.array(np.random.random(4))
    #rebalance weights to sum to 1
    weights /= np.sum(weights)
    
    #calculate portfolio return and volatility
    portfolio_return = np.sum(mean_daily_returns * weights) * 252
    portfolio_std_dev = np.sqrt(np.dot(weights.T,np.dot(cov_matrix, weights))) * np.sqrt(252)
    
    #store results in results array
    results[0,i] = portfolio_return
    results[1,i] = portfolio_std_dev
    #store Sharpe Ratio (return / volatility) - risk free rate element excluded for simplicity
    results[2,i] = results[0,i] / results[1,i]
    #iterate through the weight vector and add data to results array
    for j in range(len(weights)):
        results[j+3,i] = weights[j]
 
#convert results array to Pandas DataFrame
results_frame = pd.DataFrame(results.T,columns=['ret','stdev','sharpe',stocks[0],stocks[1],stocks[2],stocks[3]])
 
#locate position of portfolio with highest Sharpe Ratio
max_sharpe_port = results_frame.iloc[results_frame['sharpe'].idxmax()]
#locate positon of portfolio with minimum standard deviation
min_vol_port = results_frame.iloc[results_frame['stdev'].idxmin()]
 
#create scatter plot coloured by Sharpe Ratio
fig = matplotlib.pyplot.gcf()
plt.scatter(results_frame.stdev,results_frame.ret,c=results_frame.sharpe,cmap='RdYlBu')
plt.xlabel('Volatility')
plt.ylabel('Returns')
plt.colorbar()
#plot red star to highlight position of portfolio with highest Sharpe Ratio
plt.scatter(max_sharpe_port[1],max_sharpe_port[0],marker=(5,1,0),color='r',s=1000)
#plot green star to highlight position of minimum variance portfolio
plt.scatter(min_vol_port[1],min_vol_port[0],marker=(5,1,0),color='g',s=1000)
fig.savefig('test2png.png', dpi=80)
print(max_sharpe_port)
weights = max_sharpe_port[3:7].tolist()
print(weights)
weights = np.asarray(weights)

#the rest of the code compute annualized return
portfolio1 = BeiIRA_data
#returns = np.log(portfolio1 / portfolio1.shift(1))
port_returns=np.sum(returns.mean()*weights)*252
#portfolio_return = np.sum(mean_daily_returns * weights) * 252
port_variance=np.sqrt(np.dot(weights.T,np.dot(returns.cov()*252,weights)))
sharpe_ratio_p1 = port_returns/port_variance
print(port_returns)
print(port_variance)
print(sharpe_ratio_p1)
#print(min_vol_port)

