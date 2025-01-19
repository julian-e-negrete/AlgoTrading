from ppi_client.api.constants import ACCOUNTDATA_TYPE_ACCOUNT_NOTIFICATION, ACCOUNTDATA_TYPE_PUSH_NOTIFICATION, \
    ACCOUNTDATA_TYPE_ORDER_NOTIFICATION
from ppi_client.ppi import PPI

import pandas as pd


from datetime import datetime
import json
import traceback
import os


from finance.PPI.classes.account_ppi import Account 
from finance.PPI.classes.market_ppi import Market_data





def main():
    try:
        # Change sandbox variable to False to connect to production environment
        ppi = PPI(sandbox=False)
        
        # Change login credential to connect to the API
        #ppi.account.login_api('UG5kSHRnVlF5dVdQT2JQUGtRVlM=', 'YjA4MGM3ZjMtZGNmOS00NWU1LWIyZGEtMmQ4ZWM5MmZhOTA0')

        
        account = Account(ppi)
             
        # Get available balance
        account.get_available_balance()
        
        account.get_active_orders()
        
        
        #account.get_movements_by_date()
        
        
        
        market = Market_data(account.ppi)
        
        market.add_instrument("BA37D", "BONOS", "INMEDIATA")
        #market.add_instrument("BB37D", "BONOS", "INMEDIATA")
        # Start the connection
        market.start()
        
        """
        #market.get_market_data("BA37D", "Bonos", "A-48HS")
        
        #market.get_instrument("BA37D", "Byma", "Bonos")
        
        # BA37D 100 ruedas a $76.300
        #market.estimate_bond("BA37D", 100, 76300)
        #market.search_current_book("BA37D", "Bonos","A-48HS" )
        
        #market.add_instrument("CRES", "ACCIONES", "A-24HS")
        #market.add_instrument("YFCIO", "ON", "A-48HS")

        #market.add_instrument("AL30D", "BONOS", "INMEDIATA")
        #market.add_instrument("DLR/MAR25", "FUTUROS", "INMEDIATA")
        
        market.get_intraday_market_data("YPFD", "Acciones", "A-48HS")
        dict_historical : dict= market.get_historical_data("BB37D", "Bonos", "A-48HS")
        
        

        # Create a DataFrame
        df = pd.DataFrame(dict_historical)

        # Display the DataFrame
        print(df.describe())

        # Perform operations as a datatable
        
        print("\nFiltered data (price > 1480):")
        filtered_df = df[df["price"] > 1480]
        print(filtered_df)
        
        
        # Sort by date
        print("\nSorted by date:")
        sorted_df = df.sort_values(by="date", ascending=False)
        print(sorted_df)

        """



    except Exception as e:
        print(datetime.now())
        print(f"ERROR: '{e}' ")



def calculo_variacion_opciones():
     # Change sandbox variable to False to connect to production environment
        ppi = PPI(sandbox=False)
        
        # Change login credential to connect to the API
        #ppi.account.login_api('UG5kSHRnVlF5dVdQT2JQUGtRVlM=', 'YjA4MGM3ZjMtZGNmOS00NWU1LWIyZGEtMmQ4ZWM5MmZhOTA0')

        
        account = Account(ppi)
             
       
        
        
        
        market = Market_data(account.ppi)
        market.get_instrument()
        #market.get_historical_data()


if __name__ == '__main__':
    os.system("cls")
    main()
