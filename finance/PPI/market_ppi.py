# Imports 
from ppi_client.ppi import PPI

from ppi_client.models.instrument import Instrument
from datetime import datetime
from ppi_client.models.estimate_bonds import EstimateBonds
import json
import traceback
import math




class Market_data:
    
    def __init__(self, P_ppi ) -> None:
        self.ppi = P_ppi
        self.instruments = []
        
        
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
    def get_instrument(self, ticker: str,market: str, type_instrument: str ):
        # Search Instrument
        print("\nSearching instruments")
        instruments = self.ppi.marketdata.search_instrument(ticker.upper(), "", market, type_instrument)
        for ins in instruments:
            print(f"Ticker: {ins["ticker"]}\t Descripcion: {ins["description"]}\t Moneda: {ins["currency"]}\t Tipo: {ins["type"]}")
            
            
    def search_current_book(self, ticker: str, type_: str, time: str):
        # Search Current Book
        print("\nSearching Current Book")
        current_book = self.ppi.marketdata.book(ticker.upper(), type_, time)
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
    def get_market_data(self, ticker, type_instrument, time):
        if(ticker == ""):
            ticker = input("ingrese el ticker que quiere buscar: ")
            
        print("\nSearching Current MarketData")
        current_market_data = self.ppi.marketdata.current(ticker.upper(), type_instrument, time)
        print(ticker.upper())
        print("-----------------------------------------")
        date_object = datetime.strptime(current_market_data["date"],  "%Y-%m-%dT%H:%M:%S%z")

        formatted_date = date_object.strftime("%d-%m-%Y")  # Example: "23-Dec-2024"

        #print(current_market_data)
        print(f"fecha :{formatted_date}\t Precio: {current_market_data["price"]}\t Volumen: {current_market_data["volume"]}")
        
    # Search intraday data
    def get_intraday_market_data(self):
        # Search Intraday MarketData
        print("\nSearching Intraday MarketData")
        intraday_market_data = self.ppi.marketdata.intraday("GGAL", "Acciones", "A-48HS")
        for intra in intraday_market_data:
            print(intra)
               
    #endregion
    
    
    def estimate_bond(self, ticker, cantidad, precio):
        print("\nEstimate bond\n")
        if(ticker == ""):
            ticker :str= input("Ingrese el ticker: ").upper()
            cantidad :int = input("Ingrese la cantidad: ")
            precio :float = input("Ingrese el precio: ")
            
        estimate = self.ppi.marketdata.estimate_bonds(EstimateBonds(ticker=ticker, date=datetime.today(), 
        quantityType="PAPELES", quantity=cantidad, price=precio))
        
        
        print("FLOWS")
        total = 0
        for i in range(0, len(estimate["flows"])):
            date_object = datetime.strptime(estimate["flows"][i]["cuttingDate"],  "%Y-%m-%dT%H:%M:%S%z" )

            formatted_date = date_object.strftime("%d-%m-%Y")  # Example: "23-Dec-2024"

            #print(estimate["sensitivity"][i])
            print(f"Fecha: {formatted_date}", end="  ")
            print(f"Residual Value: %{ '{:.2f}'.format(estimate["flows"][i]["residualValue"] * 100) }", end="  ")
            print(f"Interes: ${ '{:.2f}'.format(estimate["flows"][i]["rent"]) }", end="  ")
            print(f"Amortizacion: ${ '{:.2f}'.format(estimate["flows"][i]["amortization"]) }", end="  ")
            print(f"Total: ${ '{:.2f}'.format(estimate["flows"][i]["total"]) }")
            total += estimate["flows"][i]["total"]
        
        print(f"total obtenido en el vencimiento: {'{:.2f}'.format(total)}")
        
        
        print("\n\nSENSISTIVITY")
        for i in range(0, len(estimate["sensitivity"])):
            print(f"TIR: {'{:.2f}'.format(estimate["sensitivity"][i]["tir"])}", end=" \t ")
            print(f"Precio: ${'{:.2f}'.format(estimate["sensitivity"][i]["price"])}", end=" \t ")    
            print(f"Paridad: {'{:.2f}'.format(estimate["sensitivity"][i]["parity"])}", end=" \t ") 
            print(f"Variacion: %{'{:.2f}'.format(estimate["sensitivity"][i]["variation"] * 100)}")    
           
        print(estimate["tir"])    
            
                
        
        
        
        
        
    #region realtime
    
    def add_instrument(self, ticker, type_, settlement):
        """
        Adds an instrument to the subscription list.

        Args:
            ticker (str): The instrument's ticker symbol.
            type_ (str): The type of the instrument (e.g., ACCIONES, BONOS).
            settlement (str): The settlement type (e.g., A-48HS, INMEDIATA).
        """
        self.instruments.append((ticker, type_, settlement))

    def on_connect(self):
        """Handles the connection to the real-time market data."""
        try:
            print("\nConnected to real-time market data")
            for ticker, type_, settlement in self.instruments:
                self.ppi.realtime.subscribe_to_element(Instrument(ticker, type_, settlement))
        except Exception as error:
            print("Error during connection:")
            traceback.print_exc()

    def on_disconnect(self):
        try:
            print("\nDisconnected from real-time market data")
        except Exception as error:
            print("Error during disconnection:")
            traceback.print_exc()

    def on_market_data(self, data):
        try:
            msg = json.loads(data)
            if msg.get("Trade"):
                print("%s [%s-%s] Price %.2f Volume %.2f" % (
                    msg['Date'], msg['Ticker'], msg['Settlement'], msg['Price'], msg['VolumeAmount']))
            else:
                bid = msg['Bids'][0]['Price'] if msg.get('Bids') else 0
                offer = msg['Offers'][0]['Price'] if msg.get('Offers') else 0
                print(
                    "%s [%s-%s] Offers: %.2f-%.2f Opening: %.2f MaxDay: %.2f MinDay: %.2f Accumulated Volume %.2f" %
                    (
                        msg['Date'], msg['Ticker'], msg['Settlement'], bid, offer,
                        msg['OpeningPrice'], msg['MaxDay'], msg['MinDay'], msg['VolumeTotalAmount']))
        except Exception as error:
            print(datetime.now())
            traceback.print_exc()

    def start(self):
        """Starts the real-time connections."""
        try:
            self.ppi.realtime.connect_to_market_data(
                self.on_connect,
                self.on_disconnect,
                self.on_market_data
            )
            self.ppi.realtime.start_connections()
        except Exception as error:
            print(datetime.now())
            print("Error during start:")
            traceback.print_exc()
                
    #endregion
    
    
    