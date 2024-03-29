from webull import paper_webull, webull
from stock_data import stock_data
from trade import trade as td
from datetime import datetime

import os.path, json, pandas, ftplib


class wb_user:

    def __init__(self, json_path, stock_dic, is_pwb, data_range = ['3d', '1m']):
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
        self.all_stocks_ticker = []
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
                real_quant = 1500 // each_stock.get_current_price()
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
                        buy_out = self.wb.place_order(stock = key, action = "BUY", orderType = "MKT", enforce = "DAY", quant = real_quant)
                        print(buy_out)
                elif (not value == 0) and should_sell['kdjj']:
                    #finished_td = self.trade_counter[key]
                    #finished_td.sell_update(end_time = str(datetime.now()), end_price = each_stock.get_current_price())
                    #self.trade_record.append(finished_td)
                    self.stock_dic[key] = 0
                    if self.is_pwb: self.pwb.place_order(stock = key, action = "SELL", orderType = "MKT", enforce = "DAY", quant = value)
                    else: self.wb.place_order(stock = key, action = "SELL", orderType = "MKT", enforce = "DAY", quant = value)
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

    # login to the webull real account
    def login_wb(self, trade_pwd):
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
        self.wb._account_id = self.wb.get_account_id()
        self.wb.get_trade_token(trade_pwd)
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

    test_user = wb_user("../Data/webull_credentials.json", stock_dic, is_pwb = True)
    #wb_id = test_user.login_wb()
    pwb_id = test_user.login_pwb()


    stats_index = ['kdjj']
    buy_flag = {'kdjj': 15}
    sell_flag = {'kdjj': 85}
    test_user.set_trade_data((stats_index, buy_flag, sell_flag))
    #schedule.every().saturday.at("14:42").do(test_user.trade)
    test_user.create_all_stock_tickers()
    test_user.simulation_2_filter()
    test_user.update_stock_list()

