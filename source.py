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
    print(input_df)
    curr_df = pd.DataFrame()

    if os.path.exists(path):
        curr_df = pd.read_csv(path)
    else:
        # Create an empty DataFrame if the file doesn't exist
        curr_df = pd.DataFrame(columns=['ticker', 'price', 'currency', 'qty', 'type','last_price'])

    for index, row in input_df.iterrows():
        if row['ticker'] in curr_df['ticker'].values:
            curr_index = curr_df[curr_df['ticker'] == row['ticker']].index[0]
            if row['type'].upper() == 'BUY':
                curr_df.at[curr_index, 'price'] = (curr_df.at[curr_index, 'price'] * curr_df.at[curr_index, 'qty'] + row['price'] * row['qty']) / (curr_df.at[curr_index, 'qty'] + row['qty'])
                curr_df.at[curr_index, 'qty'] += row['qty']
                if curr_df.at[curr_index, 'qty'] == 0:
                    curr_df.drop(curr_index, inplace=True)
            else:
                curr_df.at[curr_index, 'qty'] -= row['qty']
                if curr_df.at[curr_index, 'qty'] == 0:
                    curr_df.drop(curr_index, inplace=True)
        else:
            curr_df = pd.concat([curr_df, pd.DataFrame([row])], ignore_index=True)

    curr_df.to_csv(path, index=False)

def update_prices(path):
    df=pd.read_csv(path)
    now=datetime.now()
    tickers=df['ticker'].to_list()
    clock_response=requests.get(clock_url,headers=headers)
    
    prices=fetch(tickers,clock_response)
    used=pd.DataFrame(prices[['symbol','close']])
    
    for idx, row in used.iterrows():
        df.loc[df['ticker'] == row['symbol'], 'last_price'] = row['close']
    
    
def get_total():
    entry_total = 0
    curr_total = 0
    df=pd.read_csv(POSITIONS_PATH)
    update_prices(POSITIONS_PATH)
    for idx, row in df.iterrows():
        entry_total+=row['price']*row['qty']
        curr_total+=row['last_price']*row['qty']
    
    return (entry_total,curr_total)
    
    
    
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

#print(testfetch())