import sys, schedule, time, json, pandas
from alp_user import alp_user
from update_database import *



csv_list = pandas.read_csv('../Data/mid_volume_stocks.csv', keep_default_na=False)
stock_list = csv_list[csv_list.columns[0]]

long_stock_dic, short_stock_dic = {}, {}

#for key in long_stock_list: long_stock_dic[key] = 0
short_stock_dic = {key: 0 for key in stock_list}
with open('../Data/confidentials.json') as json_file:
    data = json.load(json_file)
    paper_secret_key = data["paper_secret_key"]
    paper_api_key = data["paper_api_key"]

    api_key = data["api_key"]
    secret_key = data["secret_key"]

short_user = alp_user(stock_dic = short_stock_dic, paper_trading = True, api_key = paper_api_key, secret_key = paper_secret_key)


stats_index = ['kdjj']
buy_flag = {'kdjj': 15}
sell_flag = {'kdjj': 85}

short_user.set_trade_data((stats_index, buy_flag, sell_flag))

# ----------- change csv in create_all_stock_tickers -------------
print(short_user.create_all_stock_tickers())
print(short_user.simulation_2_filter())
print(short_user.update_stock_list())


#deal with 9:XX
for m in range(30, 60):
    tot_time = f'09:{str(m)}'
    schedule.every().monday.at(tot_time).do(short_user.trade)
    schedule.every().tuesday.at(tot_time).do(short_user.trade)
    schedule.every().wednesday.at(tot_time).do(short_user.trade)
    schedule.every().thursday.at(tot_time).do(short_user.trade)
    schedule.every().friday.at(tot_time).do(short_user.trade)

#deal with the rest
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

schedule.every().monday.at("15:59").do(short_user.sell_all_stocks)
schedule.every().tuesday.at("15:59").do(short_user.sell_all_stocks)
schedule.every().wednesday.at("15:59").do(short_user.sell_all_stocks)
schedule.every().thursday.at("15:59").do(short_user.sell_all_stocks)
schedule.every().friday.at("15:59").do(short_user.sell_all_stocks)

schedule.every().monday.at("16:00").do(short_user.create_all_stock_tickers)
schedule.every().tuesday.at("16:00").do(short_user.create_all_stock_tickers)
schedule.every().wednesday.at("16:00").do(short_user.create_all_stock_tickers)
schedule.every().thursday.at("16:00").do(short_user.create_all_stock_tickers)
schedule.every().friday.at("16:00").do(short_user.create_all_stock_tickers)

schedule.every().monday.at("16:30").do(short_user.simulation_2_filter)
schedule.every().tuesday.at("16:30").do(short_user.simulation_2_filter)
schedule.every().wednesday.at("16:30").do(short_user.simulation_2_filter)
schedule.every().thursday.at("16:30").do(short_user.simulation_2_filter)
schedule.every().friday.at("16:30").do(short_user.simulation_2_filter)

schedule.every().monday.at("17:00").do(short_user.update_stock_list)
schedule.every().tuesday.at("17:00").do(short_user.update_stock_list)
schedule.every().wednesday.at("17:00").do(short_user.update_stock_list)
schedule.every().thursday.at("17:00").do(short_user.update_stock_list)
schedule.every().friday.at("17:00").do(short_user.update_stock_list)

while True:
    schedule.run_pending()
    time.sleep(10)
