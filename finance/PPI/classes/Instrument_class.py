from ppi_client.api.constants import ACCOUNTDATA_TYPE_ACCOUNT_NOTIFICATION, ACCOUNTDATA_TYPE_PUSH_NOTIFICATION, \
    ACCOUNTDATA_TYPE_ORDER_NOTIFICATION
from ppi_client.ppi import PPI

import pandas as pd
import numpy as np

# GARCH MODEL
from arch import arch_model

# BLACK SCHOLES MODEL
from scipy.stats import norm
#Implied volatility
from scipy.optimize import brentq



import os


from classes.account_ppi import Account
from classes.market_ppi import Market_data

class Instrument:
    
    def __init__(self, df_p ) -> None:
        self.df = df_p
        self.structurate_df(self.df)
        self.risk_free_rate = 0.048 # usa sovereign bond interest rate
        
        
        
    def structurate_df(self, df_p):
        df_p['date'] = pd.to_datetime(df_p['date'])
        df_p.set_index('date', inplace=True)

        # Calcular los rendimientos diarios de los precios
        df_p['Daily Return'] = df_p['price'].pct_change()
        df_p['Daily Return'] = df_p['Daily Return'].fillna(0)
        
        self.df = df_p
        
    def Sharpe_ratio(self):
        risk_free_return = self.risk_free_rate / 252  # Tasa libre de riesgo diaria
        excess_return = self.df['Daily Return'].mean() - risk_free_return
        sharpe_ratio = excess_return / self.df['Daily Return'].std()
        
        return sharpe_ratio