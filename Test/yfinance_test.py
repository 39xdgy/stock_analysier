import yfinance as yf
import stockstats

data = yf.download(tickers = 'AAPL', period = '1d', interval = '5m')

info_list = ['kdjk', 'kdjd', 'kdjj']

stockStat = stockstats.StockDataFrame.retype(data)
for info in info_list:
    data[info] = stockStat[[info]]


print(data.shape)