from ppi_client.api.constants import ACCOUNTDATA_TYPE_ACCOUNT_NOTIFICATION, ACCOUNTDATA_TYPE_PUSH_NOTIFICATION, \
    ACCOUNTDATA_TYPE_ORDER_NOTIFICATION
from ppi_client.ppi import PPI

import pandas as pd
import numpy as np



from datetime import datetime
import json
import traceback
import os

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from PPI.account_ppi import Account
from PPI.market_ppi import Market_data

from Opciones_class import Opciones

import QuantLib as ql


def main():
    ppi = PPI(sandbox=False)
    
    account = Account(ppi)
            
   
    market = Market_data(account.ppi)
    

    
     
    date_format = "%Y-%m-%d"

    start_date = datetime.strptime('2024-01-01', date_format)
    end_date = datetime.now()

    lst_historical = market.get_historical_data("METR","ACCIONES", "A-24HS", start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    df = pd.DataFrame(lst_historical)
    
    Opciones_class = Opciones(df, account, market)

    daily_volatility = Opciones_class.daily_volatility()
    annual_volatility = Opciones_class.annual_volatility()
    
    delta = len(Opciones_class.df['Daily Return'].dropna())        

    print(f"Desviación estándar diaria: {(daily_volatility * 100):.2f}%")
    print(f"Volatilidad en {delta} dias: {(annual_volatility * 100):.2f}%")
    

    
    
    
    

    precio_accion = market.get_market_data("METR", "ACCIONES", "A-24HS")


    # Define option parameters
    spot_price = precio_accion["price"]  # Current price of the stock
    strike_price = 3100  # Strike price
    expiry = ql.Date(21, 2, 2025)  # Expiry date
    risk_free_rate = 0.048  # 4.8% risk-free rate(1 year bond interes rate usa sovereign bonds)
    volatility = annual_volatility  
    
    risk_free_return = risk_free_rate / 252  # Tasa libre de riesgo diaria
    excess_return = Opciones_class.df['Daily Return'].mean() - risk_free_return
    sharpe_ratio = excess_return / Opciones_class.df['Daily Return'].std()

    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

    option_price , message = quantlib_option_price(spot_price, strike_price, expiry, risk_free_rate, volatility)
    
    print(message)
    total_value = strike_price * 100 + 2900 * 100
    #option_position = option_price * 100
    
    option_position = 20000
    
    # 2830 es el precio de compra de las acciones promedio
    tolerance_max = (2830 * 200 - option_position) / 200
    ganan_max = total_value + option_position
    
    print(f"valor minimo de accion en el cual se generan 0 ganancias: ${tolerance_max:.2f}")
    print(f"Ganancia maxima en venta en strike price + venta de primas: ${ganan_max:.2f} con una inversion de : ${2830 * 200}")
    print(f"Ganancia Nominal: ${(ganan_max - 2830*200):.2f}")
    print(f"la venta en strike price + primas es igual al precio de la accion evolucionando a : ${(ganan_max/200):.2f}")
    
    conditional_volatility, message  = Opciones_class.garch_model(delta)
    #print(message)

    volatility = conditional_volatility
    
    quantlib_option_price(spot_price, strike_price, expiry, risk_free_rate, volatility)
    
    
    
    
    
def quantlib_option_price(spot_price, strike_price, expiry, risk_free_rate, volatility):
    # Define option type
    payoff = ql.PlainVanillaPayoff(ql.Option.Call, strike_price)
    exercise = ql.EuropeanExercise(expiry)

    # Create option
    european_option = ql.VanillaOption(payoff, exercise)

    # Set up pricing engine
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
    rate_handle = ql.YieldTermStructureHandle(ql.FlatForward(0, ql.NullCalendar(), ql.QuoteHandle(ql.SimpleQuote(risk_free_rate)), ql.Actual360()))
    vol_handle = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(0, ql.NullCalendar(), ql.QuoteHandle(ql.SimpleQuote(volatility)), ql.Actual360()))
    process = ql.BlackScholesProcess(spot_handle, rate_handle, vol_handle)

    engine = ql.AnalyticEuropeanEngine(process)
    european_option.setPricingEngine(engine)
    

    
    return european_option.NPV(), f"Option Price: ${(european_option.NPV()):.2f}"
    
    

if __name__ == '__main__':
    os.system("cls")
    main()
