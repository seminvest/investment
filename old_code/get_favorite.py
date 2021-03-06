import pandas as pd
import pandas.io.data as web 
import numpy as np
import datetime; import csv; import os; import urllib; import re; 


nasdaq_100_stocks = []


start = datetime.datetime(2012,12,31)
end = datetime.datetime(2016,12,30)
current_stock = web.DataReader('SPY', "yahoo", start, end)
benchmark_return_spy = (current_stock["Adj Close"][len(current_stock)-1]-current_stock["Adj Close"][0])/current_stock["Adj Close"][0]

start = datetime.datetime(2012,12,31)
end = datetime.datetime(2016,12,30)
current_stock = web.DataReader('QQQ', "yahoo", start, end)
benchmark_return_qqq = (current_stock["Adj Close"][len(current_stock)-1]-current_stock["Adj Close"][0])/current_stock["Adj Close"][0]


return_list_vs_qqq = []
return_list_vs_spy = []
return_list = []
nasdaq_return_dict = {}
relative_return_dict = {}
nasdaq_100_stocks = ['AAPL', 'FB', 'GOOGL', 'AMZN', 'NFLX', 'V', 'NVDA', 'PCLN', 'MA', 'BIDU', 'NTES', 'EDU', 'CTRP', 'AVGO','CRM','NKE','HD','DIS', 'QQQ', 'SPY']
#for nasdaq_stock in ['AAPL', 'ADI']:
for nasdaq_stock in nasdaq_100_stocks:
#for nasdaq_stock in ['AAPL', 'FB', 'GOOGL', 'AMZN','NFLX','V','NVDA','PCLN']:	
	#a = nasdaq_stock
	#print(nasdaq_stock) 
	start = datetime.datetime(2012,12,31)
	end = datetime.datetime(2016,12,30)
	current_stock = web.DataReader(nasdaq_stock, "yahoo", start, end)
	current_return = (current_stock["Adj Close"][len(current_stock)-1]-current_stock["Adj Close"][0])/current_stock["Adj Close"][0]
	return_vs_qqq = current_return-benchmark_return_qqq
	return_vs_spy = current_return-benchmark_return_spy
	#print(return_vs_qqq)
	return_list_vs_qqq.append(return_vs_qqq)
	return_list_vs_spy.append(return_vs_spy)
	return_list.append(current_return)


	#mylist.append(current_stock)
#Form a nasdaq stock dictionary	


for i in range(len(nasdaq_100_stocks)):
    nasdaq_return_dict[nasdaq_100_stocks[i]] = return_list[i]
    relative_return_dict[nasdaq_100_stocks[i]] = (return_list_vs_qqq[i], return_list_vs_spy[i])

#sort the dictionary value in descending order
for key, value in sorted(nasdaq_return_dict.iteritems(), key=lambda (k,v): (v,k), reverse=True):
    print "%s: %s" % (key, value)


with open('favorite_stock_return.csv', 'w') as f:
    [f.write('{0},{1}\n'.format(key, value)) for key, value in nasdaq_return_dict.items()]


#df = pd.DataFrame(mylist, columns=["colummn"])
#df.to_csv('list.csv', index=False)
#print(nasdaq_return_list)

#Form different portfolio




