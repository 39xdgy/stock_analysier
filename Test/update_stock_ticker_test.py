import ftplib
import os
import re
import yfinance as yf

# Connect to ftp.nasdaqtrader.com
ftp = ftplib.FTP('ftp.nasdaqtrader.com', 'anonymous', 'anonymous@debian.org')
 
# Download files nasdaqlisted.txt and otherlisted.txt from ftp.nasdaqtrader.com
for ficheiro in ["nasdaqlisted.txt", "otherlisted.txt"]:
        ftp.cwd("/SymbolDirectory")
        localfile = open(f'../Data/{ficheiro}', 'wb')
        ftp.retrbinary('RETR ' + ficheiro, localfile.write)
        localfile.close()
ftp.quit()
 
# Grep for common stock in nasdaqlisted.txt and otherlisted.txt

test_tickers = []

for ficheiro in ["nasdaqlisted.txt", "otherlisted.txt"]:
        localfile = open(f'../Data/{ficheiro}', 'r')
        open("../Data/tickers.txt", "w")
        for line in localfile:
            #print(line)
            ticker = line.split("|")[0]
            if 'File Creation Time' not in ticker and 'Symbol' not in ticker and "$" not in ticker and "." not in ticker and ticker not in test_tickers:
                test_tickers.append(ticker)



print(len(test_tickers))

#print('SV' in test_tickers)


all_tickers_str = " ".join(test_tickers)
'''
test_read_all = yf.download(all_tickers_str)
print(test_read_all)
'''
import pandas
csv_list = pandas.read_csv('../Data/nasdaq_screener.csv')
all_stock_list = csv_list[csv_list.columns[0]]

diff_count = 0
diff_list = []
for each_ticker in all_stock_list:
        if each_ticker not in test_tickers and "^" not in each_ticker and '/' not in each_ticker and ' ' not in each_ticker:
                diff_count += 1
                diff_list.append(each_ticker)
print(f'There are {diff_count} of stocks in csv are not in test tickers')
#print(diff_list)
diff_real_stock = []
for each_ticker in diff_list:
        test_download = yf.download(tickers = each_ticker, period = '3d', interval = '1m')
        #print(len(test_download))
        if len(test_download) != 0:
                diff_real_stock.append(each_ticker)
print(diff_real_stock)
