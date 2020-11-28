import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time

apiKey = 'VLG4S2J38MECAW2U'

ts = TimeSeries(key="apiKey", output_format='pandas')
data, meta_data = ts.get_daily(symbol='AAPL', outputsize='full')
print(data)

'''get S&P500'''
#spData = ts.get_daily(symbol='SPX', outputsize='compact')
#print(spData)

closeData = data['4. close']
print(closeData)
percentChange = closeData.pct_change()
print(percentChange[-1])
