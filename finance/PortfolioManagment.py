import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import os
import pandas as pd
from datetime import datetime, timedelta

#import matplotlib
#matplotlib.use('Agg')  # Use non-interactive backend

# Get the current working directory
path = os.getcwd()

# Define your portfolio with shares and purchase prices
portfolio = {
    'MELI.BA': {'shares': 2, 'purchase_price': 18300},  
    'TSLA.BA': {'shares': 1, 'purchase_price': 26600},         
    'AMZN.BA': {'shares': 2, 'purchase_price': 1706}
}
# Monte Carlo Simulation Parameters
days = 126  # Number of trading days in 6 months
simulations = 100000  # Number of simulations

# Initialize results for portfolio risk management
portfolio_results = []
portfolio_simulations = []  # Store total portfolio values for all simulations

# Loop through each stock in the portfolio
for ticker, details in portfolio.items():
    shares = details['shares']
    purchase_price = details['purchase_price']
    print(f"Processing {ticker}...")

    # Fetch historical data
    csv_filename = f'{path}\\csv\\{ticker}_data.csv'
    try:
        data = yf.download(ticker, start='2024-01-01', end=datetime.Today())
        if data.empty:
            raise ValueError(f"No data available for {ticker}")
    except Exception as e:
        print(f"Error downloading data for {ticker}: {e}")
        continue

    
    data.to_csv(csv_filename)

    # Calculate daily returns
    data['Daily Return'] = data['Adj Close'].pct_change()

    # Calculate mean and volatility from historical data in ARS
    data['Log Return'] = np.log(data['Adj Close'] / data['Adj Close'].shift(1))
    mu = data['Log Return'].mean() * 252  # Annualized log return
    sigma = data['Log Return'].std() * np.sqrt(252)  # Annualized volatility

    data.columns = data.columns.droplevel(1)  # Drop the 'Price' level in the multi-level columns

    # Get the last stock price
    initial_stock_price = data['Adj Close'][-1]
    if np.isnan(initial_stock_price):  # Handle case where data might be missing
        print(f"Skipping {ticker} due to insufficient data.")
        continue

    # Monte Carlo simulation
    final_values = []
    for _ in range(simulations):
        # Simulate daily returns over 126 days
        daily_returns = np.random.normal(mu / days, sigma / np.sqrt(days), days)
        # Calculate the stock price over time
        stock_price = initial_stock_price * np.cumprod(1 + daily_returns)[-1]
        final_values.append(stock_price)

    # Convert final values into a numpy array for analysis
    final_values = np.array(final_values)

    # Add the total value of this stock (price * shares) to the portfolio simulations
    portfolio_simulations.append(final_values * shares)

    # Calculate statistics
    mean_final_price = np.mean(final_values)
    percentile_5 = np.percentile(final_values, 5)  # 5th percentile (Value-at-Risk)
    percentile_95 = np.percentile(final_values, 95)  # 95th percentile

    # Assess total value of shares based on Monte Carlo results
    mean_total_value = mean_final_price * shares
    purchase_value = purchase_price * shares
    risk_value_at_5th_percentile = percentile_5 * shares

    # Save results for the portfolio
    portfolio_results.append({
        'Ticker': ticker,
        'Shares': shares,
        'Purchase Price per Share': purchase_price,
        'Purchase Total Value': purchase_value,
        'Mean Final Price per Share': mean_final_price,
        'Mean Total Value': mean_total_value,
        '5th Percentile Total Value (VaR)': risk_value_at_5th_percentile,
        '95th Percentile Price per Share': percentile_95,
    })

    # Plot the histogram of final stock prices
    plt.hist(final_values, bins=50, edgecolor='black')
    plt.title(f"Monte Carlo Simulation: {ticker} Stock Price Distribution")
    plt.xlabel("Stock Price (ARS)")
    plt.ylabel("Frequency")
    plt.savefig(f"{path}\\png\\{ticker}_Histogram.png")
    plt.close()  # Close the plot to free memory

    print(f"{ticker} - Simulation complete.")
    print("-" * 50)

# Combine all simulations into total portfolio value
portfolio_final_values = np.sum(portfolio_simulations, axis=0)

# Plot the histogram of portfolio values
plt.figure(figsize=(10, 6))
plt.hist(portfolio_final_values, bins=50, edgecolor='black', alpha=0.7)
plt.title("Monte Carlo Simulation: Portfolio Value Distribution")
plt.xlabel("Portfolio Value (ARS)")
plt.ylabel("Frequency")
plt.axvline(np.percentile(portfolio_final_values, 5), color='r', linestyle='dashed', linewidth=1.5, label="5th Percentile (VaR)")
plt.axvline(np.mean(portfolio_final_values), color='g', linestyle='dashed', linewidth=1.5, label="Mean Portfolio Value")
plt.axvline(np.percentile(portfolio_final_values, 95), color='b', linestyle='dashed', linewidth=1.5, label="95th Percentile")
plt.legend()
plt.grid()



# Create a summary DataFrame for portfolio results
portfolio_df = pd.DataFrame(portfolio_results)

# Display portfolio summary
print(portfolio_df)

# Calculate total portfolio metrics
total_purchase_value = portfolio_df['Purchase Total Value'].sum()
total_mean_value = portfolio_df['Mean Total Value'].sum()
total_risk_value_at_5th_percentile = portfolio_df['5th Percentile Total Value (VaR)'].sum()

print("\nPortfolio Summary:")
print(f"Total Purchase Value: ${total_purchase_value:,.2f} ARS")
print(f"Total Mean Simulated Value: ${total_mean_value:,.2f} ARS")
print(f"Total Value-at-Risk (5th Percentile): ${total_risk_value_at_5th_percentile:,.2f} ARS")

plt.savefig(f"{path}\\png\\Portfolio_MonteCarlo_Histogram.png")

plt.show()
plt.close()  # Close the plot to free memory
# Save the portfolio results to a CSV file
portfolio_df.to_csv(f"{path}\\csv\\portfolio_results.csv", index=False)

