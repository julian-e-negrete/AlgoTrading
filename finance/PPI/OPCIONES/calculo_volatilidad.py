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






def main():
    try:
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
        


        #print(df.describe())
        lst_historical = market.get_historical_data("METR","BONOS", "A-24HS", "2024-01-01", "2025-01-02")
        df = pd.DataFrame(lst_historical)
        #print(df.columns)
        
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        # Calcular los rendimientos diarios de los precios
        df['Daily Return'] = df['price'].pct_change()

        # Calcular la desviación estándar de los rendimientos diarios
        daily_volatility = df['Daily Return'].std()

        # Calcular la volatilidad anualizada
        annual_volatility = daily_volatility * np.sqrt(252)  # 252 días de negociación en un año

        print(f"Desviación estándar diaria: {(daily_volatility * 100):.2f}%")
        print(f"Volatilidad anualizada: {(annual_volatility * 100):.2f}%")



    except Exception as e:
        print(datetime.now())
        print(f"ERROR: '{e}' ")





if __name__ == '__main__':
    os.system("cls")
    main()
