import math
from stock_data import stock_data
from stock_data_origin import stock_data_origin
from trade import trade as td
from datetime import datetime, timedelta, time
import time as tm
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import os.path, json, pandas


class alp_user:

    def __init__(self, stock_dic, paper_trading, api_key, secret_key):
        self.stock_dic = stock_dic
        if not os.path.exists("../Data/back_up.json"):
            with open("../Data/back_up.json", "w") as f:
                json.dump(self.stock_dic, f)
        else: 
            with open("../Data/back_up.json", "r") as f:
                self.stock_dic = json.load(f)
        self.is_paper = paper_trading
        if self.is_paper:
            self.trading_client = TradingClient(api_key, secret_key, paper=True)
        else:
            self.trading_client = TradingClient(api_key, secret_key, paper=False)
       
        self.stats_index, self.buy_flag, self.sell_flag, self.trade_counter = {}, {}, {}, {}
        self.trade_record = []
       
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
        each_stock = stock_data_origin(stock_name = stock_name, period='3d', interval='1m')
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
    
        csv_list = pandas.read_csv('../Data/mid_volume_stocks.csv', keep_default_na=False)
        self.all_stocks_ticker = csv_list[csv_list.columns[0]]


    def simulation_2_filter(self):
        pass_stock = []
        volume = []
        for ticker in self.all_stocks_ticker:
            print(ticker)
            try:
                # Get the current date in local time
                today = datetime.today().date()

                # Add one day to get tomorrow's date
                tomorrow = today + timedelta(days=1)

                # Construct a datetime object for midnight tomorrow
                midnight_tomorrow = datetime.combine(tomorrow, time.min)

                # Get the Unix timestamp for midnight tomorrow
                tomorrow = int(tm.mktime(midnight_tomorrow.timetuple()))


                #get the date of 5 days ago in unix timestamp
                five_days_ago = tomorrow - 604800

                stock = stock_data(stock_name=ticker, start = five_days_ago, end = tomorrow)
                stock.get_stats_info(['kdjj'])
                time_diff, time_sum, stock_num, base_value = 0, 0, 0, 10000
                time_tracker = [-1, -1]
                flag, sell_flag = True, False

                buy_value, trade_count, fail_count, value_record = 0, 0, 0, 10000
                temp_price = 0.0
                # total_volume = 0.0
                for index, row in stock.get_stock_data().iterrows():
                    # total_volume += float(row["volume"])
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
                #volume.append(total_volume)
                #avg_volume = total_volume / 5
                if stock_num != 0:
                    base_value += stock.get_current_price() * stock_num
                
                if trade_count > 0 and fail_count / trade_count <= 0.25 and trade_count >= 10 and base_value > 10500:
                    pass_stock.append({
                        'name': ticker,
                        'final_value': base_value,
                        'trade_count': trade_count,
                        'fail_chance': fail_count / trade_count,
                        'avg_day': time_sum / trade_count,
                        'short_mins': time_tracker[0],
                        'long_mins': time_tracker[1]
                    })
                #total_outcome += base_value

            except Exception as e:
                print(e)
                continue
        #print(volume)
        sorted_list = sorted(pass_stock, key=lambda x: (x['fail_chance'], -x['final_value']))[:10]
    
        print(sorted_list)
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
                
                if self.is_paper:
                    quant = math.floor(100/each_stock.get_current_price() * 100) / 100
                else:
                    quant = math.floor(100/each_stock.get_current_price() * 100) / 100
        
                if value == 0 and should_buy['kdjj']:
                    new_td = td()
                    new_td.buy_update(name = key, start_time = str(datetime.now()), start_price = each_stock.get_current_price(), amount = quant)
                    self.trade_counter[key] = new_td
                    self.stock_dic[key] = quant
                    
                    if self.is_paper: 
                        self.stock_dic[key] = quant
                        # preparing orders
                        market_order_data = MarketOrderRequest(
                                            symbol = key,
                                            qty = quant,
                                            side = OrderSide.BUY,
                                            time_in_force = TimeInForce.DAY
                                            )

                        # Market order
                        market_order = self.paper_trading_client.submit_order(
                                        order_data=market_order_data
                                    )
                        print(market_order)
                    else: 
                        self.stock_dic[key] = quant
                        # preparing orders
                        market_order_data = MarketOrderRequest(
                                            symbol = key,
                                            qty = quant,
                                            side = OrderSide.BUY,
                                            time_in_force = TimeInForce.DAY
                                            )

                        # Market order
                        market_order = self.trading_client.submit_order(
                                        order_data=market_order_data
                                    )
                        print(market_order)
                elif (not value == 0) and should_sell['kdjj']:
                    #finished_td = self.trade_counter[key]
                    #finished_td.sell_update(end_time = str(datetime.now()), end_price = each_stock.get_current_price())
                    #self.trade_record.append(finished_td)
                    self.stock_dic[key] = 0
                    if self.is_paper:
                        self.stock_dic[key] = quant
                        # preparing orders
                        market_order_data = MarketOrderRequest(
                                            symbol = key,
                                            qty = quant,
                                            side = OrderSide.SELL,
                                            time_in_force = TimeInForce.DAY
                                            )

                        # Market order
                        market_order = self.paper_trading_client.submit_order(
                                        order_data=market_order_data
                                    )
                        print(market_order)
                    else: 
                        self.stock_dic[key] = quant
                        # preparing orders
                        market_order_data = MarketOrderRequest(
                                            symbol = key,
                                            qty = quant,
                                            side = OrderSide.SELL,
                                            time_in_force = TimeInForce.DAY
                                            )

                        # Market order
                        market_order = self.trading_client.submit_order(
                                        order_data=market_order_data
                                    )
                        print(market_order)

                    if(key in self.memory):
                        del self.memory[self.memory.index(key)]
                        del self.stock_dic[key]
                        with open("../Data/memory.json", 'w') as f:
                            json.dump(self.memory, f)

            except Exception as E:
                print(E)
        with open("../Data/back_up.json", 'w') as f:
            json.dump(self.stock_dic, f)
        
    def sell_all_stocks(self):
        for key in self.stock_dic:
            if self.stock_dic[key] != 0:
                quant = self.stock_dic[key]
                if self.is_paper:
                    self.stock_dic[key] = quant
                    # preparing orders
                    market_order_data = MarketOrderRequest(
                                        symbol = key,
                                        qty = quant,
                                        side = OrderSide.SELL,
                                        time_in_force = TimeInForce.DAY
                                        )

                    # Market order
                    market_order = self.paper_trading_client.submit_order(
                                    order_data=market_order_data
                                )
                    print(market_order)
                else: 
                    self.stock_dic[key] = quant
                    # preparing orders
                    market_order_data = MarketOrderRequest(
                                        symbol = key,
                                        qty = quant,
                                        side = OrderSide.SELL,
                                        time_in_force = TimeInForce.DAY
                                        )

                    # Market order
                    market_order = self.trading_client.submit_order(
                                    order_data=market_order_data
                                )
                    print(market_order)
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


