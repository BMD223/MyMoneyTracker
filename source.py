from alpaca.data.live.stock import *
from alpaca.data.historical.stock import *
from alpaca.data.requests import *
from alpaca.data.timeframe import *
import pandas as pd
import numpy as np
import os
import requests
from datetime import datetime, timedelta

POSITIONS_PATH = "/Users/bbd223/Desktop/Personal projects/private data/positions.csv"
KEYS_PATH = "/Users/bbd223/Desktop/Personal projects/private data/keys"
f_keys=open(KEYS_PATH, mode='r')
keys=f_keys.readlines()
PUBLIC_KEY=keys[0].strip()
PRIVATE_KEY=keys[1].strip()
clock_url='https://paper-api.alpaca.markets/v2/clock'
headers = {'APCA-API-KEY-ID': PUBLIC_KEY,'APCA-API-SECRET-KEY': PRIVATE_KEY}
client=StockHistoricalDataClient(api_key=PUBLIC_KEY,secret_key=PRIVATE_KEY)
"""
Here i will do a test segment, to fetch AAPL price 15 mins ago.

"""
def testfetch():
    clock_response=requests.get(clock_url,headers=headers)
    symbol= ['AAPL', 'TSLA', 'GOOG']
    #clock_response=requests.get(clock)
    market_time_str = clock_response.json()['timestamp']
    market_time_str = market_time_str[:26] #+ market_time_str[market_time_str.find('-'):]  # Keep up to 6 fractional digits because Python doesn't support o
    market_time = datetime.fromisoformat(market_time_str)
    print(market_time)

    end_time=market_time-timedelta(minutes=15)
    start_time=end_time-timedelta(minutes=1)

    request_params=StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Minute,
        start=start_time.isoformat(),
        end=end_time.isoformat()
    )
    #this works like a charm IF THE MARKET IS OPEN, but today is Jimmy Carters Mourning day, soo...
    
    
    
    #return client.get_stock_latest_trade(symbol=symbol, feed='iex')
    return client.get_stock_bars(request_params)

def fetch(tickers,clock):
    market_time_str = clock.json()['timestamp']
    market_time_str = market_time_str[:26] #+ market_time_str[market_time_str.find('-'):]  # Keep up to 6 fractional digits because Python doesn't support o
    market_time = datetime.fromisoformat(market_time_str)
    
    end_time=market_time-timedelta(minutes=15)
    start_time=end_time-timedelta(minutes=1)

    request_params=StockBarsRequest(
        symbol_or_symbols=tickers,
        timeframe=TimeFrame.Minute,
        start=start_time.isoformat(),
        end=end_time.isoformat()
    )
    return client.get_stock_bars(request_params)

def add_positions(path, input_df):
    """
    Updates the positions CSV file by adding or modifying stock data.

    Args:
    - path (str): Path to the positions CSV file.
    - input_df (pd.DataFrame): DataFrame containing 'ticker', 'type', 'price', and 'qty' columns.
    """
    curr_df = pd.DataFrame()

    if os.path.exists(path):
        curr_df = pd.read_csv(path)
    else:
        # Create an empty DataFrame if the file doesn't exist
        curr_df = pd.DataFrame(columns=['ticker', 'price', 'currency', 'qty', 'type','last_price'])

    new_df = pd.DataFrame()
    for index, row in input_df.iterrows():
        if row['ticker'] in curr_df['ticker'][index]:
            if row['type'] == 'BUY':
                curr_df['price'][index] = curr_df['price'] * curr_df['qty'] + row['price'] * row['qty']
                curr_df['qty'][index] += row['qty']
                curr_df['price'][index] /= curr_df['qty']
            else:
                curr_df['qty'] -= row['qty']
    curr_df.join(row)

    curr_df.to_csv(path, index=False)

def update_prices(path):
    df=pd.read_csv(path)
    now=datetime.now()
    tickers=df['ticker'].to_list()
    clock_response=requests.get(clock_url,headers=headers)
    
    prices=fetch(tickers,clock_response)
    
    for i in prices['']:
        ...
    
    return prices
    
    
def get_total():
    total=0
    df=pd.read_csv(POSITIONS_PATH)
    updated_prices = update_prices(POSITIONS_PATH)
    df = df.merge(updated_prices, left_on='ticker', right_on='symbol', how='left')
    df['total_value'] = df['qty'] * df['close']
    total = df['total_value'].sum()
    
    return total
    
    
    
#Example
# check_stock = pd.DataFrame({
#     'ticker': ['AAPL'],
#     'price': [19.00],
#     'currency': ['$'],
#     'qty': [3.00],
#     'type': ['SELL']
#     'curr_price': [0.00]
#})

#check_stock.to_csv(POSITIONS_PATH, index=False)

#add_positions(POSITIONS_PATH, check_stock)

print(testfetch())