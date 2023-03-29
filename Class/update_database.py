import mysql.connector
from pandas import *
import yfinance as yf
import time as T
import multiprocessing
from istarmap import *
import tqdm
import schedule, time

mydb = mysql.connector.connect(
  host = 'localhost',
  user = 'root',
  password = "",
  database = "Stocks"
)


def get_all_info():
	try:
		df = read_csv("nasdaq.csv", keep_default_na=False)
		tickers = df["Symbol"].tolist()
		names = df["Name"].tolist()
		args_iter = []
		#format the iterable tuples for starmap args
		for i in range(len(tickers)):
			args_iter.append((tickers[i], names[i]))
		start = T.time()
		pool_obj = multiprocessing.Pool()
		with pool_obj as pool:
			for _ in tqdm.tqdm(pool.istarmap(get_all_info_worker, args_iter),total=len(args_iter)):
				pass 
			
		end = T.time()
		print("Processed " + str(len(tickers)) + " stocks")
		print("Time taken: " + str(end-start) + " seconds")
		mydb.commit()
		# cursor.close()
	except Exception as e:
		return str(e)
	return "Done"

def get_all_info_worker(ticker, name):
	try:
		#print("Getting info for: " + ticker + " - " + name)
		cursor = mydb.cursor()
		cursor.execute(''' INSERT IGNORE INTO stock_info(symbol,name) VALUES(%s,%s)''',(ticker, name))
		mydb.commit()
	except Exception as e:
		return str(e)
	return "Done"

def get_all_history():
	try:
		df = read_csv("nasdaq.csv", keep_default_na=False)
		tickers = df["Symbol"].tolist()
	
		start = T.time()
		pool_obj = multiprocessing.Pool()
		with pool_obj as pool:
			for _ in tqdm.tqdm(pool.imap(get_all_history_worker, tickers),total=len(tickers)):
				pass
			
		end = T.time()
		print("Time taken: " + str(end-start))
		mydb.commit()
		# cursor.close()
	except Exception as e:
		return str(e)
	return "Done"

def get_all_history_worker(ticker):
	try:
		cursor = mydb.cursor()
		history = yf.download(ticker, period="5d", interval="1m")
		if not history["Close"].empty:
			open_dict = history["Open"].to_dict()
			close_dict = history["Close"].to_dict()
			high_dict = history["High"].to_dict()
			low_dict = history["Low"].to_dict()
			volume_dict = history["Volume"].to_dict()
			for time,open in open_dict.items():
				
				close = close_dict[time]
				high = high_dict[time]
				low = low_dict[time]
				volume = volume_dict[time]
				try:
					cursor.execute(''' INSERT IGNORE INTO stock_prices_1m(symbol,date,open,close,high,low,volume) VALUES(%s,%s,%s,%s,%s,%s,%s)''',(ticker, time, open, close, high, low, volume))
				except mysql.connector.Error as err:
					print("MySQL error: {}".format(err))
				mydb.commit()
		mydb.commit()
	except Exception as e:
		return str(e)
	return "Done"

if __name__ == "__main__":
	schedule.every().monday.at("16:45").do(get_all_history)
	schedule.every().tuesday.at("16:45").do(get_all_history)
	schedule.every().wednesday.at("16:45").do(get_all_history)
	schedule.every().thursday.at("16:45").do(get_all_history)
	schedule.every().friday.at("16:45").do(get_all_history)

	while True:
		schedule.run_pending()
		time.sleep(10)
	# get_all_history()
