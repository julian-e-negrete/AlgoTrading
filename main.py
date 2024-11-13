import yfinance as yf
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib as plot
plot.use('Agg')

# Set up parameters
symbol = 'MELI'  # Ticker for Tesla (note this simulates the U.S. stock as an approximation)
end_date = dt.datetime(2024, 11, 24)  # End date for the simulation
num_simulations = 1000  # Number of simulation paths
num_days = (end_date - dt.datetime.now()).days  # Days into the future to simulate

# Fetch historical data for TSLA from yfinance (assuming a look-back period of 1 year)
data = yf.download(symbol, start=end_date - dt.timedelta(days=365), end=end_date)
closing_prices = data['Close']

# Calculate daily returns and the mean & standard deviation
daily_returns = closing_prices.pct_change().dropna()
mu = daily_returns.mean()
sigma = daily_returns.std()

# Monte Carlo simulation
simulated_prices = np.zeros((num_days, num_simulations))
##simulated_prices[0] = 19125  # Start from current price in ARS

for day in range(1, num_days):
    # Random daily change based on drift and volatility
    random_returns = np.random.normal(mu, sigma, num_simulations)
    simulated_prices[day] = simulated_prices[day - 1] * (1 + random_returns)

# Plot the simulation results
plt.figure(figsize=(10, 6))
plt.plot(simulated_prices)
plt.title("Monte Carlo Simulation of TSLA CEDEAR Price")
plt.xlabel("Days")
plt.ylabel("Price (ARS)")
plt.savefig("MELI.png")
plt.show()

