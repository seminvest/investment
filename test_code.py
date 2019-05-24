
import pandas as pd

def test_run():
	start_date ='2018-08-14'
	end_date='2019-01-07'
	dates=pd.date_range(start_date,end_date)
	#print(dates[0])
	df1=pd.DataFrame(index=dates)
	symbols = ['TSLA','FB','AAPL']
	for symbol in symbols:
		df_temp=pd.read_csv("{}.csv".format(symbol),index_col="date",parse_dates=True,usecols=['date','adjusted close'],na_values=['nan'])
		df_temp = df_temp.rename(columns={"adjusted close":symbol})
		df1=df1.join(df_temp,how='inner')
	print(df1)

    dfTSLA = pd.read_csv("./data/TSLA.csv", index_col="date",parse_dates=True,usecols=['date','adjusted close'],na_values=['nan'])
    #df1=df1.join(dfTSLA,how='inner')
    #df1=df1.dropna()

if __name__ == "__main__":
	test_run()