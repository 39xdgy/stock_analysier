import pandas as pd
import pandas_datareader as web
import yfinance as yf
import stockstats
import os
from get_stock_data import fetch_data

class stock_data:
    def __init__(self, stock_name, start, end):
        self._stock_name = stock_name
        self._start = start
        self._end = end
        self._stock_data = fetch_data(self._stock_name, self._start, self._end)
        self._buy_flag = {}
        self._sell_flag = {}

    #----------------------------------------------------

    def get_stock_name(self) -> str:
        return self._stock_name

    def get_stock_data(self):
        return self._stock_data


    #---------------------------------------


    def set_buy_flag(self, buy_flag: dict):
        self._buy_flag = buy_flag

    def set_sell_flag(self, sell_flag: dict):
        self._sell_flag = sell_flag
    
    #---------------------------------------

    def __str__(self) -> str:
        out = f'Stock: {self._stock_name}\n'
        out += f'\tStart: {self._start}\n'
        out += f'\tEnd: {self._end}\n'
        return out

    #---------------------------------------------------

    # update the stock data to get the latest stock info
    def update_stock_data(self):
        self._stock_data = fetch_data(self._stock_name, self._start, self._end)

    # create the stats info and add it into the stock data
    def get_stats_info(self, info_list):
        try:
            #print(self._stock_data)
            stockStat = stockstats.StockDataFrame.retype(self._stock_data)
            for info in info_list:
                self._stock_data[info] = stockStat[[info]]
            return True
        except:
            return False

    # return the current price
    def get_current_price(self):
        return self._stock_data.at[self._stock_data.index[-1] ,'close']


    # decide the result wheather the stock should be buy or not base on the flag that people give
    # return a dictionary where all the result of the flags
    def should_buy(self):
        output = {}
        for key in self._buy_flag:
            value = self._buy_flag[key]
            if "cross" in key:
                diff = self._stock_data.at[self._stock_data.index[-1], "kdjk"] - self._stock_data.at[self._stock_data.index[-1], "kdjd"]
                if diff > 0: output[key] = True
                elif diff == 0:
                    double_check = self._stock_data.at[self._stock_data.index[-2], "kdjk"] - self._stock_data.at[self._stock_data.index[-2], "kdjd"]
                    if double_check > 0: output[key] = True
                    else: output[key] = False
                else: output[key] = False
            else:
                print(self._stock_data)
                data_value= self._stock_data.at[self._stock_data.index[-1], key]
                last_data_value = self._stock_data.at[self._stock_data.index[-2], key]
                if key == "macdh":
                    if data_value> 0: output[key] = True
                    elif data_value== 0:
                        if last_data_value >= 0: output[key] = True
                        else: output[key] = False
                    else: output[key] = False
                if key == "kdjj":
                    if data_value<= value: output[key] = True
                    else: output[key] = False

        return output


    # decide the result wheather the stock should be sell or not base on the flag that people give
    # return a dictionary where all the result of the flags
    def should_sell(self):
        output = {}
        for key in self._sell_flag:
            value = self._sell_flag[key]
            if "cross" in key:
                diff = self._stock_data.at[self._stock_data.index[-1], "kdjk"] - self._stock_data.at[self._stock_data.index[-1], "kdjd"]
                if diff < 0:
                    output[key] = True
                elif diff == 0:
                    double_check = double_check = self._stock_data.at[self._stock_data.index[-2], "kdjk"] - self._stock_data.at[self._stock_data.index[-2], "kdjd"]
                    if double_check > 0: output[key] = True
                    else: output[key] = False
                else: output[key] = False
            else:
                data_value= self._stock_data.at[self._stock_data.index[-1], key]
                last_data_value = self._stock_data.at[self._stock_data.index[-2], key] 
                if key == "macdh":
                    if data_value< 0: output[key] = True
                    elif data_value== 0:
                        if last_data_value < 0: output[key] = True
                        else: output[key] = False
                    else: output[key] = False
                if key == "kdjj":
                    if data_value>= value: output[key] = True
                    else: output[key] = False

        return output

    


if __name__ == "__main__":
    #testing only
    test = stock_data(stock_name="AAPL", start=1552790273, end=1584422673)
    print(test)
    test.get_stats_info(['kdjj'])
    test.set_buy_flag({'kdjj': 15})
    test.set_sell_flag({'kdjj': 85})
    
    print(test.get_stock_data())
    print(test.should_buy())
    print(test.should_sell())
