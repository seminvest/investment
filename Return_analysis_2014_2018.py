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

end_date_2013='2012-12-31'
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
        #print(df1)
        df1.to_csv(start_date+'_'+end_date+'.csv')
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
#TWTR 2013-11-07
start_date1 = end_date_2013
end_date1= end_date_2016
data1=combine_stocks(symbols,start_date1,end_date1)
prices1 = data1.dropna()
risk_v1 = get_risk(prices1)
return_v1 = get_return(prices1)
sharp_v1=return_v1/risk_v1

start_date2 = end_date_2014
end_date2= end_date_2017
data2=combine_stocks(symbols,start_date2,end_date2)
prices2 = data2.dropna()
risk_v2 = get_risk(prices2)
return_v2 = get_return(prices2)
sharp_v2=return_v2/risk_v2

start_date3 = end_date_2015
end_date3= end_date_2018
data3=combine_stocks(symbols,start_date3,end_date3)
prices3 = data3.dropna()
risk_v3 = get_risk(prices3)
return_v3 = get_return(prices3)
sharp_v3=return_v3/risk_v3

#sharp_v1.tolist()
#return_v1.tolist()
return_3years = pd.DataFrame(
    {'symbol': symbols,
    'return_2014_2016': return_v1,
    'return_2015_2017': return_v2,
    'return_2016_2018': return_v3,        
    })
return_3years.sort_values('return_2014_2016')
print(return_3years.sort_values('return_2014_2016',ascending=0))

