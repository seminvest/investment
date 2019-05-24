import pandas as pd
import pandas.io.data as web 
import numpy as np
import datetime; import csv; import os; import urllib; import re; 
from pandas_datareader.data import Options
tsla = Options('TSLA','yahoo')
data = tsla.get_all_data()
data.iloc[0:5, 0:5]

