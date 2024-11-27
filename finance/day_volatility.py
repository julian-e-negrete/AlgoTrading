import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def get_daily_volatility_and_mean_return(stock_ticker, date, window=30):
    """
    Calculate the volatility and mean return of a stock around a specific date.

    Args:
        stock_ticker (str): The stock ticker symbol (e.g., "AAPL").
        date (str): The date for analysis in YYYY-MM-DD format.
        window (int): The number of days to calculate historical statistics (default: 30).

    Returns:
        dict: A dictionary with the daily return, mean return, and volatility.
    """
    # Fetch historical daily data
    end_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    
   
        
    data = yf.download(tickers=stock_ticker, start=end_date, period="1d")
    
    
    
    # Check if data is available
    if data.empty:
        return {"error": f"No daily data available for {stock_ticker}."}
    
    data.columns = data.columns.droplevel(1)
    df = pd.DataFrame(data)
    columns_values_list = df[["Close"]].values.tolist()
    print(columns_values_list)
    sum_close = 0
    for i in range(0,len(columns_values_list)):
        if (i == 0): continue;
        sum_close += (columns_values_list[i][0] - columns_values_list[i-1][0])  / columns_values_list[i-1][0] 
    
    print(sum_close)
    sum_close = df["Close"].sum()
    sum_open = df["Open"].sum()
    
    # Calculate daily returns
    data['Return'] = data['Adj Close'].pct_change()
    mean_return = (sum_close - sum_open) / sum_open 
    """
    print("\n \n")
    print(f"{mean_return* 100}%")
    # Extract the return for the specified date
    """
    try:
        daily_return = data.loc[datetime.today(), 'Return']
    except KeyError:
        return {"error": f"No data available for {stock_ticker} on {date}."}
    """
    # Calculate mean return and volatility over the historical window
    #mean_return = data['Return'].mean()
    volatility = data['Return'].std()
    
    return {
        #"Daily Return": daily_return,
        "Mean Return (Window)": mean_return,
        "Volatility (Window)": volatility
    }
    """

os.system("cls")

# Example usage
stock_ticker = "YPFD.BA"  # Replace with the stock ticker
date = "2024-11-20"    # Replace with the desired date
results = get_daily_volatility_and_mean_return(stock_ticker, date)
"""
print(f"Results for {stock_ticker} on {date}:")
print(results)
"""