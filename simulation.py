from stock_data import stock_data
import datetime as dt
from get_all_tickers import get_tickers as gt
import pandas
#print(gt.get_tickers(NYSE = False, NASDAQ = True, AMEX = True))

start = dt.datetime.now() - dt.timedelta(days = 365*3)
start = start.strftime('%Y-%m-%d')
today = dt.datetime.today().strftime('%Y-%m-%d')
#print(start)
stock_info = ['macd', 'macds', 'macdh', 'kdjk', 'kdjd', 'kdjj', 'rsi_6', 'rsi_12', 'rsi_14']

stock_list = ["AAPL", "SBUX", "ZM", "TWTR", "GME", "DIS", "V"]
write_info = ''

fail_list = []
csv_list = pandas.read_csv('nasdaq_screener.csv')
all_stock_list = csv_list[csv_list.columns[0]]
print(all_stock_list)
for each_stock in all_stock_list:
    try:
        stock = stock_data(stock_name=each_stock, start_date= start, end_date= today)

        stock.read_stock_from_yahoo()
        stock.get_stats_info(stock_info)

        #print(stock.get_stock_data())

        stock.set_buy_flag({"macdh": None})
        stock.set_sell_flag({"macdh": None})

        base_value = 10000
        stock_num = 0
        flag = True

        trade_count = 0
        fail_count = 0
        value_record = 10000

        for index, row in stock.get_stock_data().iterrows():
            #print(row['macdh'])
            diff = row['kdjk'] - row['kdjd']
            if row['macdh'] > 0 and flag:
                trade_count += 0.5
                flag = False
                stock_num = base_value // row['close']
                base_value -= stock_num * row['close']
                #print(f'{each_stock} buying with {stock_num} of stocks. Orgin value is {base_value}.\n')
            
            if row['macdh'] < 0 and not flag:
                trade_count += 0.5
                flag = True
                base_value += stock_num * row['close']
                stock_num = 0
                if value_record > base_value: fail_count += 1
                value_record = base_value
                #print(f'{each_stock} selling.value is {base_value}.\n')
        
        if stock_num != 0:
            #print("BRO")
            base_value += stock.get_stock_data().iloc[-1]["close"] * stock_num


        if fail_count / trade_count < 0.3 and trade_count >= 10:
            write_info += f'{each_stock} is finished. here is the output!\n'
            write_info += str(base_value) + '\n'
            write_info += str(trade_count) + '\n'
            write_info += str(fail_count / trade_count) + '\n'

            #print(f'{each_stock} is finished. here is the output!')
            #print(base_value)
            #print(trade_count)
            #print(fail_count / trade_count)
    except:
        fail_list.append(each_stock)

f = open("all_stock_output.txt", "w")
f.write(write_info)
f.close()


print("fail_list here")
print(fail_list)

