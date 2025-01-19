from ppi_client.api.constants import ACCOUNTDATA_TYPE_ACCOUNT_NOTIFICATION, ACCOUNTDATA_TYPE_PUSH_NOTIFICATION, \
    ACCOUNTDATA_TYPE_ORDER_NOTIFICATION
from ppi_client.ppi import PPI

import pandas as pd
import numpy as np



from datetime import datetime
import json
import traceback
import sys
import os

# Dynamically add the parent directory (PPI) to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

# Now import the required modules

from classes import Account, Market_data, Instrument, Opciones

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
    strike_price = 2900  # Strike price
    expiry = ql.Date(21, 2, 2025)  # Expiry date
    risk_free_rate = 0.048  # 4.8% risk-free rate(1 year bond interes rate usa sovereign bonds)
    volatility = annual_volatility  
    
    # Sharpe Ratio
    sharpe_ratio = Opciones_class.instrument_cl.Sharpe_ratio()

    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

    option_price , message = quantlib_option_price(spot_price, strike_price, expiry, risk_free_rate, volatility)
    
    print(message)
    total_value = 3100 * 100 + 2900 * 100
    #option_position = option_price * 100
    
    # calculo en base a la compra de una opcion put de venta en 2700(2720 es la tolerancia maxima)
    # 6761 * 100 
    option_position = 20000  
    
    # 2830 es el precio de compra de las acciones promedio
    tolerance_max = (2830 * 200 - option_position) / 200
    dif_porc = (((spot_price - tolerance_max) * 100 / spot_price) * -1)
    ganan_max = total_value + option_position
    
    print(f"valor minimo de accion en el cual se generan 0 ganancias: ${tolerance_max:.2f}, \npor lo tanto la accion deberia sufrir una baja del: {dif_porc:.2f}%")
    print(f"Ganancia maxima en venta en strike price + venta de primas: ${ganan_max:.2f} con una inversion de : ${2830 * 200}")
    print(f"Ganancia Nominal: ${(ganan_max - 2830*200):.2f}, +{((ganan_max - 2830*200) * 100 / (2830*200)):.2f}%") 
    print(f"la venta en strike price + primas es igual al precio de la accion evolucionando a : ${(ganan_max/200):.2f}")
    
    conditional_volatility, message  = Opciones_class.garch_model(delta)
    
    #print(message)

    volatility = conditional_volatility
    
    quantlib_option_price(spot_price, strike_price, expiry, risk_free_rate, volatility)
    
    # El valor nocional es el precio del subyacente multiplicado por el tamaño del contrato.(el tamaño de los contratos es por cada opcion 100 acciones subyacentes)
    valor_nocional = 2920 * 100
    print("\n \nGarantia necesaria para la posicion actual: ")
    print(f"\nGarantia sobre la posicion de venta de METC2900FE: ${(valor_nocional * 0.21):.2f}")
    print(f"Garantia sobre la posicion de venta de METC3100FE: ${(valor_nocional * 0.10):.2f}\n")
    
    print(f"Garantia Total: ${(valor_nocional * 0.21 + valor_nocional * 0.10):.2f}")
    
    
    
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
