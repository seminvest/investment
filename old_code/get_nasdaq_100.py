import pandas as pd
import pandas.io.data as web 
import datetime

import csv
import os

#start = datetime.datetime(2015,12,31)
#end = datetime.date.today()
#apple = web.DataReader("AAPL", "yahoo", start, end)
#type(apple)
#apple.head()
nasdaq_100_stocks = []
import urllib; import re; 
#print line.split('\"')[1] for line in re.findall('\[\"[A-Z]+\",', urllib.urlopen('http://www.nasdaq.com/quotes/nasdaq-100-stocks.aspx').read())
#print sorted(line.split('\"')[1] for line in re.findall('\[\"[A-Z]+\",', urllib.urlopen('http://www.nasdaq.com/quotes/nasdaq-100-stocks.aspx').read()))
nasdaq_100_stocks = sorted(line.split('\"')[1] for line in re.findall('\[\"[A-Z]+\",', urllib.urlopen('http://www.nasdaq.com/quotes/nasdaq-100-stocks.aspx').read()))

#mylist = []
nasdaq_return_list = []
nasdaq_return_dict = {}
#for nasdaq_stock in ['AAPL', 'ADI']:
for nasdaq_stock in nasdaq_100_stocks:
#for nasdaq_stock in ['AAPL', 'FB', 'GOOGL', 'AMZN','NFLX','V','NVDA','PCLN']:	
	#a = nasdaq_stock
	#print(nasdaq_stock) 
	start = datetime.datetime(2015,12,31)
	end = datetime.date.today()
	current_stock = web.DataReader(nasdaq_stock, "yahoo", start, end)
	stock_return = (current_stock["Close"][len(current_stock)-1]-current_stock["Close"][0])/current_stock["Close"][0]
	nasdaq_return_list.append(stock_return)
	#mylist.append(current_stock)
#Form a nasdaq stock dictionary	
for i in range(len(nasdaq_100_stocks)):
    nasdaq_return_dict[nasdaq_100_stocks[i]] = nasdaq_return_list[i]

with open('stock_return.csv', 'w') as f:
    [f.write('{0},{1}\n'.format(key, value)) for key, value in nasdaq_return_dict.items()]


#df = pd.DataFrame(mylist, columns=["colummn"])
#df.to_csv('list.csv', index=False)
#print(nasdaq_return_list)

#Form different portfolio

