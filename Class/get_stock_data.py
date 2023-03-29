import mysql.connector
import pandas as pd


# Fetch data for the specific symbol and format it as a pandas DataFrame
def fetch_data_day(symbol ,start_date, end_date):
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host = 'localhost', 
        user = 'root',
        password = "",
        database = "Stocks"
        )

    cursor = connection.cursor()
    # Execute the query to fetch data for the specific symbol
    query = f"""SELECT date, open, high, low, close, volume
                FROM stock_prices
                WHERE symbol = '{symbol}'
                AND date BETWEEN FROM_UNIXTIME('{start_date}') AND FROM_UNIXTIME('{end_date}')"""
    cursor.execute(query)

    # Fetch all rows as a list of tuples
    rows = cursor.fetchall()

    # Convert the rows to a pandas DataFrame
    df = pd.DataFrame(rows, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

    # Set the 'Date' column as the index
    df.set_index('Date', inplace=True)

    # Sort the DataFrame by the index (which is now the 'Date' column)
    df.sort_index(inplace=True)

    # Close the database connection
    connection.close()

    return df

# Fetch data for the specific symbol and format it as a pandas DataFrame
def fetch_data_1m(symbol ,start_date, end_date):
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host = 'localhost', 
        user = 'root',
        password = "",
        database = "Stocks"
        )

    cursor = connection.cursor()
    # Execute the query to fetch data for the specific symbol
    query = f"""SELECT date, open, high, low, close, volume
                FROM stock_prices_1m
                WHERE symbol = '{symbol}'
                AND date BETWEEN FROM_UNIXTIME('{start_date}') AND FROM_UNIXTIME('{end_date}')"""
    cursor.execute(query)

    # Fetch all rows as a list of tuples
    rows = cursor.fetchall()

    # Convert the rows to a pandas DataFrame
    df = pd.DataFrame(rows, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

    # Set the 'Date' column as the index
    df.set_index('Date', inplace=True)

    # Sort the DataFrame by the index (which is now the 'Date' column)
    df.sort_index(inplace=True)

    # Close the database connection
    connection.close()

    return df


