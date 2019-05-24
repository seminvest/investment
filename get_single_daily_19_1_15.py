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
import time
def get_stock_daily(symbol,sizeoption):
        data = { "function": "TIME_SERIES_DAILY_ADJUSTED", 
        "symbol": symbol,
        "outputsize" : sizeoption,       
        "datatype": "json", 
        "apikey": "AXTFJ8VGFWQ1PWZD" } 
        response = requests.get(API_URL, data) 
        data = response.json()
        print(symbol,"start")
        data=data['Time Series (Daily)'];
        df=pd.DataFrame(columns=['date','open','high','low','close','adjusted close','volume'])	
        for d,p in data.items():
        	date=datetime.datetime.strptime(d,'%Y-%m-%d')
        	data_row=[date,float(p['1. open']),float(p['2. high']),float(p['3. low']),float(p['4. close']), float(p['5. adjusted close']), int(p['6. volume'])]
        	df.loc[-1,:]=data_row
        	df.index=df.index+1
        data=df.sort_values('date')
        data.to_csv(symbol + '.csv', index=False)
        print(symbol,"finish")
        return data
symbols = ['FB']
sizeoption = 'full'
for symbol in symbols:
    stock_daily=get_stock_daily(symbol,sizeoption)

def combine_stocks(symbols):
	start_date ='2018-08-31'
	end_date='2019-01-14'
	dates=pd.date_range(start_date,end_date)
	#print(dates[0])
	df1=pd.DataFrame(index=dates)
	for symbol in symbols:
		print(symbol,"start")
		df_temp=pd.read_csv("{}.csv".format(symbol),index_col="date",parse_dates=True,usecols=['date','adjusted close'],na_values=['nan'])
		df_temp = df_temp.rename(columns={"adjusted close":symbol})
		df1=df1.join(df_temp,how='inner')
		print(symbol,"finish")
	print(df1)
	df1.to_csv('SAAS_100_daily.csv')
	return df1

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    # TODO: Your code here
    # Note: Returned DataFrame must have the same number of rows
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:]/df[:-1].values)-1
    daily_returns.iloc[0,:] = 0
    return daily_returns

def plot_data(df, title="Stock prices"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()

def plot_selected(df, columns, start_index, end_index):
    plot_data(df.iloc[start_index:end_index,columns],title="selected data")
    """Plot the desired columns over index values in the given range."""
    # TODO: Your code here
    # Note: DO NOT modify anything else!
    
    
API_URL = "https://www.alphavantage.co/query" 
symbols = ['CRM','NOW','WDAY','AYX','HUBS']
symbols2 = ['TWLO','DOCU','ADBE','OKTA','NEWR']
symbols3 = ['INTU','PLAN','DBX','ZS','ZEN']
for symbol in symbols:
	get_stock_daily(symbol)

time.sleep(60)

for symbol in symbols2:
	get_stock_daily(symbol)

time.sleep(60)

for symbol in symbols3:
	get_stock_daily(symbol)

symbols = ['CRM','NOW','WDAY','AYX','HUBS','TWLO','DOCU','ADBE','OKTA','NEWR','INTU','DBX','ZS','ZEN']
saas_data=combine_stocks(symbols)
#normalized to the first row
saas_data=saas_data/saas_data.iloc[0,:]
plot_data(saas_data)
plot_selected(saas_data, ['CRM', 'NOW'], '2018-08-31', '2019-01-14')
saas_data.loc[:,'CRM'].hist()
saas_data.plot(kind='scatter',x='CRM',y='NOW')
saas_daily_return=compute_daily_returns(saas_data)
saas_daily_return.plot(kind='scatter',x='CRM',y='NOW')
beta_NOW, alpha_NOW =np.polyfit(saas_daily_return['CRM'],saas_daily_return['NOW'],1)
plt.plot(saas_daily_return['CRM'],beta_NOW*saas_daily_return['CRM']+alpha_NOW,'-',color='r')
plt.show()
print(saas_daily_return.corr(method='pearson'))


#symbols = ['CRM','NOW']
#t1 = time.time()

#t2 = time.time()
#print (t2-t1)        
#plt.savefig('myfilename.png')
#api_key=open('alpha.txt','r').read()
#data=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=1min&symbol=YESBANK&apikey={}'.format(api_key))