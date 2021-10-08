from webull import paper_webull, webull
from stock_data import stock_data
from trade import trade as td
from datetime import datetime

import os.path, json, pandas


class user:

    def __init__(self, json_path, stock_dic, is_pwb = True, data_range = ['3d', '1m']):
        self.stock_dic = stock_dic
        if not os.path.exists("../Data/back_up.json"):
            with open("../Data/back_up.json", "w") as f:
                json.dump(self.stock_dic, f)
        else: 
            with open("../Data/back_up.json", "r") as f:
                self.stock_dic = json.load(f)
        self.json_path = json_path
        self.is_pwb = is_pwb
        self.wb, self.pwb = webull(), paper_webull()
        self.stats_index, self.buy_flag, self.sell_flag, self.trade_counter = {}, {}, {}, {}
        self.trade_record = []
        self.data_range = data_range
        self.next_day_dic = {}

    # helper function to get stock data
    def _create_stock_info(self, stock_name):
        each_stock = stock_data(stock_name = stock_name, period = self.data_range[0], interval = self.data_range[1])
        each_stock.set_buy_flag(self.buy_flag)
        each_stock.set_sell_flag(self.sell_flag)
        each_stock.get_stats_info(self.stats_index)
        return each_stock

    # set up all the trading flags and indexs
    def set_trade_data(self, input_data):
        self.stats_index, self.buy_flag, self.sell_flag = input_data

    # update the stock list
    def update_stock_list(self):
        if len(self.next_day_dic.keys()) == 0:
            return
        for key in self.stock_dic:
            if key in self.next_day_dic:
                self.next_day_dic[key] = self.stock_dic[key]
            elif not self.stock_dic[key] == 0:
                if self.is_pwb: self.pwb.place_order(stock = key, action = "SELL", orderType = "LMT", enforce = "DAY", quant = self.stock_dic[key])
                else: self.wb.place_order(stock = key, action = "SELL", orderType = "LMT", enforce = "DAY", quant = self.stock_dic[key])

        self.stock_dic = self.next_day_dic
        with open("../Data/back_up.json", "w") as f:
                json.dump(self.stock_dic, f)

    def simulation_2_filter(self):
        csv_list = pandas.read_csv('../Data/nasdaq_screener.csv')
        all_stocks_ticker = csv_list[csv_list.columns[0]]
        success_list = []
        pass_stock = {}
        for ticker in all_stocks_ticker:
            if '^' in ticker or '/' in ticker: continue
            try:
                stock = stock_data(stock_name=ticker, period = '7d')
                stock.get_stats_info(['kdjj'])
                time_diff, time_sum, stock_num, base_value = 0, 0, 0, 10000
                time_tracker = [-1, -1]
                flag, sell_flag = True, False

                buy_value, trade_count, fail_count, value_record = 0, 0, 0, 10000
                temp_price = 0.0
                
                for index, row in stock.get_stock_data().iterrows():
                    
                    if flag and row['kdjj'] < 15:
                        
                        flag, sell_flag = False, True
                        trade_count += 0.5
                        time_diff += 1

                        temp_price = row['close']
                        stock_num = base_value // row['close']
                        base_value -= stock_num * row['close']
                    elif sell_flag:
                        if (row['kdjj'] > 85):
                            trade_count += 0.5
                            flag, sell_flag = True, False
                            
                            if time_tracker[0] == -1:
                                time_tracker[0] = time_diff
                                time_tracker[1] = time_diff

                            if time_diff < time_tracker[0]: time_tracker[0] = time_diff
                            if time_diff > time_tracker[1]: time_tracker[1] = time_diff

                            time_sum += time_diff
                            base_value += stock_num * row['close']
                            time_diff, stock_num = 0, 0
                            if value_record > base_value: fail_count += 1
                            value_record = base_value
                        else: time_diff += 1
                
                if stock_num != 0:
                    base_value += stock.get_current_price() * stock_num
                
                if fail_count / trade_count <= 0.2 and trade_count >= 35 and base_value > 10350:
                    pass_stock[ticker] = {
                        'name': ticker,
                        'final_value': base_value,
                        'trade_count': trade_count,
                        'fail_chance': fail_count / trade_count,
                        'avg_day': time_sum / trade_count,
                        'short_mins': time_tracker[0],
                        'long_mins': time_tracker[1]
                    }
                total_outcome += base_value

                success_list.append(ticker)
            except Exception as e:
                continue

        with open("../Data/success.json", "w") as f:
                json.dump(success_list, f)
        print(success_list)
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
        
        self.next_day_dic = {stock["name"]: 0 for stock in sorted_list}
        return self.next_day_dic
        
        '''
        for stock in sorted_list:
            #print(stock)
            print(f'stock: {stock["name"]}\t count: {stock["trade_count"]}\t fail: {stock[sort_key]}\n')
            sorted_name = stock["name"]
            #print()
        '''
        





    # trade with all the stocks under this user
    def trade(self):
        for key in self.stock_dic:
            try:
                value = self.stock_dic[key]
                each_stock = self._create_stock_info(key)
                should_buy = each_stock.should_buy()
                should_sell = each_stock.should_sell()
                quant = 10000 // each_stock.get_current_price()
                real_quant = 150 // each_stock.get_current_price()
                if value == 0 and should_buy['kdjj']:
                    new_td = td()
                    new_td.buy_update(name = key, start_time = str(datetime.now()), start_price = each_stock.get_current_price(), amount = quant)
                    self.trade_counter[key] = new_td
                    self.stock_dic[key] = quant
                    
                    if self.is_pwb: 
                        self.stock_dic[key] = quant
                        self.pwb.place_order(stock = key, action = "BUY", orderType = "MKT", enforce = "DAY", quant = quant)
                    else: 
                        self.stock_dic[key] = real_quant
                        self.wb.place_order(stock = key, action = "BUY", orderType = "MKT", enforce = "DAY", quant = real_quant)

                elif (not value == 0) and should_sell['kdjj']:
                    finished_td = self.trade_counter[key]
                    finished_td.sell_update(end_time = str(datetime.now()), end_price = each_stock.get_current_price())
                    self.trade_record.append(finished_td)
                    self.stock_dic[key] = 0
                    if self.is_pwb: self.pwb.place_order(stock = key, action = "SELL", orderType = "MKT", enforce = "DAY", quant = value)
                    else: self.wb.place_order(stock = key, action = "SELL", orderType = "MKT", enforce = "DAY", quant = value)
            except Exception as E:
                print(E)
        with open("../Data/back_up.json", 'w') as f:
            json.dump(self.stock_dic, f)

    # write into a file with all the records
    def write_trade_record(self):
        f = open("../Data/trade_record.txt", "a")
        write_str = ''
        for record in self.trade_record:
            write_str += str(record)
            write_str += "\n\n"

        f.write(write_str)
        f.close()

    # login to the webull real account
    def login_wb(self):
        fh = open(self.json_path, 'r')
        credential_data = json.load(fh)
        fh.close()

        self.wb._refresh_token = credential_data['refreshToken']
        self.wb._access_token = credential_data['accessToken']
        self.wb._token_expire = credential_data['tokenExpireTime']
        self.wb._uuid = credential_data['uuid']

        n_data = self.wb.refresh_login()
        #print(n_data)
        credential_data['refreshToken'] = n_data['refreshToken']
        credential_data['accessToken'] = n_data['accessToken']
        credential_data['tokenExpireTime'] = n_data['tokenExpireTime']

        file = open(self.json_path, 'w')
        json.dump(credential_data, file)
        file.close()

        # important to get the account_id
        return self.wb.get_account_id()

    # login to the webull paper trading account
    def login_pwb(self):
        fh = open(self.json_path, 'r')
        credential_data = json.load(fh)
        fh.close()

        self.pwb._refresh_token = credential_data['refreshToken']
        self.pwb._access_token = credential_data['accessToken']
        self.pwb._token_expire = credential_data['tokenExpireTime']
        self.pwb._uuid = credential_data['uuid']

        n_data = self.pwb.refresh_login()

        credential_data['refreshToken'] = n_data['refreshToken']
        credential_data['accessToken'] = n_data['accessToken']
        credential_data['tokenExpireTime'] = n_data['tokenExpireTime']

        file = open(self.json_path, 'w')
        json.dump(credential_data, file)
        file.close()

        # important to get the account_id
        return self.pwb.get_account_id()


if __name__ == "__main__":
    import schedule, time

    stock_list = ["TTE", "SGOC", "CPK", "HQI", "TDAC", "NXPI", "AB", "FIVN", "SILV", "HUBS"]
    stock_dic = {}
    for key in stock_list:
        stock_dic[key] = 0

    test_user = user("../Data/webull_credentials.json", stock_dic)
    wb_id = test_user.login_wb()
    pwb_id = test_user.login_pwb()


    stats_index = ['kdjj']
    buy_flag = {'kdjj': 15}
    sell_flag = {'kdjj': 85}
    test_user.set_trade_data((stats_index, buy_flag, sell_flag))
    #schedule.every().saturday.at("14:42").do(test_user.trade)
    print(test_user.simulation_2_filter())

    