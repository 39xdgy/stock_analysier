from webull import paper_webull, webull
from datetime import datetime, timedelta, time
import time as tm
from get_stock_data import fetch_data_1m
from stock_data_origin import stock_data_origin

webull_email = 'wzongshuo@gmail.com'

wb = paper_webull()
# wb.get_mfa(webull_email)
wb._did = '45531b559d5841c3a917369fe7e0de5c'
result = wb.login(webull_email, 'your password', 'device name', 'token')

print(result)

# # Get the current date in local time
# today = datetime.today().date()

# # Add one day to get tomorrow's date
# tomorrow = today + timedelta(days=1)

# # Construct a datetime object for midnight tomorrow
# midnight_tomorrow = datetime.combine(tomorrow, time.min)

# # Get the Unix timestamp for midnight tomorrow
# tomorrow = int(tm.mktime(midnight_tomorrow.timetuple()))


# #get the date of 5 days ago in unix timestamp
# five_days_ago = tomorrow - 604800

# data_range = [tomorrow, five_days_ago]

# print(fetch_data_1m('aapl',data_range[1] , data_range[0]))

each_stock = stock_data_origin(stock_name = 'ZKIN', period='3d', interval='1m')

print(each_stock)