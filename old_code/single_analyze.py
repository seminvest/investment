import pandas as pd
import pandas.io.data as web 
import numpy as np
import datetime; import csv; import os; import urllib; import re; 
from pandas_datareader.data import Options
tsla = Options('TSLA','yahoo')
data = tsla.get_all_data()
data.iloc[0:5, 0:5]

start = datetime.datetime(2010,12,31)
end = datetime.datetime(2016,12,30)
current_stock = web.DataReader('AMZN', "yahoo", start, end)
current_stock.to_csv('AMZN.csv')
#data = df['close']
data = current_stock['Adj Close']
# To use log return to help calculate
returns = np.log(data / data.shift(1))
# compute mean annual return
returns.mean()*252
returns.cov()*252



stock_series=current_stock['2010-12-31':'2011-12-31']
return_2011 = (stock_series["Adj Close"][len(stock_series)-1]-stock_series["Adj Close"][0])/stock_series["Adj Close"][0]
stock_series=current_stock['2011-12-30':'2012-12-31']
return_2012 = (stock_series["Adj Close"][len(stock_series)-1]-stock_series["Adj Close"][0])/stock_series["Adj Close"][0]
stock_series=current_stock['2012-12-31':'2013-12-31']
return_2013 = (stock_series["Adj Close"][len(stock_series)-1]-stock_series["Adj Close"][0])/stock_series["Adj Close"][0]
stock_series=current_stock['2013-12-31':'2014-12-31']
return_2014 = (stock_series["Adj Close"][len(stock_series)-1]-stock_series["Adj Close"][0])/stock_series["Adj Close"][0]
stock_series=current_stock['2014-12-31':'2015-12-31']
return_2015 = (stock_series["Adj Close"][len(stock_series)-1]-stock_series["Adj Close"][0])/stock_series["Adj Close"][0]
stock_series=current_stock['2015-12-31':'2016-12-31']
return_2016 = (stock_series["Adj Close"][len(stock_series)-1]-stock_series["Adj Close"][0])/stock_series["Adj Close"][0]

#current_stock[current_stock['Date'].str.contains("2011-")]
# = (current_stock["Adj Close"][len(current_stock)-1]-current_stock["Adj Close"][0])/current_stock["Adj Close"][0]