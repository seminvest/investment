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

end_date_2013='2013-12-31'
end_date_2014='2014-12-31'
end_date_2015='2015-12-31'
end_date_2016='2016-12-30'
end_date_2017='2017-12-29'
end_date_2018='2018-12-31'

def combine_stocks(symbols,start_date,end_date):
        dates=pd.date_range(start_date,end_date)
	#print(dates[0])
        df1=pd.DataFrame(index=dates)
        for symbol in symbols:
                print(symbol,"start")
                root = '/Users/ruitang/Dropbox/Program/Stock_Analysis'
                day = 'daily_data'
                subdir = os.path.join(root, day,symbol + '.csv')
                df_temp=pd.read_csv(subdir,index_col="date",parse_dates=True,usecols=['date','adjusted close'],na_values=['nan'])
                df_temp = df_temp.rename(columns={"adjusted close":symbol})
                df1=df1.join(df_temp,how='inner')
                #df1=df1.join(df_temp)
                print(symbol,"finish")
        print(df1)
        df1.to_csv('Bei_IRA.csv')
        return df1
def get_risk(prices):
    return (prices / prices.shift(1) - 1).dropna().std().values

def get_return(prices):
    return ((prices / prices.shift(1) - 1).dropna().mean() * np.sqrt(252)).values

#symbols = ['TSLA','FB','BABA','AMZN']
symbols = ['TSLA','AAPL','AMZN','GOOGL','FB','TWTR','MSFT','CRM','NOW','WDAY','ADBE','INTU','ANSS','SNPS','CDNS',
    'ADSK','MA','V','AXP','DFS','CME','COST','MORN','ILMN','ISRG','HD','LRCX','AMAT','XLNX','NVDA','AMD',
    'AVGO','MU','OLED','XBI','QQQ','MTN','NTES','TRIP','NFLX','DIS','ATVI','EA']
#ZEN 2014-05-15
#NEWR 2014-12-12
#HUBS 2014-10-09
#SQ 2015-11-19
#JD 2014-05-22
#BABA 2014-09-19
#PYPL 2015-07-20
start_date = end_date_2015
end_date= end_date_2018
BeiIRA_data=combine_stocks(symbols,start_date,end_date)
prices = BeiIRA_data.dropna()
risk_v = get_risk(prices)
return_v = get_return(prices)
sharp_v=return_v/risk_v
fig, ax = plt.subplots()
fig = matplotlib.pyplot.gcf()
ax.scatter(x=risk_v, y=return_v, alpha=0.5)
ax.set(title='Return and Risk', xlabel='Risk', ylabel='Return')
for i, symbol in enumerate(symbols):
    ax.annotate(symbol, (risk_v[i], return_v[i]))
#plt.show()
fig.savefig('test2png.png', dpi=300)

sharp_v.tolist()
return_v.tolist()
sharp_3years = pd.DataFrame(
    {'symbol': symbols,
    'return': return_v,
     'sharp ratio': sharp_v
    })
sharp_3years.sort_values('return')
print(sharp_3years.sort_values('return',ascending=0))


