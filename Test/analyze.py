f = open('../Data/all_stock_5m_output.txt', 'r')

stock_info = {}
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

sorted_list = [stock_info[list(stock_info.keys())[0]]]
sort_key = 'fail_chance'

for stock_name in list(stock_info.keys())[1:]:
    last_val = sorted_list[-1][sort_key]
    check_val = stock_info[stock_name][sort_key]
    if check_val > last_val:
        continue
    for i in range(0, len(sorted_list)):
        loop_val = sorted_list[i][sort_key]
        if loop_val > check_val:
            sorted_list = sorted_list[:i] + [stock_info[stock_name]] + sorted_list[i:]
            break
    if len(sorted_list) > 10:
        sorted_list = sorted_list[:-1]

sorted_name = []
for stock in sorted_list:
    print(f'stock: {stock["name"]}\t count: {stock["trade_count"]}\t fail: {stock[sort_key]}\n')


f = open('top_20_output.txt', 'w')
f.write(str(sorted_list))
f.close()