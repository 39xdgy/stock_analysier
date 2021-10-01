import datetime as dt
import sys
import pandas

sys.path.append('../Class/')
from stock_data import stock_data


stock_info = ['kdjj']#['macd', 'macds', 'macdh', 'kdjk', 'kdjd', 'kdjj', 'rsi_6', 'rsi_12', 'rsi_14']

write_info = f'Top 20 \n\n'
success_list = []
csv_list = pandas.read_csv('../Data/nasdaq_screener.csv')
all_stock_list = csv_list[csv_list.columns[0]]
pass_stock = {}

for each_stock in all_stock_list:
    if '^' in each_stock or '/' in each_stock: continue
    try:
        stock = stock_data(stock_name=each_stock, period = '1d')

        stock.get_stats_info(stock_info)
        
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
            diff = row['kdjk'] - row['kdjd']
            
            if flag:
                if row['kdjj'] < 15:
                    sell_flag = True
                    trade_count += 0.5
                    flag = False
                    time_diff += 1

                    temp_price = row['close']
                    stock_num = base_value // row['close']
                    base_value -= stock_num * row['close']

            elif sell_flag:
                if row['kdjj'] > 85 or (row['close'] - temp_price) / temp_price >= 0.02:
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
                    stock_num = 0
                    if value_record > base_value: fail_count += 1
                    value_record = base_value
                else:
                    time_diff += 1

        if stock_num != 0:
            base_value += stock.get_current_price() * stock_num


        if fail_count / trade_count <= 0.25 and trade_count >= 15 and base_value > 10150:
            pass_stock[each_stock] = {
                'name': each_stock,
                'final_value': base_value,
                'trade_count': trade_count,
                'fail_chance': fail_count / trade_count,
                'avg_day': time_sum / trade_count,
                'short_mins': time_tracker[0]
                'long_mins': time_tracker[1]
            }
            '''
            write_info += f'{each_stock} \t 10000 -> {base_value}\n'
            write_info += f'{trade_count} \t {fail_count / trade_count}% of fail\n'
            write_info += f'{time_sum / trade_count} \t {str(time_tracker)}\n\n'
            '''
        
        total_outcome += base_value

        success_list.append(each_stock)
    except Exception as e:
        print(f'{each_stock} has error because of {e}')

'''
f = open("/../data/all_stock_5m_output.txt", "w")
f.write(write_info)
f.close()
'''

'''
f = open('../Data/all_stock_5m_output.txt', 'r')

pass_stock = {}
each_stock = {}

for line in f:
    info = line.split(" ")
    
    if "->" in line:
        #print(float(info[-1][:-1]))
        each_stock['name'] = info[0]
        each_stock['final_value'] = float(info[-1][:-1])
    if "%" in line:
        #print(info)
        each_stock['trade_count'] = float(info[0])
        each_stock['fail_chance'] = float(info[2][:-1])
    if "[" in line:
        #print(info[-1][:-1])
        each_stock['avg_day'] = float(info[0])
        each_stock['short_day'] = int(info[-2][1:-1])
        each_stock['long_day'] = int(info[-1][:-2])
        stock_info[each_stock['name']] = each_stock
        each_stock = {}

#print(len(stock_info))
#print(list(stock_info.keys())[0])
'''
sorted_list = [pass_stock[list(pass_stock.keys())[0]]]
sort_key = 'fail_chance'

for stock_name in list(pass_stock.keys())[1:]:
    last_val = sorted_list[-1][sort_key]
    check_val = pass_stock[stock_name][sort_key]
    if check_val > last_val:
        continue
    for i in range(0, len(sorted_list)):
        loop_val = sorted_list[i][sort_key]
        if loop_val > check_val:
            sorted_list = sorted_list[:i] + [pass_stock[stock_name]] + sorted_list[i:]
            break
    if len(sorted_list) > 10:
        sorted_list = sorted_list[:-1]

sorted_name = []

for stock in sorted_list:
    #print(stock)
    print(f'stock: {stock["name"]}\t count: {stock["trade_count"]}\t fail: {stock[sort_key]}\n')
    sorted_name = stock["name"]
    #print()

'''
f = open('../Data/top_20_output.txt', 'w')
f.write(str(sorted_list))
f.close()
'''