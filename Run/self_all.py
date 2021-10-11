import sys, schedule, time

sys.path.append('../Class/')
from trade import trade
from user import user

short_stock_list = ["FRLN", "SALM", "ADMA", "IVR", "NBY", "AVD", "STVN", "GGPI", "SOGO", "GPOR"]
#print(len(stock_list))
long_stock_dic, short_stock_dic = {}, {}

#for key in long_stock_list: long_stock_dic[key] = 0
short_stock_dic = {key: 0 for key in short_stock_list}
short_user = user(json_path = "../Data/webull_credentials.json", stock_dic = short_stock_dic)

short_user.login_pwb()

stats_index = ['kdjj']
buy_flag = {'kdjj': 15}
sell_flag = {'kdjj': 85}

short_user.set_trade_data((stats_index, buy_flag, sell_flag))




for m in range(30, 60):
    tot_time = f'09:{str(m)}'
    schedule.every().monday.at(tot_time).do(short_user.trade)
    schedule.every().tuesday.at(tot_time).do(short_user.trade)
    schedule.every().wednesday.at(tot_time).do(short_user.trade)
    schedule.every().thursday.at(tot_time).do(short_user.trade)
    schedule.every().friday.at(tot_time).do(short_user.trade)


for h in range(10, 16):
    for m in range(0, 60):
        h_str, m_str = str(h), str(m)
        if(len(m_str) == 1): m_str = "0" + m_str
        tot_time = f'{h_str}:{m_str}'
        schedule.every().monday.at(tot_time).do(short_user.trade)
        schedule.every().tuesday.at(tot_time).do(short_user.trade)
        schedule.every().wednesday.at(tot_time).do(short_user.trade)
        schedule.every().thursday.at(tot_time).do(short_user.trade)
        schedule.every().friday.at(tot_time).do(short_user.trade)


schedule.every().monday.at("17:00").do(short_user.simulation_2_filter)
schedule.every().tuesday.at("17:00").do(short_user.simulation_2_filter)
schedule.every().wednesday.at("17:00").do(short_user.simulation_2_filter)
schedule.every().thursday.at("17:00").do(short_user.simulation_2_filter)
schedule.every().friday.at("17:00").do(short_user.simulation_2_filter)

schedule.every().monday.at("22:00").do(short_user.update_stock_list)
schedule.every().tuesday.at("22:00").do(short_user.update_stock_list)
schedule.every().wednesday.at("22:00").do(short_user.update_stock_list)
schedule.every().thursday.at("22:00").do(short_user.update_stock_list)
schedule.every().friday.at("22:00").do(short_user.update_stock_list)

while True:
    schedule.run_pending()
    time.sleep(10)
