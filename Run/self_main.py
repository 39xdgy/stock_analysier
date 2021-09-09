import sys, schedule, time

sys.path.append('../Class/')
from trade import trade
from user import user

stock_list = ["TTE", "SGOC", "CPK", "HQI", "TDAC", "NXPI", "AB", "FIVN", "SILV", "HUBS"]
#print(len(stock_list))
stock_dic = {}

for key in stock_list:
    stock_dic[key] = 0

kdj_user = user(json_path = "../data/webull_credentials.json", stock_dic = stock_dic)

kdj_user.login_pwb()
kdj_user.login_wb()

stats_index = ['kdjj']
buy_flag = {'kdjj': 15}
sell_flag = {'kdjj': 85}


schedule.every().monday.at("15:45").do(kdj_user.trade, (stats_index, buy_flag, sell_flag))
schedule.every().tuesday.at("15:45").do(kdj_user.trade, (stats_index, buy_flag, sell_flag))
schedule.every().wednesday.at("15:45").do(kdj_user.trade, (stats_index, buy_flag, sell_flag))
schedule.every().thursday.at("15:45").do(kdj_user.trade, (stats_index, buy_flag, sell_flag))
schedule.every().friday.at("15:45").do(kdj_user.trade, (stats_index, buy_flag, sell_flag))

while True:
    schedule.run_pending()
    time.sleep(50)
