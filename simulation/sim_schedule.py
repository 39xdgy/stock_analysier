
import pandas as pd
import pandas_market_calendars as mcal
from datetime import datetime, timedelta

def rolling_six_mon_one_mon_schedule():
    # Define the stock exchange we want to use
    nyse = mcal.get_calendar('NYSE')

    # Define the start and end dates
    end_date = datetime.today()
    start_date = end_date - timedelta(days=5*365)

    # Get the schedule of trading days between the start and end dates
    schedule = nyse.schedule(start_date=start_date, end_date=end_date)

    # Get the trading days as a list of datetime objects
    trading_days = schedule.index.tolist()

    # Create a list of tuples, where each tuple contains the start and end date of a 6-month period followed by a 1-month period
    date_pairs = []
    six_month_days = 6 * 21
    one_month_days = 21

    for i in range(len(trading_days) - six_month_days - one_month_days + 1):
        six_month_start = trading_days[i]
        six_month_end = trading_days[i + six_month_days - 1]
        one_month_start = trading_days[i + six_month_days]
        one_month_end = trading_days[i + six_month_days + one_month_days - 1]
        date_pairs.append((six_month_start, six_month_end, one_month_start, one_month_end))

    return date_pairs

def rolling_six_mon_two_mon_schedule():
    # Define the stock exchange we want to use
    nyse = mcal.get_calendar('NYSE')

    # Define the start and end dates
    end_date = datetime.today()
    start_date = end_date - timedelta(days=5*365)

    # Get the schedule of trading days between the start and end dates
    schedule = nyse.schedule(start_date=start_date, end_date=end_date)

    # Get the trading days as a list of datetime objects
    trading_days = schedule.index.tolist()

    # Create a list of tuples, where each tuple contains the start and end date of a 6-month period followed by a 2-month period
    date_pairs = []
    six_month_days = 6 * 21
    two_month_days = 2 * 21

    for i in range(len(trading_days) - six_month_days - two_month_days + 1):
        six_month_start = trading_days[i]
        six_month_end = trading_days[i + six_month_days - 1]
        two_month_start = trading_days[i + six_month_days]
        two_month_end = trading_days[i + six_month_days + two_month_days - 1]
        date_pairs.append((six_month_start, six_month_end, two_month_start, two_month_end))

    return date_pairs

def six_mon_one_mon_schedule():
    # Define the stock exchange we want to use
    nyse = mcal.get_calendar('NYSE')

    # Define the start and end dates
    end_date = datetime.today()
    start_date = end_date - timedelta(days=5*365)

    # Get the schedule of trading days between the start and end dates
    schedule = nyse.schedule(start_date=start_date, end_date=end_date)

    # Get the trading days as a list of datetime objects
    trading_days = schedule.index.tolist()

    # Create a list of tuples, where each tuple contains the start and end date of a 180-day period followed by a 30-day period
    date_pairs = []
    period_length = 126 + 21
    for i in range(0, len(trading_days), period_length):
        if i + 210 < len(trading_days):
            date_pairs.append((trading_days[i], trading_days[i+125], trading_days[i+126], trading_days[i+146]))
        else:
            date_pairs.append((trading_days[i], trading_days[-1]))
    return date_pairs
    # 0-1 is training data, 2-3 is testing data
    #data = yf.download("AAPL", start=date_pairs[0][2], end=date_pairs[0][3])

def six_mon_three_mon_schedule():
    # Define the stock exchange we want to use
    nyse = mcal.get_calendar('NYSE')

    # Define the start and end dates
    end_date = datetime.today()
    start_date = end_date - timedelta(days=5*365)

    # Get the schedule of trading days between the start and end dates
    schedule = nyse.schedule(start_date=start_date, end_date=end_date)

    # Get the trading days as a list of datetime objects
    trading_days = schedule.index.tolist()

    # Create a list of tuples, where each tuple contains the start and end date of a 126-day period followed by a 63-day period
    date_pairs = []
    period_length = 126 + 63
    for i in range(0, len(trading_days), period_length):
        if i + period_length < len(trading_days):
            date_pairs.append((trading_days[i], trading_days[i+125], trading_days[i+126], trading_days[i+188]))
        else:
            date_pairs.append((trading_days[i], trading_days[-1]))
    return date_pairs



def five_day_one_day_schedule():
    # Define the stock exchange we want to use
    nyse = mcal.get_calendar('NYSE')

    # Define the start and end dates
    end_date = datetime.today()
    start_date = end_date - timedelta(days=45)

    # Get the schedule of trading days between the start and end dates
    schedule = nyse.schedule(start_date=start_date, end_date=end_date)

    # Get the trading days as a list of datetime objects
    trading_days = schedule.index.tolist()

    # Create a list of tuples, where each tuple contains the start and end date of a 5-day period followed by a 1-day period
    date_pairs = []
    five_day_days = 5
    one_day_days = 2

    for i in range(len(trading_days) - five_day_days - one_day_days + 1):
        five_day_start = trading_days[i]
        five_day_end = trading_days[i + five_day_days - 1]
        one_day_start = trading_days[i + five_day_days]
        one_day_end = trading_days[i + five_day_days + one_day_days - 1]
        date_pairs.append((five_day_start, five_day_end, one_day_start, one_day_end))

    return date_pairs
