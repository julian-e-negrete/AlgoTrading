from ppi_client.api.constants import ACCOUNTDATA_TYPE_ACCOUNT_NOTIFICATION, ACCOUNTDATA_TYPE_PUSH_NOTIFICATION, \
    ACCOUNTDATA_TYPE_ORDER_NOTIFICATION
from ppi_client.ppi import PPI

import pandas as pd
import numpy as np
import os

from account_ppi import Account
from market_ppi import Market_data


def main():
    ppi = PPI(sandbox=False)    
    account = Account(ppi)
    #account.get_available_balance()
    market = Market_data(account.ppi)


    
    portfolio = {
        'GGAL': {
            'type': 'ACCIONES',
            'transactions': [{'shares': 5, 'purchase_price': 8460}]
        },
        'METR': {
            'type': 'ACCIONES',
            'transactions': [
                {'shares': 73, 'purchase_price': 2740},
                {'shares': 27, 'purchase_price': 2904},
                {'shares': 100, 'purchase_price': 2879.21}
                
            ]
        },
        'BBD': {
            'type': 'CEDEARS',
            'transactions': [{'shares': 11, 'purchase_price': 2330}]
        },
        'NU': {
            'type': 'CEDEARS',
            'transactions': [{'shares': 4, 'purchase_price': 6680}]
        },
        'BA37D': {
            'type': 'BONOS',
            'transactions': [
                {'shares': 1, 'purchase_price': 78000},
                {'shares': 0.98, 'purchase_price': 76531}
            ]
        }
    }

    total_purchase_cost = 0
    # 20.000 base gracias a la venta de opciones de compra de METR(METC2900FE) por 20.000(precio de la prima: ~$211.68) 
    # + 3.5 * 1220 que es el pago de intereses de GD41
    total_current_value = 20000 
    

    for ticker, details in portfolio.items():
        instrument_type = details['type']
        transactions = details['transactions']

        # Aggregate shares and weighted average purchase price
        total_shares = sum(t['shares'] for t in transactions)
        weighted_avg_price = np.average(
            [t['purchase_price'] for t in transactions],
            weights=[t['shares'] for t in transactions],
        )
        current_price = market.get_market_data(ticker, instrument_type, "A-24HS")
        current_price = current_price["price"]
        # Calculate current value and cost
        current_value = total_shares * current_price
        purchase_cost = total_shares * weighted_avg_price

        # Add to totals
        total_current_value += current_value
        total_purchase_cost += purchase_cost

        # Print details for each asset
        print(f"{ticker} ({instrument_type}):")
        print(f"  Total Shares: {total_shares}")
        print(f"  Weighted Avg Purchase Price: {weighted_avg_price:.2f}")
        print(f"  Current Price: {current_price}")
        print(f"  Purchase Cost: {purchase_cost:.2f}")
        print(f"  Current Value: {current_value:.2f}")
        print(f"  Gain/Loss: {current_value - purchase_cost:.2f}")
        print("-" * 30)
        
     # Print portfolio totals
    print(f"Portfolio Total Purchase Cost: {total_purchase_cost:.2f}")
    print(f"Portfolio Current Value: {total_current_value:.2f}")
    print(f"Portfolio Gain/Loss: {total_current_value - total_purchase_cost:.2f}")
    print(f"Portfolio Porcentual Gain/Loss: {((total_current_value - total_purchase_cost) * 100 / total_purchase_cost):.2f}%")
    




if __name__ == '__main__':
    os.system("cls")
    main()