import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime, csv, os, urllib, re;
rom pandas_datareader.data import Options

start = datetime.datetime(2012,12,31)
end = datetime.datetime(2016,12,30)
SPY_data = web.DataReader('SPY', "yahoo", start, end)
current_portfolio_list = SPY_data['Adj Close']

return_list_vs_qqq = []
return_list_vs_spy = []
return_list = []
nasdaq_return_dict = {}
relative_return_dict = {}
nasdaq_100_stocks = ['FB', 'GOOGL', 'AMZN', 'V', 'NVDA', 'CTRP', 'TRIP','CMCM','RWLK','XLF']
for nasdaq_stock in nasdaq_100_stocks:
	start = datetime.datetime(2012,12,31)
	end = datetime.date.today()
	current_stock = web.DataReader(nasdaq_stock, "yahoo", start, end)
	current_stock["200d"]=pd.rolling_mean(current_stock['Adj Close'], 200)
	current_stock["50d"]=pd.rolling_mean(current_stock['Adj Close'], 50)
	current_stock["20d"]=pd.rolling_mean(current_stock['Adj Close'], 20)
	current_stock["5d"]=pd.rolling_mean(current_stock['Adj Close'], 5)
	data = current_stock[['Adj Close','200d','50d','20d','5d']]
	data['Long Term'] = 'hold'
	data['Long Term'][(data['50d'] > data['200d']) & (data['200d'] < data['Adj Close'])] = 'buy'
	data['Long Term'][(data['50d'] < data['200d']) & (data['200d'] > data['Adj Close'])] = 'sell'
	data['Medium Term'] = 'hold'
	data['Medium Term'][(data['20d'] > data['50d']) & (data['50d'] < data['Adj Close'])] = 'buy'
	data['Medium Term'][(data['20d'] < data['50d']) & (data['50d'] > data['Adj Close'])] = 'sell'
	data['Short Term'] = 'hold'
	data['Short Term'][(data['5d'] > data['20d']) & (data['20d'] < data['Adj Close'])] = 'buy'
	data['Short Term'][(data['5d'] < data['20d']) & (data['20d'] > data['Adj Close'])] = 'sell'
	data.to_csv(nasdaq_stock + '.csv')
	tmp_list = current_stock['Adj Close']
	current_portfolio_list = pd.concat([current_portfolio_list, tmp_list], axis=1)
current_portfolio_list.columns = ['SPY','QQQ','AAPL', 'FB', 'GOOGL', 'AMZN', 'NFLX', 'V', 'NVDA', 'PCLN', 'MA', 'BIDU', 'NTES', 'EDU', 'CTRP', 'AVGO','CRM','NKE','HD','DIS']
current_portfolio_list.to_csv('Favorite.csv')

weights = [0.25,0.25,0.25,0.25]
weights = np.asarray(weights)
portfolio1 = current_portfolio_list[['AMZN','FB','V','GOOGL']]
returns = np.log(portfolio1 / portfolio1.shift(1))
port_returns=np.sum(returns.mean()*weights)*252
port_variance=np.sqrt(np.dot(weights.T,np.dot(returns.cov()*252,weights)))
sharpe_ratio_p1 = port_returns/port_variance

portfolio2 = current_portfolio_list[['CTRP','NTES','AAPL','NVDA']]
returns = np.log(portfolio1 / portfolio1.shift(1))
port_returns=np.sum(returns.mean()*weights)*252
port_variance=np.sqrt(np.dot(weights.T,np.dot(returns.cov()*252,weights)))
sharpe_ratio_p2 = port_returns/port_variance

weights = [0.2,0.2,0.2,0.2,0.2]
weights = np.asarray(weights)
portfolio3 = current_portfolio_list[['AMZN','FB','V','GOOGL','AAPL']]
returns = np.log(portfolio3 / portfolio3.shift(1))
port_returns=np.sum(returns.mean()*weights)*252
port_variance=np.sqrt(np.dot(weights.T,np.dot(returns.cov()*252,weights)))
sharpe_ratio_p2 = port_returns/port_variance


#amzn_data = current_portfolio_list['AMZN']
#returns = np.log(current_portfolio_list / current_portfolio_list.shift(1))
