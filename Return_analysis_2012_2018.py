#https://towardsdatascience.com/efficient-frontier-optimize-portfolio-with-scipy-57456428323e
#1/26/2019, this script is used to test SaaS company 2016-2019/1 performance
import requests
import alpha_vantage
import json
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import time
import os
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import time
import os
from scipy.optimize import minimize
import matplotlib
import matplotlib.dates as mdates
import matplotlib.path as mpath
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib import style

def combine_stocks(symbols,start_date,end_date):
        dates=pd.date_range(start_date,end_date)
	#print(dates[0])
        df1=pd.DataFrame(index=dates)
        for symbol in symbols:
                #print(symbol,"start")
                root = '/Users/ruitang/Dropbox/Program/Stock_Analysis'
                day = 'daily_data'
                subdir = os.path.join(root, day,symbol + '.csv')
                df_temp=pd.read_csv(subdir,index_col="date",parse_dates=True,usecols=['date','adjusted close'],na_values=['nan'])
                df_temp = df_temp.rename(columns={"adjusted close":symbol})
                df1=df1.join(df_temp,how='inner')
                #df1=df1.join(df_temp)
                #print(symbol,"finish")
        #print(df1)
        df1.to_csv(start_date+'_'+end_date+'.csv')
        return df1

#symbols = ['TSLA','FB','BABA','AMZN']
symbols = ['QQQ','TSLA','AAPL','AMZN','GOOGL','FB','MSFT','CRM','NOW','WDAY','ADBE','INTU','ANSS','SNPS','CDNS',
    'ADSK','MA','V','AXP','DFS','CME','COST','MORN','ILMN','ISRG','HD','LRCX','AMAT','XLNX','NVDA','AMD',
    'AVGO','MU','OLED','XBI','MTN','NTES','TRIP','NFLX','DIS','ATVI','EA']

#ZEN 2014-05-15
#NEWR 2014-12-12
#HUBS 2014-10-09
#SQ 2015-11-19
#JD 2014-05-22
#BABA 2014-09-19
#PYPL 2015-07-20
#TWTR 2013-11-07
date_point = ['2012-12-31','2013-12-31','2014-12-31','2015-12-31','2016-12-30','2017-12-29','2018-12-31']
df1=pd.DataFrame(index=symbols)
for i in range (0,len(date_point)-1):
    print(date_point[i],date_point[i+1])
    data1=combine_stocks(symbols,date_point[i],date_point[i+1])
    prices1 = data1.dropna()
    prices=pd.concat([prices1.head(1), prices1.tail(1)])
    returns = prices.pct_change().dropna()
    df1=df1.join(returns.T,how='inner')
print(df1)
tmp=df1 - df1.loc['QQQ'].values.squeeze()    
#sharp_v1.tolist()
#return_v1.tolist()
print(tmp)
#print(df1.sort_values('return_2014_2016',ascending=0))

