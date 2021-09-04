import pandas as pd
import pandas_datareader as web
import yfinance as yf
import stockstats
import os

class stock_data:
    def __init__(self, stock_name = "", start_date = "", end_date = ""):
        self._stock_name = stock_name
        self._start_date = start_date
        self._end_date = end_date
        self._stock_data = None
        self._buy_flag = {}
        self._sell_flag = {}

    #----------------------------------------------------

    def get_stock_name(self) -> str:
        return self._stock_name
    
    def get_start_date(self) -> str:
        return self._start_date

    def get_end_date(self) -> str:
        return self._end_date

    def get_stock_data(self):
        return self._stock_data

    def get_buy_flag(self) -> dict:
        return self._buy_flag

    def get_sell_flag(self) -> dict:
        return self._sell_flag

    #---------------------------------------

    def set_stock_name(self, stock_name: str):
        self._stock_name = stock_name

    def set_start_date(self, start_date: str):
        self._start_date = start_date

    def set_end_date(self, end_date: str):
        self._end_date = end_date

    def set_buy_flag(self, buy_flag: dict):
        return self._buy_flag

    def set_sell_flag(self, sell_flag: dict):
        return self._sell_flag
    
    #---------------------------------------

    def __str__(self) -> str:
        out = "Stock: " + self._stock_name
        out += "\n" + "Start Date: " + str(self._start_date)[:10]
        out += "\n" + "End Date: " + str(self._end_date)[:10] + "\n"
        return out

    #---------------------------------------------------

    def read_stock_from_yahoo(self) -> bool:
        if(self._stock_name == "" or self._start_date == "" or self._end_date == ""):
            return False
        self._stock_data = web.DataReader(self._stock_name,'yahoo',self._start_date, self._end_date)
        #self._stock_data = yf.download(self._stock_name, self._start_date, self._end_date, interval = "5m")
        return True

    def write_to_json(self):
        self._stock_data.to_json(self._stock_name + '.json')

    def read_from_json(self, file_path) -> bool:
        if os.path.isfile(file_path):
            self._stock_name = file_path.split("/")[-1][:-5]
            self._stock_data = pd.read_json(file_path)
            self._start_date = self._stock_data.index[0]
            self._end_date = self._stock_data.index[-1]
            return True
        else:
            return False

    def get_stats_info(self, info_list):
        try:
            stockStat = stockstats.StockDataFrame.retype(self._stock_data)
            for info in info_list:
                self._stock_data[info] = stockStat[[info]]
            return True
        except:
            return False

    def get_current_price(self):
        return self._stock_data[self._end_date]['close']

    def should_buy(self):
        output = {}
        for key, value in self._buy_flag:
            if "cross" in key:
                diff = self._stock_data[self._end_date]["kdjk"] - self._stock_data[self._end_date]["kdjd"]
                if diff > 0: output[key] = True
                elif diff == 0:
                    double_check = self._stock_data[self._stock_data.index[-2]]["kdjk"] - self._stock_data[self._stock_data.index[-2]]["kdjd"]
                    if double_check > 0: output[key] = True
                    else: output[key] = False
                else: output[key] = False
            else:
                data_value = self._stock_data[self._end_date][key]
                last_data_value = self._stock_data[self._stock_data.index[-2]][key]
                if key == "macdh":
                    if data_value > 0: output[key] = True
                    elif data_value == 0:
                        if last_data_value >= 0: output[key] = True
                        else: output[key] = False
                    else: output[key] = False
                if key == "kdjj":
                    if data_value <= value: output[key] = True
                    else: output[key] = False
        return output

    def should_sell(self):
        output = {}
        for key, value in self._sell_flag:
            if "cross" in key:
                diff = self._stock_data[self._end_date]["kdjk"] - self._stock_data[self._end_date]["kdjd"]
                if diff < 0:
                    output[key] = True
                elif diff == 0:
                    double_check = double_check = self._stock_data[self._stock_data.index[-2]]["kdjk"] - self._stock_data[self._stock_data.index[-2]]["kdjd"]
                    if double_check > 0: output[key] = True
                    else: output[key] = False
                else:
                    data_value = self._stock_data[self._end_date][key]
                    last_data_value = self._stock_data[self._stock_data.index[-2]][key] 
                    if key == "macdh":
                        if data_value < 0: output[key] = True
                        elif data_value == 0:
                            if last_data_value < 0: output[key] = True
                            else: output[key] = False
                        else: output[key] = False
                    if key == "kdjj":
                        if data_value >= value: output[key] = True
                        else: output[key] = False

        return output

    


if __name__ == "__main__":
    #testing only
    test = stock_data()
    print(test)
    test.read_from_json('AAPL.json')
    print(test)
    test.get_stats_info(['macd', 'macds', 'macdh', 'kdjk', 'kdjd', 'kdjj', 'rsi_6', 'rsi_12', 'rsi_14'])
    print(test.get_stock_data())