import datetime as dt
import sys
import pandas

import ftplib
import os
import re

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



#print(gt.get_tickers(NYSE = False, NASDAQ = True, AMEX = True))
print(len(test_tickers))
sys.path.append('../Class/')
from stock_data import stock_data

start = dt.datetime.now() - dt.timedelta(days = 365*3)
start = start.strftime('%Y-%m-%d')
today = dt.datetime.today().strftime('%Y-%m-%d')
#print(start)
stock_info = ['kdjj']#['macd', 'macds', 'macdh', 'kdjk', 'kdjd', 'kdjj', 'rsi_6', 'rsi_12', 'rsi_14']

write_info = f'Top 20 \n\n'
total_outcome = 0
fail_list = []
csv_list = pandas.read_csv('../Data/nasdaq_screener.csv')
all_stock_list = csv_list[csv_list.columns[0]]
start_time = dt.datetime.now()

set_tickers = ["SV", "ORC", "CRF", "MIC", "CLBS", "LYG", "NTB", "FTK", "GERN", "ADMS", "ETY", "SRGA"]

for each_stock in set_tickers:
    if '^' in each_stock or '/' in each_stock: continue
    try:
        stock = stock_data(stock_name=each_stock, period = '7d')

        stock.get_stats_info(stock_info)

        #print(stock.get_stock_data())
        
        stock.set_buy_flag({"kdjj": 15})
        stock.set_sell_flag({"kdjj": 85})
        time_diff = 0
        time_sum = 0
        time_tracker = [-1, -1]
        base_value = 10000
        stock_num = 0
        flag = True

        sell_flag = False

        buy_value = 0

        trade_count = 0
        fail_count = 0
        value_record = 10000
        temp_price = 0.0
        for index, row in stock.get_stock_data().iterrows():
            #print(row['macdh'])
            diff = row['kdjk'] - row['kdjd']
            
            if flag:
                if row['kdjj'] < 15:
                    #print(row['kdjj'])
                    sell_flag = True
                    trade_count += 0.5
                    flag = False
                    time_diff += 1

                    temp_price = row['close']
                    stock_num = base_value // row['close']
                    base_value -= stock_num * row['close']
                    #print(f'{each_stock} buying with {stock_num} of stocks. Orgin value is {base_value}.\n')

            elif sell_flag:
                if row['kdjj'] > 85:# or (row['close'] - temp_price) / temp_price >= 0.02:
                    #(row['kdjj'])
                    #print((row['close'] - temp_price) / temp_price)
                    trade_count += 0.5
                    flag = True
                    sell_flag = False

                    if time_tracker[0] == -1:
                        time_tracker[0] = time_diff
                        time_tracker[1] = time_diff

                    if time_diff < time_tracker[0]: time_tracker[0] = time_diff
                    if time_diff > time_tracker[1]: time_tracker[1] = time_diff

                    time_sum += time_diff
                    time_diff = 0
                    base_value += stock_num * row['close']
                    #print(base_value)
                    stock_num = 0
                    if value_record > base_value: fail_count += 1
                    value_record = base_value
                    #print(f'{each_stock} selling.value is {base_value}.\n')
                else:
                    time_diff += 1

        if stock_num != 0:
            #print("BRO")
            base_value += stock.get_current_price() * stock_num

        '''
        if fail_count / trade_count <= 0.25 and trade_count >= 15 and base_value > 10150:
            write_info += f'{each_stock} \t 10000 -> {base_value}\n'
            write_info += f'{trade_count} \t {fail_count / trade_count}% of fail\n'
            write_info += f'{time_sum / trade_count} \t {str(time_tracker)}\n\n'
        '''
        total_outcome += base_value
        
        print(f'{each_stock} is finished. here is the output!')
        print(f'\t Outcome: {base_value}')
        print(f'\t Trade number: {trade_count}')
        print(f'\t Fail%: {fail_count / trade_count}')
        print(f'\t Avg time: {time_sum / trade_count}')
        #print(time_tracker)
        
    except:
        #print(each_stock)
        fail_list.append(each_stock)
'''
f = open("../data/all_stock_1m_output.txt", "w")
f.write(write_info)
f.close()
'''

print("fail_list here")
print(fail_list)
print(f'Start at: {start_time}')
print(f'End at: {dt.datetime.now()}')

