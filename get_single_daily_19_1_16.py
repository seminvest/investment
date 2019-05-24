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




if __name__ == "__main__":
    symbols = ['FB']
    sizeoption = 'full'
    API_URL = "https://www.alphavantage.co/query" 
    for symbol in symbols:
        stock_daily=get_stock_daily(symbol,sizeoption)
        df= get_stock_time_frame(symbol,'2017-12-29','2019-01-14')
        plot_data(df.loc['2017-12-29':'2019-01-14','adjusted close'],title="FB")

def get_stock_time_frame(symbol, start_date, end_date):
    dates=pd.date_range(start_date,end_date)
    df1=pd.DataFrame(index=dates)
    print(symbol,"start")
    df_temp=pd.read_csv("{}.csv".format(symbol),index_col="date",parse_dates=True,na_values=['nan'])
    df1=df1.join(df_temp,how='inner')
    print(symbol,"finish")
    df1.to_csv('tmp.csv')
    return df1

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
    ax = df.plot(title=title, fontsize=12, marker=cut_star, markersize=15)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()

def plot_data_special(df, title="Stock prices"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    star = mpath.Path.unit_regular_star(6)
    circle = mpath.Path.unit_circle()
    # concatenate the circle with an internal cutout of the star
    verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
    codes = np.concatenate([circle.codes, star.codes])
    cut_star = mpath.Path(verts, codes)
    ax = df.plot(title=title, fontsize=40,marker=cut_star, markersize=15)
    #figure(num=None, figsize=(80, 60), dpi=80, facecolor='w', edgecolor='k')
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(80, 60)
    fig.savefig('test2png.png', dpi=80)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()
    

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


star = mpath.Path.unit_regular_star(6)
circle = mpath.Path.unit_circle()
    # concatenate the circle with an internal cutout of the star
verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
codes = np.concatenate([circle.codes, star.codes])
cut_star = mpath.Path(verts, codes)
ax = df.plot(title=title, fontsize=40,marker=cut_star, markersize=15)
    #figure(num=None, figsize=(80, 60), dpi=80, facecolor='w', edgecolor='k')
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(80, 60)
fig.savefig('test2png.png', dpi=80)
ax.set_xlabel("Date")
ax.set_ylabel("Price")
plt.show()
ax.annotate('Q4,2017 earning',
             (df1.index[df1==df1.loc['2018-01-31']], df1.loc['2018-01-31']),
             xytext=(20, 20), 
             textcoords='offset points',
             arrowprops=dict(arrowstyle='-|>'),fontsize=60)
ax.annotate('Q1,2018 earning',
             (df1.index[df1==df1.loc['2018-04-25']], df1.loc['2018-04-25']),
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
ax.annotate('Q1,2018 earning',
             xy=(10, 20), fontsize=60)