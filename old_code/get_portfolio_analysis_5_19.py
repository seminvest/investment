import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime, csv, os, urllib, re;
from pandas_datareader.data import Options
# get data from Yahoo Finance, TA recommendation, Portfolio Sharpe Ratio
# 5/19 Test Google Finance
def stockTA(current_stock, nasdaq_stock):
	current_stock["200d"]=current_stock['Close'].rolling(window=200,center=False).mean()
	current_stock["50d"]=current_stock['Close'].rolling(window=50,center=False).mean()
	current_stock["20d"]=current_stock['Close'].rolling(window=20,center=False).mean()
	current_stock["5d"]=current_stock['Close'].rolling(window=5,center=False).mean()
	data = current_stock[['Close','200d','50d','20d','5d']]
	data['Long Term'] = 'hold'
	data['Long Term'][(data['50d'] > data['200d']) & (data['200d'] < data['Close'])] = 'buy'
	data['Long Term'][(data['50d'] < data['200d']) & (data['200d'] > data['Close'])] = 'sell'
	data['Medium Term'] = 'hold'
	data['Medium Term'][(data['20d'] > data['50d']) & (data['50d'] < data['Close'])] = 'buy'
	data['Medium Term'][(data['20d'] < data['50d']) & (data['50d'] > data['Close'])] = 'sell'
	data['Short Term'] = 'hold'
	data['Short Term'][(data['5d'] > data['20d']) & (data['20d'] < data['Close'])] = 'buy'
	data['Short Term'][(data['5d'] < data['20d']) & (data['20d'] > data['Close'])] = 'sell'
	data.to_csv(nasdaq_stock + '.csv')
	return data

start = datetime.datetime(2012,12,31)
end = datetime.date.today()
SPY_data = web.DataReader('SPY', "google", start, end)
current_portfolio_list = SPY_data['Close']
data=stockTA(SPY_data,'SPY')
today_recommend=data.tail(1)

return_list_vs_qqq = []
return_list_vs_spy = []
return_list = []
nasdaq_return_dict = {}
relative_return_dict = {}
nasdaq_100_stocks = ['FB', 'GOOGL', 'AMZN', 'V', 'NVDA', 'CTRP', 'TRIP','CMCM','RWLK','XLF']
for nasdaq_stock in nasdaq_100_stocks:
	start = datetime.datetime(2012,12,31)
	end = datetime.date.today()
	current_stock = web.DataReader(nasdaq_stock, "google", start, end)
	data=stockTA(current_stock, nasdaq_stock)
	tmp_recommend=data.tail(1)
	today_recommend = today_recommend.append(tmp_recommend, ignore_index=True)
	tmp_list = current_stock['Close']
	current_portfolio_list = pd.concat([current_portfolio_list, tmp_list], axis=1)

today_recommend=today_recommend.rename(index={0: 'SPY',1:'FB',2:'GOOGL',3:'AMZN',4:'V',5:'NVDA',6:'CTRP',7:'TRIP',8:'CMCM',9:'RWLK',10:'XLF'})
today_recommend.to_csv('current_recommend.csv')	
current_portfolio_list.columns = ['SPY','FB', 'GOOGL', 'AMZN', 'V', 'NVDA', 'CTRP', 'TRIP','CMCM','RWLK','XLF']
current_portfolio_list.to_csv('Favorite.csv')




#amzn_data = current_portfolio_list['AMZN']
#returns = np.log(current_portfolio_list / current_portfolio_list.shift(1))
