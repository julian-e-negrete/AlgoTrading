import yfinance as yf
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib as plot
plot.use('Agg')


# Set up parameters
symbol = 'MELI'  # Ticker for TSLA CEDEAR in Buenos Aires (ARS)
num_simulations = 1000  # Number of simulation paths
future_days = 30  # Days to project into the future

# Fetch historical data for TSLA.BA (CEDEAR) from yfinance (last 1 year)
data = yf.download(symbol, period="1y")

# Check if data is available
if data.empty:
    print("No data found for the given period.")
else:
    # Get the opening price of the most recent trading day as the start price
    start_price = data['Open', symbol].iloc[-1]  
    print(f"Start price: {start_price}")

    # Calculate daily returns based on historical prices
    closing_prices = data['Close', symbol]
    daily_returns = closing_prices.pct_change().dropna()

    # Monte Carlo simulation based on historical daily returns
    simulated_prices = np.zeros((future_days, num_simulations))
    simulated_prices[0] = start_price  # Start from the opening price

    for sim in range(num_simulations):
        for day in range(1, future_days):
            # Sample a daily return from historical data
            daily_return = np.random.choice(daily_returns)
            simulated_prices[day, sim] = simulated_prices[day - 1, sim] * (1 + daily_return)

    # Plot the simulation results
    plt.figure(figsize=(10, 6))
    plt.plot(simulated_prices)
    plt.title(f"Monte Carlo Simulation of {symbol} CEDEAR Price (based on Historical Returns)")
    plt.xlabel("Days")
    plt.ylabel("Price (ARS)")
    plt.show()
    plt.savefig(f"{symbol}.png")

