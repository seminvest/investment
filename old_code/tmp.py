import pandas as pd

import numpy as np

year_list=[]

month_list=[]

rtn_list=[]

return_list = []

start = datetime.datetime(2012,12,31)
end = datetime.datetime(2016,12,30)
current_stock = web.DataReader('QQQ', "yahoo", start, end)
benchmark_return_qqq = (current_stock["Adj Close"][len(current_stock)-1]-current_stock["Adj Close"][0])/current_stock["Adj Close"][0]
#df = pd.DataFrame(current_stock, columns=["colummn"])
current_stock.to_csv('list.csv', index=True)
return1= (current_stock["Adj Close"][125]-current_stock["Adj Close"][0])/current_stock["Adj Close"][0]
return_list.append(return1)
return1= (current_stock["Adj Close"][252]-current_stock["Adj Close"][125])/current_stock["Adj Close"][125]
return_list.append(return1)
return1= (current_stock["Adj Close"][376]-current_stock["Adj Close"][252])/current_stock["Adj Close"][252]

for year in range(2013,2016):
    for month in [6,12]:
        year_list.append(year)
        month_list.append(month)
        rtn=round((-1)**(month/6)*(month/6/10),3)+(np.random.random()-0.5)*0.1
        rtn_list.append(rtn)
df=pd.DataFrame()
df['year']=year_list
df['month']=month_list

df_year=df.groupby(['year']).sum()
del df_year['month']
# investment