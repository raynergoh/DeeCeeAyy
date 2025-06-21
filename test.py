from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.timeseries import TimeSeries

API_KEY ='DU9CW9ZHWOPF3POH'

ts =TimeSeries(key = API_KEY,)

fd = FundamentalData(key = API_KEY, output_format = 'pandas')

data = fd.get_company_overview(symbol = "AAPL")

print(data[0].T)