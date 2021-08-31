f = open('all_stock_output.txt', 'r')

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

#print(len(stock_info))
#print(stock_info.keys())

sorted_list = []
sort_key = 'fail_chance'


for stock_name in stock_info.keys():
    compare_data = stock_info[stock_name][sort_key]
    #print(stock_name)
    if(len(sorted_list) == 0):
        sorted_list.append(stock_info[stock_name])
    elif(len(sorted_list) == 1):
        if(sorted_list[0][sort_key] < compare_data):
            sorted_list.append(stock_info[stock_name])
        else:
            sorted_list = [stock_info[stock_name]] + sorted_list
    elif(sorted_list[0][sort_key] >= compare_data):
        sorted_list = [stock_info[stock_name]] + sorted_list
    elif(sorted_list[-1][sort_key] <= compare_data):
        sorted_list.append(stock_info[stock_name])
    else:
        start = 0
        end = len(sorted_list)
        mid = len(sorted_list) // 2
        while start > end:
            #print(f'{start} {end} {mid}')
            #print(f'{sorted_list[start][sort_key]} {sorted_list[end][sort_key]} {sorted_list[mid][sort_key]}')
            if sorted_list[mid][sort_key] >= compare_data:
                end = mid - 1
            else:
                start = mid
            mid = (end - start) // 2 + start
        mid += 1
        sorted_list = sorted_list[:mid] + [stock_info[stock_name]] + sorted_list[mid:]

#print(sorted_list)
for stock in sorted_list:
    print(stock[sort_key])