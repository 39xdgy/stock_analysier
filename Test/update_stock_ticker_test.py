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
            '''
            if re.search("Common Stock", line):
                ticker = line.split("|")[0]
                # Append tickers to file tickers.txt
                open("../Data/tickers.txt","a+").write(ticker + "\n")
            '''


print(len(test_tickers))
'''
tickers = ''
with open('../Data/tickers.txt', 'r') as f:
    tickers = f.read()

tickers = tickers.split('\n')[:-1]


tickers = [each_ticker for each_ticker in tickers if ('.' not in each_ticker)]
print(len(tickers))
nasdaq_list = []

lines = []
with open('../Data/nasdaqlisted.txt', 'r') as f:
    lines = f.readlines()
    #print(len(lines))

for each_line in lines:
    ticker = each_line.split('|')[0]
    if 'File Creation Time' not in ticker and 'Symbol' not in ticker and "$" not in ticker and "." not in ticker:
        nasdaq_list.append(ticker)
        if ticker not in tickers:
            tickers.append(ticker)

print(len(tickers))

lines = []
other_list = []

with open('../Data/otherlisted.txt', 'r') as f:
    lines = f.readlines()
    #print(len(lines))

for each_line in lines:
    ticker = each_line.split('|')[0]
    if 'File Creation Time' not in ticker and 'Symbol' not in ticker and "$" not in ticker and "." not in ticker:
        other_list.append(ticker)
        if ticker not in tickers:
            tickers.append(ticker)


print(len(tickers))

#all_tickers_str = ' '.join(tickers)

test_read_all = yf.download(all_tickers_str)
print(test_read_all)



for ticker in tickers:
    if ticker not in test_tickers:
        print(ticker)
'''