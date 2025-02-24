from ppi_client.api.constants import ACCOUNTDATA_TYPE_ACCOUNT_NOTIFICATION, ACCOUNTDATA_TYPE_PUSH_NOTIFICATION, \
    ACCOUNTDATA_TYPE_ORDER_NOTIFICATION
from ppi_client.ppi import PPI

import pandas as pd
import numpy as np
import os

from classes.account_ppi import Account
from classes.market_ppi import Market_data


def main():
    ppi = PPI(sandbox=False)    
    account = Account(ppi)
    #account.get_available_balance()
    market = Market_data(account.ppi)


    
    portfolio = {
        'PBR': {
            'type': 'CEDEARS',
            'transactions': [{'shares': 6, 'purchase_price': 16625},
                             {'shares': 5, 'purchase_price': 16325}
                             ]
        },
        'EWZ': {
            'type': 'CEDEARS',
            'transactions': [{'shares': 3, 'purchase_price': 14850}]
        }
        ,
        'NU': {
            'type': 'CEDEARS',
            'transactions': [{'shares': 4, 'purchase_price': 7970},
                             {'shares': 2, 'purchase_price': 6730}
                            ]
        }
        ,
        'BBD': {
            'type': 'CEDEARS',
            'transactions': [{'shares': 50, 'purchase_price': 2576},
                             {'shares': 20, 'purchase_price': 2460},
                             {'shares': 15, 'purchase_price': 2600}
                             ]
        },
        'MELI': {
            'type': 'CEDEARS',
            'transactions': [{'shares': 3, 'purchase_price': 24100}]
        }
    }

    total_purchase_cost = 0
    # +$13.000 primas por venta de opciones call
    # + 3.5 * 1220 que es el pago de intereses de GD41
    # +$189.094 ganados operando opciones
    # +$3.773  a favor con venta de deuda
    primes_gains = 3.5 * 1120 + 13000 + 189094 + 3773
    #100.000 total perdida de $METR
    total_current_value = -100000
    total_current_value += primes_gains
    

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
        print(f"  Gain/Loss%: {((current_value - purchase_cost) * 100 /purchase_cost):.2f}%")
        print("-" * 30)
        
     # Print portfolio totals
    print(f"Portfolio Total Purchase Cost: {total_purchase_cost:.2f}")
    print(f"Portfolio Current Value: {total_current_value:.2f}")
    print(f"Portfolio Dividends/primes/amortizations: {primes_gains:.2f}")
    print(f"Portfolio Gain/Loss: {total_current_value - total_purchase_cost:.2f}")
    print(f"Portfolio Porcentual Gain/Loss: {((total_current_value - total_purchase_cost) * 100 / total_purchase_cost):.2f}%")
    




if __name__ == '__main__':
    # windows
    # os.system("cls")
    # linux
    os.system("clear")
    
    main()