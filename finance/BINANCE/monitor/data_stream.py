from binance import ThreadedWebsocketManager
import asyncio
import pandas as pd
from config import BINANCE_API_KEY, BINANCE_SECRET_KEY, SYMBOL, INTERVAL, LOOKBACK

from indicators import compute_rsi
from alerting import evaluate_alerts, warning_price
from graphing import update_graph
import time
import threading
import os



class BinanceMonitor:
    def __init__(self):
        self.data = pd.DataFrame()

    def start(self):
        self.twm = ThreadedWebsocketManager(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY)
        self.twm.start()
        self.conn_key = self.twm.start_kline_socket(callback=self.process_message, symbol=SYMBOL.lower(), interval=INTERVAL)
        print(f"WebSocket started with connection key: {self.conn_key}")  # Confirming the conn_key is set
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down...")
            self.stop()
        

    def process_message(self, msg):
        
        if msg['e'] != 'kline':
            return
        kline = msg['k']
        new_row = {
            "timestamp": pd.to_datetime(kline['t'], unit='ms'),
            "open": float(kline['o']),
            "high": float(kline['h']),
            "low": float(kline['l']),
            "close": float(kline['c']),
            "volume": float(kline['v']),
        }
        self.data = pd.concat([self.data, pd.DataFrame([new_row])]).drop_duplicates(subset="timestamp")
        os.system("clear")
        self.data = self.data.tail(LOOKBACK)
        
        #print(f"Data length after update: {len(self.data)}")  # Log length after data update
        warning_price(self.data["open"][0])
        
        if len(self.data) >= 14:
            print(f"Data length: {len(self.data)}")
            print(f"Latest data: {self.data.tail()}")

            rsi = compute_rsi(self.data)
            evaluate_alerts(rsi)
            #update_graph(self.data)
        else:
            print("self.data < 14")

    def stop(self):
        if self.twm:
            print("Attempting to stop WebSocket manager...")
            if hasattr(self, 'conn_key'):
                print(f"Stopping WebSocket with conn_key: {self.conn_key}")
                self.twm.stop_socket(self.conn_key)
            else:
                print("No connection key found. WebSocket might not have started properly.")
            
            # Ensure the WebSocket manager is stopped
            self.twm.stop()  # Properly stop the WebSocket manager
            print("WebSocket manager stopped")
            
            for thread in threading.enumerate():
                print(f"Thread still running: {thread.name}")
            
        else:
            print("WebSocket manager not initialized")
