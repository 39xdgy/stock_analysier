from webull import paper_webull, webull
from stock_data import stock_data
import datetime
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

    
    def set_stock_data(self, input_data):
        self.stats_index, self.buy_flag, self.sell_flag = input_data
        
    

    def trade(self):
        print("trade start")
        #print(self.buy_flag)
        #print(self.sell_flag)
        #print(self.stats_index)
        
        for key in self.stock_dic:
            value = self.stock_dic[key]
            each_stock = stock_data(stock_name = key, start_date = datetime.date.today() - datetime.timedelta(days = 365), end_date = datetime.date.today())
            each_stock.read_stock_from_yahoo()
            each_stock.set_buy_flag(self.buy_flag)#{'kdjj': 15})
            each_stock.set_sell_flag(self.sell_flag)#{'kdjj': 85})
            each_stock.get_stats_info(self.stats_index)#['kdjj'])
            should_buy = each_stock.should_buy()
            should_sell = each_stock.should_sell()
            if value == 0 and each_stock.should_buy()['kdjj']:
                if self.is_pwb:
                    self.pwb.place_order(stock = key, action = "BUY", orderType = "MKT", quant = 10000 // each_stock.get_current_price())
                else:
                    self.wb.place_order(stock = key, action = "BUY", orderType = "MKT", quant = 10000 // each_stock.get_current_price())
            
            if value != 0 and each_stock.should_sell()['kdjj']:
                if self.is_pwb:
                    self.pwb.place_order(stock = key, action = "SELL", orderType = "MKT", quant = 10000 // each_stock.get_current_price())
                else:
                    self.wb.place_order(stock = key, action = "SELL", orderType = "MKT", quant = 10000 // each_stock.get_current_price())
        print("trade finished")

            



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
    test_user.set_stock_data((stats_index, buy_flag, sell_flag))
    schedule.every().saturday.at("14:42").do(test_user.trade)
    #test_user.trade((stats_index, buy_flag, sell_flag))

    #test_user.trade()

    
    while True:
        schedule.run_pending()
        time.sleep(1)
        #print("still going")
    