#https://stackoverflow.com/questions/48071949/how-to-use-the-alpha-vantage-api-directly-from-python
#https://www.profitaddaweb.com/2018/07/alpha-vantage-preprocessed-free-apis-in.html
import requests
import alpha_vantage
import json
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

API_URL = "https://www.alphavantage.co/query" 
symbols = ['TSLA','FB','AAPL']

for symbol in symbols:
        data = { "function": "TIME_SERIES_DAILY_ADJUSTED", 
        "symbol": symbol,
        "outputsize" : "compact",       
        "datatype": "json", 
        "apikey": "XXX" } 
        response = requests.get(API_URL, data) 
        data = response.json()
        #print(data);
        data=data['Time Series (Daily)'];
        df=pd.DataFrame(columns=['date','open','high','low','close','adjusted close','volume'])	
        for d,p in data.items():
        	date=datetime.datetime.strptime(d,'%Y-%m-%d')
        	data_row=[date,float(p['1. open']),float(p['2. high']),float(p['3. low']),float(p['4. close']), float(p['5. adjusted close']), int(p['6. volume'])]
        	df.loc[-1,:]=data_row
        	df.index=df.index+1
        data=df.sort_values('date')
        data.to_csv(symbol + '.csv', index=False)
#plt.savefig('myfilename.png')
#api_key=open('alpha.txt','r').read()
#data=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=1min&symbol=YESBANK&apikey={}'.format(api_key))