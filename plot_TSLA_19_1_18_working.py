#https://stackoverflow.com/questions/48071949/how-to-use-the-alpha-vantage-api-directly-from-python
#https://www.profitaddaweb.com/2018/07/alpha-vantage-preprocessed-free-apis-in.html
import requests
import alpha_vantage
import json
import pandas as pd
import datetime
import numpy as np
import time
from mpl_finance import candlestick_ohlc
import matplotlib
import matplotlib.dates as mdates
import matplotlib.path as mpath
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib import style

def get_stock_time_frame(symbol, start_date, end_date):
    dates=pd.date_range(start_date,end_date)
    df1=pd.DataFrame(index=dates)
    print(symbol,"start")
    df_temp=pd.read_csv("{}.csv".format(symbol),index_col="date",parse_dates=True,na_values=['nan'])
    df1=df1.join(df_temp,how='inner')
    print(symbol,"finish")
    df1.to_csv('tmp.csv')
    return df1
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


if __name__ == "__main__":
    symbols = ['FB']
    sizeoption = 'full'
    API_URL = "https://www.alphavantage.co/query" 
    for symbol in symbols:
        stock_daily=get_stock_daily(symbol,sizeoption)
        df= get_stock_time_frame(symbol,'2017-12-29','2019-01-14')
        df1=df.loc['2017-12-29':'2019-01-14','adjusted close']
    star = mpath.Path.unit_regular_star(6)
    circle = mpath.Path.unit_circle()
    verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
    codes = np.concatenate([circle.codes, star.codes])
    cut_star = mpath.Path(verts, codes)
    ax = df1.plot(fontsize=40,marker=cut_star, markersize=15)
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start, end, 20))
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(80, 60)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.annotate('Q4,2017 earning',
             (df1.index[df1==df1.loc['2018-01-31']], df1.loc['2018-01-31']),
             xytext=(20, 20), 
             textcoords='offset points',
             arrowprops=dict(arrowstyle='-|>'),fontsize=60)
ax.annotate('Q1,2018 earning',
    #tmp workout around to solve the problem for two day same closing price
             (df1.index[df1==df1.loc['2018-04-26']], df1.loc['2018-04-25']),
             xytext=(20, 20), 
             textcoords='offset points',
             arrowprops=dict(arrowstyle='-|>'),fontsize=60)
ax.annotate('Q2,2018 earning',
             (df1.index[df1==df1.loc['2018-07-25']], df1.loc['2018-07-25']),
             xytext=(20, 20), 
             textcoords='offset points',
             arrowprops=dict(arrowstyle='-|>'),fontsize=60)
ax.annotate('Q3,2018 earning',
             (df1.index[df1==df1.loc['2018-10-30']], df1.loc['2018-10-30']),
             xytext=(20, 20), 
             textcoords='offset points',
             arrowprops=dict(arrowstyle='-|>'),fontsize=60)
fig.savefig('test2png.png', dpi=80)
#plt.show()