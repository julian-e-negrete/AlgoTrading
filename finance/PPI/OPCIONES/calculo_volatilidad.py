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


from datetime import datetime
import json
import traceback
import os

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from PPI.account_ppi import Account
from PPI.market_ppi import Market_data






def main():
    # Change sandbox variable to False to connect to production environment
    ppi = PPI(sandbox=False)
    
    account = Account(ppi)
            
    # Get available balance
    #account.get_available_balance()
    
    #account.get_active_orders()
    

    
    
    
    market = Market_data(account.ppi)
    #con esto puedo obtener todos los instrumentos que esten relacionados a esos parametros
    #lst_opciones = market.get_instrument("MET","BYMA", "ACCIONES")
    """
    
    
    df = pd.DataFrame(lst_opciones)
    
    headers = df.columns
    
    for i in df["ticker"]:
        market.get_market_data(i, "OPCIONES", "A-72")
        #market.search_current_book(i,"OPCIONES","A-24HS")
        #market.get_historical_data(i,"OPCIONES", "A-24HS", "2024-12-01", "2024-12-31")
    """    
    
    from datetime import datetime
    date_format = "%Y-%m-%d"

    start_date = datetime.strptime('2024-01-01', date_format)
    end_date = datetime.now()

    
    
    #print(df.describe())
    lst_historical = market.get_historical_data("METR","ACCIONES", "A-24HS", start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    df = pd.DataFrame(lst_historical)
    #print(df.columns)
    
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Calcular los rendimientos diarios de los precios
    df['Daily Return'] = df['price'].pct_change()
    df['Daily Return'] = df['Daily Return'].fillna(0)  # Replace NaN with 0 or any other value you prefer
    
    delta = len(df['Daily Return'].dropna())  # Number of valid trading days in the period

    # Calcular la desviación estándar de los rendimientos diarios
    daily_volatility = df['Daily Return'].std()

    # Calcular la volatilidad anualizada
    annual_volatility = daily_volatility * np.sqrt(delta)  # 252 días de negociación en un año
    
    
    sigma  = garch_model(df, delta)
    
    print(f"Desviación estándar diaria: {(daily_volatility * 100):.2f}%")
    print(f"Volatilidad en {delta} dias: {(annual_volatility * 100):.2f}%")
    
    
    
    S = 2790  # Precio actual de la acción (en pesos)
    K = 2900  # Precio de ejercicio (en pesos)
    days_to_expiry = 44  # Días hasta el vencimiento
    r = 0.048  # Tasa libre de riesgo (4.8% anual, en proporción) sovereing bonds interest rate in a year
    T = days_to_expiry / 365  # Tiempo hasta el vencimiento en años 
    market_price = 145  # Prima observada en el mercado
    
    call_price = black_scholes_model(S, K, T, r, annual_volatility)
    #print(f"Volatilidad condicional para el vencimiento: {sigma * 100:.2f}%")
    print(f"Precio de la opción Call: {call_price:.2f} pesos")
    # Calcular la volatilidad implícita
    iv = implied_volatility_call(S, K, T, r, market_price)
    print(f"Volatilidad implícita: {iv * 100:.2f}%")
    

    try:
        print("------")

    except Exception as e:
        print(datetime.now())
        print(f"ERROR: '{e}' ")




"""
calculo del modelo garch para la volatilidad
    
"""
def garch_model(df_p, delta_p):
    df_p['Scaled Return'] = df_p['Daily Return'] * 10
    
    # Modelo GARCH(1, 1)
    model = arch_model(df_p['Scaled Return'], vol='Garch', p=1, q=1, dist='normal')
    garch_fit = model.fit(disp="off")

    # Obtener la volatilidad condicional anualizada
    daily_garch_volatility = garch_fit.conditional_volatility / 10
    annual_garch_volatility = daily_garch_volatility.iloc[-1] * np.sqrt(delta_p ** 0.5)

    print(f"Volatilidad condicional (GARCH, en {delta_p} dias): {(annual_garch_volatility * 100):.2f}%")
    return annual_garch_volatility

    
    
        

def black_scholes_model(S, K, T, r, sigma):
    """
    Calcula el precio de una opción Call usando el modelo Black-Scholes.
    S: Precio del subyacente
    K: Precio de ejercicio
    T: Tiempo hasta el vencimiento en años
    r: Tasa libre de riesgo
    sigma: Volatilidad anualizada
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def implied_volatility_call(S, K, T, r, market_price):
    """ Calcula la volatilidad implícita usando Black-Scholes y el precio de mercado """
    def difference(sigma):
        return black_scholes_model(S, K, T, r, sigma) - market_price
    
    # Buscar sigma que minimice la diferencia
    try:
        iv = brentq(difference, 1e-5, 5)  # Buscamos entre valores razonables de sigma
        return iv
    except ValueError:
        return np.nan
    



if __name__ == '__main__':
    os.system("cls")
    main()
