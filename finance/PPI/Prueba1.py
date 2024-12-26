from ppi_client.api.constants import ACCOUNTDATA_TYPE_ACCOUNT_NOTIFICATION, ACCOUNTDATA_TYPE_PUSH_NOTIFICATION, \
    ACCOUNTDATA_TYPE_ORDER_NOTIFICATION
from ppi_client.models.account_movements import AccountMovements
from ppi_client.models.order import Order
from ppi_client.ppi import PPI
from ppi_client.models.instrument import Instrument
from datetime import datetime
import json
import traceback
import os


from account_ppi import Account 
from market_ppi import Market_data





def main():
    try:
        # Change sandbox variable to False to connect to production environment
        ppi = PPI(sandbox=False)
        
        # Change login credential to connect to the API
        #ppi.account.login_api('UG5kSHRnVlF5dVdQT2JQUGtRVlM=', 'YjA4MGM3ZjMtZGNmOS00NWU1LWIyZGEtMmQ4ZWM5MmZhOTA0')

        
        account = Account(ppi)
             
        # Get available balance
        #account.get_available_balance()
        
        
        #account.get_movements_by_date()
        
        
        
        market = Market_data(account.ppi)

        #market.get_instruments()
        
        #market.get_market_data("BA37D", "Bonos", "A-48HS")
        
        #market.get_instrument("BA37D", "Byma", "Bonos")
        
        # BA37D 100 ruedas a $76.300
        #market.estimate_bond("BA37D", 100, 76300)
        #market.search_current_book("BA37D", "Bonos","A-48HS" )
        
        market.add_instrument("CRES", "ACCIONES", "A-24HS")
        #market.add_instrument("YFCIO", "ON", "A-48HS")
        market.add_instrument("BA37D", "BONOS", "INMEDIATA")
        #market.add_instrument("AL30D", "BONOS", "INMEDIATA")
        #market.add_instrument("DLR/MAR25", "FUTUROS", "INMEDIATA")

        # Start the connection
        market.start()
        
        
        #market.get_instrument_realtime()
        
        # Set up and start real-time market data connection
        #setup_market_data_realtime()
        #ppi.realtime.start_connections()

    except Exception as e:
        print(datetime.now())
        print(f"ERROR: '{e}' ")


if __name__ == '__main__':
    os.system("cls")
    main()
