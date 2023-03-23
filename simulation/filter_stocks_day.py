import datetime as dt
import json
from stock_data_2m import stock_data

def filter_sort():
    with open('../Data/all_stock_2m_output.txt', 'r') as f:
        stock_info = {}
        each_stock = {}

        for line in f:
            info = line.split(" ")

            if "->" in line:
                each_stock['name'] = info[0]
                each_stock['final_value'] = float(info[-1][:-1])
            if "%" in line:
                each_stock['trade_count'] = float(info[0])
                each_stock['fail_chance'] = float(info[2][:-1])
            if "[" in line:
                each_stock['avg_time_period'] = float(info[0])
                each_stock['shortest_time_period'] = int(info[-2][1:-1])
                each_stock['longest_time_period'] = int(info[-1][:-2])
                stock_info[each_stock['name']] = each_stock
                each_stock = {}

    sorted_list = sorted(stock_info.values(), key=lambda x: (x['fail_chance'], -x['final_value']))[:10]

    #for stock in sorted_list:
        #print(f'stock: {stock["name"]}\t count: {stock["trade_count"]}\t fail: {stock["fail_chance"]}\n')

    with open('../Data/top_10_output.json', 'w') as f:
        json.dump(sorted_list, f)
    
def run_filter(start, end, each_stock):
    #--------------------------------Change filter--------------------------------
    stock_info = ['kdjj']   #['macd', 'macds', 'macdh', 'kdjk', 'kdjd', 'kdjj', 'rsi_6', 'rsi_12', 'rsi_14']

    write_info = ""
    total_outcome = 0
    fail_list = []

    try:
        ####### ---------------------change param here----------------------------#############
        # pandas datetime to unix timestamp
        start = start.value//10**9
        end = end.value//10**9
        stock = stock_data(stock_name=each_stock, start = start, end = end)
        stock.get_stats_info(stock_info)

        #print(stock.get_stock_data())
        indicator_low = 5
        indicator_high = 95

        macd_low = 5
        macd_high = 95

        stock.set_buy_flag({"kdjj": indicator_low})
        stock.set_sell_flag({"kdjj": indicator_high})
        # stock.set_buy_flag({"macd": macd_low})
        # stock.set_sell_flag({"macd": macd_high})

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
          
            if flag:
                if row['kdjj'] < indicator_low:
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
                if row['kdjj'] > indicator_high:# or (row['close'] - temp_price) / temp_price >= 0.02:
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
            base_value += stock.get_current_price() * stock_num

        ## within 1 day
        if fail_count / trade_count <= 0.25 and trade_count >= 5 and base_value > 10150:
        ## 1 day interval
        # if fail_count / trade_count <= 0.25 and base_value > 11000:
            write_info += f'{each_stock} \t 10000 -> {base_value}\n'
            write_info += f'{trade_count} \t {fail_count / trade_count}% of fail\n'
            write_info += f'{time_sum / trade_count} \t {str(time_tracker)}\n\n'
        
        total_outcome += base_value
                
        # print(f'{each_stock} is finished. here is the output!')
        # print(f'\t Outcome: {base_value}')
        # print(f'\t Trade number: {trade_count}')
        # print(f'\t Fail%: {fail_count / trade_count}')
        # print(f'\t Avg time: {time_sum / trade_count}')
        # print(time_tracker)
        
    except Exception as e:
        #print(each_stock)
        
        fail_list.append(each_stock)
    return write_info
    
def run_analyze(start, end, each_stock):
    stock_info = ['kdjj']   #['macd', 'macds', 'macdh', 'kdjk', 'kdjd', 'kdjj', 'rsi_6', 'rsi_12', 'rsi_14']

    write_info = ""
    total_outcome = 0
    fail_list = []
    start_time = dt.datetime.now()
    try:

        #######          change param here         #############
        # pandas datetime to unix timestamp
        start = start.value//10**9
        end = end.value//10**9
        stock = stock_data(stock_name=each_stock, start = start, end = end)

        stock.get_stats_info(stock_info)

        #print(stock.get_stock_data())
        
        indicator_low = 5
        indicator_high = 95
        macd_low = 5
        macd_high = 95


        stock.set_buy_flag({"kdjj": indicator_low})
        stock.set_sell_flag({"kdjj": indicator_high})
        # stock.set_buy_flag({"macd": macd_low})
        # stock.set_sell_flag({"macd": macd_high})

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
          
            if flag:
                if row['kdjj'] < indicator_low:
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
                if row['kdjj'] > indicator_high:# or (row['close'] - temp_price) / temp_price >= 0.02:
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
            base_value += stock.get_current_price() * stock_num


        write_info += f'{each_stock} \t 10000 -> {base_value}\n'
        write_info += f'{trade_count} \t {fail_count / trade_count}% of fail\n'
        write_info += f'{time_sum / trade_count} \t {str(time_tracker)}\n\n'
        
        total_outcome += base_value
                
        # print(f'{each_stock} is finished. here is the output!')
        # print(f'\t Outcome: {base_value}')
        # print(f'\t Trade number: {trade_count}')
        # print(f'\t Fail%: {fail_count / trade_count}')
        # print(f'\t Avg time: {time_sum / trade_count}')
        # print(time_tracker)
        
    except:
        #print(each_stock)
        fail_list.append(each_stock)
    return {"info": write_info, "outcome": base_value}