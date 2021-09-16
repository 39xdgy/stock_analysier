from webull import paper_webull, webull
from stock_data import stock_data
from trade import trade as td
from datetime import datetime

import json
class user:

    def __init__(self, json_path, stock_dic, is_pwb = True):
        self.stock_dic = stock_dic
        self.json_path = json_path
        self.is_pwb = is_pwb
        self.wb = webull()
        self.pwb = paper_webull()
        self.stats_index = {}
        self.buy_flag = {}
        self.sell_flag = {}
        self.trade_counter = {}
        self.trade_record = []


    def _create_stock_info(self, stock_name):
        each_stock = stock_data(stock_name = stock_name)
        each_stock.set_buy_flag(self.buy_flag)
        each_stock.set_sell_flag(self.sell_flag)
        each_stock.get_stats_info(self.stats_index)
        return each_stock

    
    def set_trade_data(self, input_data):
        self.stats_index, self.buy_flag, self.sell_flag = input_data
        
    

    def trade(self):
        print("trade start")
        
        for key in self.stock_dic:
            print()
            value = self.stock_dic[key]
            each_stock = self._create_stock_info(key)
            should_buy = each_stock.should_buy()
            should_sell = each_stock.should_sell()
            print(type(should_sell['kdjj']))
            quant = 10000 // each_stock.get_current_price()
            print(each_stock.get_current_price())
            real_quant = 1500 // each_stock.get_current_price()
            if value == 0 and should_buy['kdjj']:
                new_td = td()
                new_td.buy_update(name = key, start_time = str(datetime.now()), start_price = each_stock.get_current_price(), amount = quant)
                self.trade_counter[key] = new_td
                value = quant
                
                if self.is_pwb: self.pwb.place_order(stock = key, action = "BUY", orderType = "MKT", quant = quant)
                else: self.wb.place_order(stock = key, action = "BUY", orderType = "MKT", quant = real_quant)
            

            #print(value)
            if (not value == 0) and should_sell['kdjj']:
                finished_td = self._trade_counter[key]
                finished_td.sell_update(end_time = str(datetime.now()), end_price = each_stock.get_current_price())
                self.trade_record.append(finished_td)
                value = 0
                if self.is_pwb: self.pwb.place_order(stock = key, action = "SELL", orderType = "MKT", quant = quant)
                else: self.wb.place_order(stock = key, action = "SELL", orderType = "MKT", quant = real_quant)
        print("trade finished")

    def write_trade_record(self):
        f = open("./Data/trade_record.txt", "w")
        write_str = ''
        for record in self.trade_record:
            write_str += str(record)
            write_str += "\n\n"

        f.write(write_str)
        f.close()



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
    #print(wb_id)
    #print(pwb_id)


    stats_index = ['kdjj']
    buy_flag = {'kdjj': 15}
    sell_flag = {'kdjj': 85}
    test_user.set_trade_data((stats_index, buy_flag, sell_flag))
    #schedule.every().saturday.at("14:42").do(test_user.trade)
    test_user.trade()

    #test_user.trade()

    '''
    while True:
        schedule.run_pending()
        time.sleep(1)
        #print("still going")
    '''
    