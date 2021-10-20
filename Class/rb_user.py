from robin_stocks import robinhood as rh
from stock_data import stock_data
from trade import trade as td
from datetime import datetime

import os.path, json, pandas, pyotp, ftplib


class rb_user:

    def __init__(self, json_path, stock_dic, data_range = ['3d', '1m']):
        self.stock_dic = stock_dic
        if not os.path.exists("../Data/back_up.json"):
            with open("../Data/back_up.json", "w") as f:
                json.dump(self.stock_dic, f)
        else: 
            with open("../Data/back_up.json", "r") as f:
                self.stock_dic = json.load(f)
        self.json_path = json_path
        self.stats_index, self.buy_flag, self.sell_flag, self.trade_counter = {}, {}, {}, {}
        self.trade_record = []
        self.data_range = data_range
        self.next_day_dic = {}
        self.memory = []
        if not os.path.exists("../Data/memory.json"):
            with open("../Data/memory.json", "w") as f:
                json.dump(self.memory, f)
        else: 
            with open("../Data/memory.json", "r") as f:
                self.memory = json.load(f)

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
            if self.stock_dic[key] != 0:
                if key not in self.next_day_dic:
                    self.memory.append(key)
                self.next_day_dic[key] = self.stock_dic[key]

        self.stock_dic = self.next_day_dic
        with open("../Data/back_up.json", "w") as f:
            json.dump(self.stock_dic, f)

        with open("../Data/memory.json", 'w') as f:
            json.dump(self.memory, f)


    def _check_if_ticker_in_list(self, ticker) -> bool:
        return 'File Creation Time' not in ticker and 'Symbol' not in ticker and "$" not in ticker and "." not in ticker and ticker not in self.all_stocks_ticker

    def create_all_stock_tickers(self):
        ftp = ftplib.FTP('ftp.nasdaqtrader.com', 'anonymous', 'anonymous@debian.org')
        
        # Download files nasdaqlisted.txt and otherlisted.txt from ftp.nasdaqtrader.com
        for ficheiro in ["nasdaqlisted.txt", "otherlisted.txt"]:
                ftp.cwd("/SymbolDirectory")
                localfile = open(f'../Data/{ficheiro}', 'wb')
                ftp.retrbinary('RETR ' + ficheiro, localfile.write)
                localfile.close()
        ftp.quit()
        
        # Grep for common stock in nasdaqlisted.txt and otherlisted.txt

        self.all_stocks_ticker = []

        for ficheiro in ["nasdaqlisted.txt", "otherlisted.txt"]:
                localfile = open(f'../Data/{ficheiro}', 'r')
                open("../Data/tickers.txt", "w")
                for line in localfile:
                    #print(line)
                    ticker = line.split("|")[0]
                    if self._check_if_ticker_in_list(ticker):
                        self.all_stocks_ticker.append(ticker)


    def simulation_2_filter(self):
        pass_stock = {}
        for ticker in self.all_stocks_ticker:
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

            except Exception as e:
                continue

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
        

    # trade with all the stocks under this user
    def trade(self):
        ticker_place_holder = [ticker for ticker in self.stock_dic]
        for key in ticker_place_holder:
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
                    
                    self.stock_dic[key] = real_quant
                    rh.order_buy_market(key, real_quant)
                    
                elif (not value == 0) and should_sell['kdjj']:
                    #finished_td = self.trade_counter[key]
                    #finished_td.sell_update(end_time = str(datetime.now()), end_price = each_stock.get_current_price())
                    #self.trade_record.append(finished_td)
                    self.stock_dic[key] = 0
                    
                    rh.order_buy_market(key, value)
                    if(key in self.memory):
                        del self.memory[self.memory.index(key)]
                        del self.stock_dic[key]
                        with open("../Data/memory.json", 'w') as f:
                            json.dump(self.memory, f)

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

    def login(self):
        user_data = {}
        with open(self.json_path, 'r') as f:
            user_data = json.load(f)
            
        totp = pyotp.TOTP(user_data['token']).now()
        print("Please check your message on your phone for your validation code!")
        login = rh.login(user_data['user'], user_data['pwd'], mfa_code=totp)
        return login

    def logout(self):
        rh.logout()



if __name__ == "__main__":
    import schedule, time

    stock_list = ["TTE", "SGOC", "CPK", "HQI", "TDAC", "NXPI", "AB", "FIVN", "SILV", "HUBS"]
    stock_dic = {}
    for key in stock_list:
        stock_dic[key] = 0

    test_user = rb_user("../Data/rh_login.json", stock_dic)
    print(test_user.login())


    stats_index = ['kdjj']
    buy_flag = {'kdjj': 15}
    sell_flag = {'kdjj': 85}
    test_user.set_trade_data((stats_index, buy_flag, sell_flag))

    

    test_user.logout()


