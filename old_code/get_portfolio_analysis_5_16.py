import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime, csv, os, urllib, re;
from pandas_datareader.data import Options
# get data from Yahoo Finance, TA recommendation, Portfolio Sharpe Ratio


start = datetime.datetime(2012,12,31)
end = datetime.date.today()
SPY_data = web.DataReader('SPY', "yahoo", start, end)
current_portfolio_list = SPY_data['Adj Close']
data=stockTA(SPY_data)
today_recommend=data.tail(1).rename(index={len(data)-1: 'SPY'})

return_list_vs_qqq = []
return_list_vs_spy = []
return_list = []
nasdaq_return_dict = {}
relative_return_dict = {}
rui2 = {}
nasdaq_100_stocks = ['FB', 'GOOGL', 'AMZN', 'V', 'NVDA', 'CTRP', 'TRIP','CMCM','RWLK','XLF']
for nasdaq_stock in nasdaq_100_stocks:
	start = datetime.datetime(2012,12,31)
	end = datetime.date.today()
	current_stock = web.DataReader(nasdaq_stock, "yahoo", start, end)
	data=stockTA(current_stock)
	tmp_recommend=data.tail(1).rename(index={len(data)-1: nasdaq_stock})
	today_recommend = pd.concat([today_recommend, tmp_recommend], axis=1)
	#tmp2=data.tail(1)[['Long Term','Medium Term','Short Term']].values
	#rui2.concat([rui2, tmp2], axis=1)
	tmp_list = current_stock['Adj Close']
	current_portfolio_list = pd.concat([current_portfolio_list, tmp_list], axis=1)
current_portfolio_list.columns = ['FB', 'GOOGL', 'AMZN', 'V', 'NVDA', 'CTRP', 'TRIP','CMCM','RWLK','XLF']
current_portfolio_list.to_csv('Favorite.csv')

def stockTA(current_stock)
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
	return data


#amzn_data = current_portfolio_list['AMZN']
#returns = np.log(current_portfolio_list / current_portfolio_list.shift(1))
