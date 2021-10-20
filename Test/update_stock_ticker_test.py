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

all_tickers_str = " ".join(test_tickers)

test_read_all = yf.download(all_tickers_str)
print(test_read_all)


