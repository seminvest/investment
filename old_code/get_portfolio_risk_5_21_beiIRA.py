import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime, csv, os, urllib, re;
from pandas_datareader.data import Options

start = datetime.datetime(2014,12,31)
end = datetime.date.today()
SPY_data = web.DataReader('SPY', "google", start, end)
current_portfolio_list = SPY_data['Close']

return_list_vs_qqq = []
return_list_vs_spy = []
return_list = []
nasdaq_return_dict = {}
relative_return_dict = {}
nasdaq_100_stocks = ['TSLA', 'BABA', 'AMZN']
for nasdaq_stock in nasdaq_100_stocks:
	start = datetime.datetime(2014,12,31)
	end = datetime.date.today()
	current_stock = web.DataReader(nasdaq_stock, "google", start, end)
	tmp_list = current_stock['Close']
	current_portfolio_list = pd.concat([current_portfolio_list, tmp_list], axis=1)
current_portfolio_list.columns = ['SPY','TSLA', 'BABA', 'AMZN']
current_portfolio_list.to_csv('Bei_IRA.csv')

weights = [0.577,0.1515,0.2714]
weights = np.asarray(weights)
portfolio1 = current_portfolio_list[nasdaq_100_stocks]
returns = np.log(portfolio1 / portfolio1.shift(1))
port_returns=np.sum(returns.mean()*weights)*252
port_variance=np.sqrt(np.dot(weights.T,np.dot(returns.cov()*252,weights)))
sharpe_ratio_p1 = port_returns/port_variance
print(port_returns)
print(sharpe_ratio_p1)


