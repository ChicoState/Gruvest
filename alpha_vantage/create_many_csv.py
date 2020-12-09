import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time

apiKey = 'VLG4S2J38MECAW2U'

stocks = ['AAPL','AMD','FB','GOOGL','AMZN','ATVI','MSFT','PYPL','EBAY','AMAT','OSK','AZN','SLV','IAU',
        'SVM','AG','EXK','AG','GLD','AAAU','BAR','SIVR','HON','NVDA','AJRD','LUV','LMT','NOC','ITA','ABT',
        'CCL','EL','CAT','VRM','CVNA','TSM','TSCO','SAP','IBM','AMC','COKE','PEP','F','GM','GE','FCX',
        'SNAP','TWTR','TSLA','NFLX','DIS','GPRO','SBUX','BAC','FIT','TTWO','EA','SNE','TROX','CRM','ROKU',
        'HPQ','MTW','TXT','RTX','ORCL','DHR','CVS','ADI','UBER','PINS','WORK','RAD','MAG','FSM','AWK','AWR',
        'YORW','MSEX','CWT','ROK','WING','CPRX','APHA','NRZ','PLUG','PTON','NKE','KO','V','MRNA','ZNGA','TXMD',
        'JNJ','WMT','NTDOY','DKNG','JPM','PENN','ET','DAL','SIRI','LYFT','NIO','OGI','PFE','ZM','KOS','GILD',
        'UAL','SAVE','BA','NCLH','BRK.B','INTC','T','JBLU','WFC','INO','RKT','CRON','CGC','BYND','MGM','AAL',
        'ACB','MFA','TLRY','XOM','HEXO','NKLA','PLTR','WKHS','FCEL','VOO','GNUS','IDEX','USO']

spy = ['SPY']

for ticker in spy:
    ts = TimeSeries(key="apiKey", output_format='pandas')
    data, meta_data = ts.get_daily(symbol=ticker, outputsize='compact')
    df = pd.DataFrame(data['4. close'])
    final = df.to_csv(ticker + '.csv', index=True)
    print(data)
    time.sleep(13)

