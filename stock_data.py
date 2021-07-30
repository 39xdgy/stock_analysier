import pandas as pd
import pandas_datareader as web
import os
class stock_data:

    def __init__(self, read_data = False, stock_name = "", start_date = "", end_date = ""):
        self._stock_name = stock_name
        self._start_date = start_date
        self._end_date = end_date
        self._stock_data = None

    #----------------------------------------------------

    def get_stock_name(self) -> str:
        return self._stock_name
    
    def get_start_date(self) -> str:
        return self._start_date

    def get_end_date(self) -> str:
        return self._end_date

    def get_stock_data(self):
        return self._stock_data

    #---------------------------------------

    def set_stock_name(self, stock_name: str) -> str:
        self._stock_name = stock_name

    def set_start_date(self, start_date: str) -> str:
        self._start_date = start_date

    def set_end_date(self, end_date: str) -> str:
        self._end_date = end_date
    
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
        

if __name__ == "__main__":
    #testing only
    test = stock_data("AAPL", '2016-01-04', '2021-07-01')
    test.read_from_json('AAPL.json')
    print(test)