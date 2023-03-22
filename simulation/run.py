import multiprocessing
from istarmap import *
from tqdm import tqdm
import pandas
import time as T
import json
from filter_stocks import run_filter, filter_sort, run_analyze
from sim_schedule import *


def concatenate_string(lock, shared_str, new_str):
    with lock:  # Acquire a lock to prevent concurrent access
        shared_str.value += new_str
    return shared_str.value

def worker(lock, shared_str, start, end, stock):
    new_str = run_filter(start, end, stock)
    return concatenate_string(lock, shared_str, new_str)

def main(schedule, n=0):
    start = T.time()
    #--------------------------------Load different CSV file--------------------------------
    csv_list = pandas.read_csv('../Data/russell-1000.csv')
    stock_list = csv_list[csv_list.columns[0]]
    args_iter = []
    
    with multiprocessing.Manager() as manager:
        # Use a Manager to create a shared ctypes string
        shared_str = manager.Value("ctypes.c_char_p", "")
        #format the iterable tuples for starmap args
        lock = manager.Lock()
        for i in range(len(stock_list)):
            args_iter.append((lock, shared_str, schedule[n][0], schedule[n][1], stock_list[i]))
        
        with multiprocessing.Pool() as pool:
            # Pass the shared string and the individual strings as arguments to the worker function
            pool.starmap(worker, args_iter)
        
        end = T.time()
        print(f"Time taken: {end - start} seconds")
        #print(f"Final string: {shared_str.value}")
        f = open("../Data/all_stock_1d_output.txt", "w")
        f.write(shared_str.value)
        f.close()
        filter_sort()

def analyze_performance(schedule, n=0):
    # Load the JSON file
    with open('../Data/top_10_output.json', 'r') as file:
        data = json.load(file)
        out_str = ""
        outcome_lst = []
        # Iterate through the JSON objects and print the 'name' field
        for item in data:
            stock_name = item['name']
            stock_anal_info = run_analyze(schedule[n][2], schedule[n][3], stock_name)
            new_str = stock_anal_info["info"]
            outcome_lst.append(stock_anal_info["outcome"])
            out_str += new_str
        print("average price: " + str(sum(outcome_lst)/len(outcome_lst)))
        f = open('../Data/top_10_output_prediction.txt', 'w')
        f.write(out_str)
        f.close()
        return sum(outcome_lst)/len(outcome_lst)

if __name__ == "__main__":
    #------------------change the schedule to the one you want to run------------------
    schedule = rolling_six_mon_two_mon_schedule()
    schedule.pop()

    five_year_performance = []
    #-------------------change the file name to the schedule you are running-------------------
    f = open('../Data/5yr_6mo_2mo_kdjj_15_85_rus1000.txt', 'w')
    for i in range(len(schedule)):
        print(f"Running schedule {i}")
        main(schedule, i)
        five_year_performance.append(analyze_performance(schedule, i))
        f.write(str(five_year_performance[i]) + "\n")
    print("5yr avg:" + str(sum(five_year_performance)/len(five_year_performance)))
    print(five_year_performance)
    f.close()


