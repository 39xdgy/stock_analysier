import ftplib
import os
import re
import yfinance as yf
'''
# Connect to ftp.nasdaqtrader.com
ftp = ftplib.FTP('ftp.nasdaqtrader.com', 'anonymous', 'anonymous@debian.org')
 
# Download files nasdaqlisted.txt and otherlisted.txt from ftp.nasdaqtrader.com
for ficheiro in ["nasdaqlisted.txt", "otherlisted.txt"]:
        ftp.cwd("/SymbolDirectory")
        localfile = open(ficheiro, 'wb')
        ftp.retrbinary('RETR ' + ficheiro, localfile.write)
        localfile.close()
ftp.quit()
 
# Grep for common stock in nasdaqlisted.txt and otherlisted.txt
for ficheiro in ["nasdaqlisted.txt", "otherlisted.txt"]:
        localfile = open(ficheiro, 'r')
        for line in localfile:
                if re.search("Common Stock", line):
                        ticker = line.split("|")[0]
                        # Append tickers to file tickers.txt
                        open("tickers.txt","a+").write(ticker + "\n")
'''

tickers = ''
with open('tickers.txt', 'r') as f:
    tickers = f.read()

tickers = tickers.split('\n')[:-1]
print(len(tickers))


nasdaq_list = []

lines = []
with open('nasdaqlisted.txt', 'r') as f:
    lines = f.readlines()

for each_line in lines:
    ticker = each_line.split('|')[0]
    if ('File Creation Time' not in ticker) and ('Symbol' not in ticker):
        nasdaq_list.append(ticker)
        if ticker not in tickers:
            tickers.append(ticker)

print(len(tickers))

lines = []
other_list = []

with open('otherlisted.txt', 'r') as f:
    lines = f.readlines()

for each_line in lines:
    ticker = each_line.split('|')[0]
    if ('File Creation Time' not in ticker) and ('Symbol' not in ticker) and ("$" not in ticker and "." not in ticker):
        other_list.append(ticker)
        if ticker not in tickers:
            tickers.append(ticker)


print(len(tickers))
'''
for each_ticker in other_list:
    _ = yf.download(each_ticker)
'''