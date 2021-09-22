import sys, schedule, time

sys.path.append('../Class/')
from trade import trade
from user import user

stock_list = ["FRLN", "SALM", "ADMA", "IVR", "NBY", "AVD", "STVN", "GGPI", "SOGO", "GPOR"]
#print(len(stock_list))
stock_dic = {}

for key in stock_list:
    stock_dic[key] = 0

kdj_user = user(json_path = "../Data/webull_credentials.json", stock_dic = stock_dic)

kdj_user.login_pwb()
kdj_user.login_wb()

stats_index = ['kdjj']
buy_flag = {'kdjj': 15}
sell_flag = {'kdjj': 85}

kdj_user.set_trade_data((stats_index, buy_flag, sell_flag))
for m in range(30, 60):
    tot_time = f'09:{str(m)}'
    print(tot_time)
    schedule.every().monday.at(tot_time).do(kdj_user.trade)
    schedule.every().tuesday.at(tot_time).do(kdj_user.trade)
    schedule.every().wednesday.at(tot_time).do(kdj_user.trade)
    schedule.every().thursday.at(tot_time).do(kdj_user.trade)
    schedule.every().friday.at(tot_time).do(kdj_user.trade)


for h in range(10, 16):
    for m in range(0, 60):
        h_str, m_str = str(h), str(m)
        if(len(m_str) == 1): m_str = "0" + m_str
        tot_time = f'{h_str}:{m_str}'
        print(tot_time)
        schedule.every().monday.at(tot_time).do(kdj_user.trade)
        schedule.every().tuesday.at(tot_time).do(kdj_user.trade)
        schedule.every().wednesday.at(tot_time).do(kdj_user.trade)
        schedule.every().thursday.at(tot_time).do(kdj_user.trade)
        schedule.every().friday.at(tot_time).do(kdj_user.trade)

while True:
    print("uo")
    schedule.run_pending()
    time.sleep(10)
