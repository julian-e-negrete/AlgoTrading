# Imports 
from ppi_client.ppi import PPI

from ppi_client.models.instrument import Instrument
from datetime import datetime
from ppi_client.models.estimate_bonds import EstimateBonds
import json
import traceback




class Market_data:
    
    def __init__(self, P_ppi ) -> None:
        self.ppi = P_ppi
        
        
    #region master
    
    
    #region types of
    def get_instruments(self):
        # Getting instrument types
        print("\nGetting instrument types")
        instruments = self.ppi.configuration.get_instrument_types()
        for item in instruments:
            print(item)
            
            
            
    def get_markets(self):
        # Getting markets
        print("\nGetting markets")
        markets = self.ppi.configuration.get_markets()
        for item in markets:
            print(item)
            
            
    def get_settlements(self):
        # Getting settlements
        print("\nGetting settlements")
        settlements = self.ppi.configuration.get_settlements()
        for item in settlements:
            print(item)
            
            
    def get_quantity_types(self):
        # Getting quantity types
        print("\nGetting quantity types")
        quantity_types = self.ppi.configuration.get_quantity_types()
        for item in quantity_types:
            print(item)
            

    def get_operation_terms(self):
        # Getting operation terms
        print("\nGetting operation terms")
        operation_terms = self.ppi.configuration.get_operation_terms()
        for item in operation_terms:
            print(item)
            
            
    def get_operations(self):
        # Getting operations
        print("\nGetting operations")
        operations = self.ppi.configuration.get_operations()
        for item in operations:
            print(item)
            
    #endregion
    
    #region holidays        
    def get_holidays(self):
        # Get holidays
        print("\nGet local holidays for the current year")
        holidays = self.ppi.configuration.get_holidays(start_date=datetime(2022, 1, 1), end_date=datetime(2022, 12, 31))
        for holiday in holidays:
            print("%s - %s " % (holiday["date"][0:10], holiday["description"]))
        
        print("\nGet USA holidays for the current year")
        holidays = self.ppi.configuration.get_holidays(start_date=datetime(2022, 1, 1), end_date=datetime(2022, 12, 31),
                                                  is_usa=True)
        for holiday in holidays:
            print("%s - %s " % (holiday["date"][0:10], holiday["description"]))
    
    
    
    def isHoliday (self) -> bool:
        # Check holidays
        print("\nIs today a local holiday?")
        print(self.ppi.configuration.is_local_holiday())
        print("\nIs today a holiday in the USA?")
        print(self.ppi.configuration.is_usa_holiday())
    
    #endregion   
    
    
    #endregion     
            
            
            
    #region search
    
    
    #search instrument, get all that is related to that instrument
    def get_instrument(self):
        # Search Instrument
        print("\nSearching instruments")
        instruments = self.ppi.marketdata.search_instrument("YPFD", "", "Byma", "Acciones")
        for ins in instruments:
            print(ins)
            
            
    def search_current_book(self):
        # Search Current Book
        print("\nSearching Current Book")
        current_book = self.ppi.marketdata.book("GGAL", "Acciones", "A-48HS")
        print(current_book)
    
    # search historic market data
    def get_historical_data(self):
        print("\nSearching MarketData")
        ticker = input("ingrese el ticker que quiere buscar: ")
        
        while True:
            date_input = input("Enter start date (YYYY-MM-DD): ")
            date_input2 = input("Enter end date (YYYY-MM-DD): ")
            try:
                # Try to parse the input into a datetime object
                start_date = datetime.strptime(date_input, "%Y-%m-%d")
                end_date = datetime.strptime(date_input2, "%Y-%m-%d")
                
                break  # Exit the loop if the date is valid
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")


        market_data = self.ppi.marketdata.search(ticker.upper(), "Acciones", "A-48HS", start_date, end_date)
        for ins in market_data:
            print("%s - %s - Volume %s - Opening %s - Min %s - Max %s" % (
                ins['date'], ins['price'], ins['volume'], ins['openingPrice'], ins['min'], ins['max']))
    
    
    
    # Search Current MarketData        
    def get_market_data(self):
        ticker = input("ingrese el ticker que quiere buscar: ")
        print("\nSearching Current MarketData")
        current_market_data = self.ppi.marketdata.current(ticker.upper(), "Acciones", "A-48HS")
        print(ticker.upper())
        print("-----------------------------------------")
        #print(f"Precio: {current_market_data["price"]} \nVolumen: {current_market_data["volume"]}  \nopen: {current_market_data["openingPrice"]} \nMAX: {current_market_data["max"]}  \nMIN: {current_market_data["min"]} \nmarket change: {current_market_data["marketChangePercent"]} ")
        
        
    # Search intraday data
    def get_intraday_market_data(self):
        # Search Intraday MarketData
        print("\nSearching Intraday MarketData")
        intraday_market_data = self.ppi.marketdata.intraday("GGAL", "Acciones", "A-48HS")
        for intra in intraday_market_data:
            print(intra)
               
    #endregion
    
    
    def estimate_bond(self):
        print("\nEstimate bond")
        estimate = self.ppi.marketdata.estimate_bonds(EstimateBonds(ticker="CUAP", date=datetime.today(), 
        quantityType="PAPELES", quantity=100, price=4555))
        print(estimate)
        
    #region realtime
    
    # Realtime subscription to market data
    def onconnect_marketdata(self):
        try:
            print("\nConnected to realtime market data")
            self.ppi.realtime.subscribe_to_element(Instrument("GGAL", "ACCIONES", "A-48HS"))
            self.ppi.realtime.subscribe_to_element(Instrument("AAPL", "CEDEARS", "A-48HS"))
            self.ppi.realtime.subscribe_to_element(Instrument("AL30", "BONOS", "INMEDIATA"))
            self.ppi.realtime.subscribe_to_element(Instrument("AL30D", "BONOS", "INMEDIATA"))
            self.ppi.realtime.subscribe_to_element(Instrument("DLR/MAR22", "FUTUROS", "INMEDIATA"))
        except Exception as error:
            traceback.print_exc()

    def ondisconnect_marketdata(self):
        try:
            print("\nDisconnected from realtime market data")
        except Exception as error:
            traceback.print_exc()

    def onmarketdata(self, data):
        try:
            msg = json.loads(data)
            if msg.get("Trade"):
                print("%s [%s-%s] Price %.2f Volume %.2f" % (
                    msg['Date'], msg['Ticker'], msg['Settlement'], msg['Price'], msg['VolumeAmount']))
            else:
                bid = msg['Bids'][0]['Price'] if msg['Bids'] else 0
                offer = msg['Offers'][0]['Price'] if msg['Offers'] else 0
                print(
                    "%s [%s-%s] Offers: %.2f-%.2f Opening: %.2f MaxDay: %.2f MinDay: %.2f Accumulated Volume %.2f" %
                    (
                        msg['Date'], msg['Ticker'], msg['Settlement'], bid, offer,
                        msg['OpeningPrice'], msg['MaxDay'], msg['MinDay'], msg['VolumeTotalAmount']))
        except Exception as error:
            print(datetime.now())
            traceback.print_exc()

    def get_instrument_realtime(self):
        print("this is executing")
        self.ppi.realtime.connect_to_market_data(
            self.onconnect_marketdata, 
            self.ondisconnect_marketdata, 
            self.onmarketdata
        )

    
    def get_account_realtime(self):
        def onconnect_accountdata():
                try:
                    print("Connected to account data")
                    self.ppi.realtime.subscribe_to_account_data(self.account_number)
                except Exception as error:
                    traceback.print_exc()

        def ondisconnect_accountdata():
            try:
                print("Disconnected from account data")
            except Exception as error:
                traceback.print_exc() 
                
    #endregion
    
    
    