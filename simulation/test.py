import yfinance as yf
from get_stock_data import fetch_data
import time as T
import sim_schedule as S
import matplotlib.pyplot as plt
# s = T.time()
# data = yf.download("AAPL", period="2mo", interval="2m")
# # e = T.time()
# print(data)
# print(e-s)
# # data2 = yf.Ticker("AAPL").history(start=1552790273, end=1584412673)
# s = T.time()
# data3 = fetch_data("AAPL", 1552790273, 1584412673)
# e = T.time()
# print(data3)
# print(e-s)

#print(S.rolling_six_mon_two_mon_schedule())

filename = '../Data/5yr_6mo_2mo_kdjj_15_85.txt'

# Read the file and store the numbers as a list of integers
with open(filename, 'r') as file:
    numbers = [float(line.strip()) for line in file]

# Count the total number of numbers
total_numbers = len(numbers)

# Count the numbers below 10,000
below_10000 = sum(1 for number in numbers if number < 10000)

# Calculate the percentage
percentage = (below_10000 / total_numbers) * 100

print(f'Average price: {sum(numbers)/len(numbers)}')
print(f'Percentage of numbers below 10,000: {percentage:.2f}%')

# Create the bar chart
plt.figure(figsize=(20, 5))
plt.bar(range(len(numbers)), numbers)

# Draw the reference line at 10,000
plt.axhline(y=10000, color='r', linestyle='--', label='10,000 Base Line')

# Customize the plot
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('Bar Chart of 5yr 6mon/2mon KDJJ 15/85 trading schedule with Base Line at 10,000')
plt.legend()

# Show the plot
plt.show()

