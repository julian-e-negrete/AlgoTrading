from ppi_client.api.constants import ACCOUNTDATA_TYPE_ACCOUNT_NOTIFICATION, ACCOUNTDATA_TYPE_PUSH_NOTIFICATION, \
    ACCOUNTDATA_TYPE_ORDER_NOTIFICATION
from ppi_client.ppi import PPI

import pandas as pd


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
        account.get_available_balance()
        
        account.get_active_orders()
        

        
        
        
        market = Market_data(account.ppi)


    except Exception as e:
        print(datetime.now())
        print(f"ERROR: '{e}' ")





if __name__ == '__main__':
    os.system("cls")
    main()
