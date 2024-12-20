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

        account = Account(ppi)
             
        # Get available balance
        #account.get_available_balance()
        
        
        #account.get_movements_by_date()
        
        
        
        market = Market_data(account.ppi)

        market.get_instruments()
        
        market.get_market_data()
        
        market.get_instrument()
        
        market.get_instrument_realtime()
        
        # Set up and start real-time market data connection
        #setup_market_data_realtime()
        #ppi.realtime.start_connections()

    except Exception as e:
        print(datetime.now())
        print(e)


if __name__ == '__main__':
    os.system("cls")
    main()
