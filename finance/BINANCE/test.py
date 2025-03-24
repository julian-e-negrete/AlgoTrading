from binance.client import Client
from binance.enums import *
import pandas as pd
import matplotlib.pyplot as plt
import time
import mplfinance as mpf


API_KEY = '60H2cfydHlhKryRGJbCwWbqbX7lNMAVQjRmier9gy5mx8o0HnlRkRVkKNR7DG9Vr'
API_SECRET = 'C2Y9ky5SNnqYzmQIUCPOLnEKuF4XX74jqVvE3VyLfGdRqCEHoCmP27pGShVDG4U4'

client = Client(API_KEY, API_SECRET)


exchange_info = client.get_exchange_info()
symbols = [s['symbol'] for s in exchange_info['symbols']]


if('USDTARS' in symbols):   # Check availability
    

    # Example: Get 1-hour candles for USDTARS for last 7 days
    klines = client.get_klines(symbol='USDTARS', interval=Client.KLINE_INTERVAL_1HOUR, limit=168)

    # Convert to DataFrame
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 
        'close_time', 'quote_asset_volume', 'num_trades', 
        'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)

    print(df.tail())
    
    
    # Graphical analysis
    """
    plt.figure(figsize=(12,6))
    plt.plot(df.index, df['close'], label='USDTARS Close Price')
    plt.title('USDT/ARS Price - 1H Interval')
    plt.xlabel('Time')
    plt.ylabel('Price in ARS')
    plt.grid(True)
    plt.legend()
    plt.show()
    """
    # candle sticks
    mpf.plot(df, type='candle', style='charles', volume=True, title='USDT/ARS')


else:
    print("no avalaible")