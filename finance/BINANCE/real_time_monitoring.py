from binance import ThreadedWebsocketManager
import pandas as pd
import ta
import threading

# ---- Config ---- #
SYMBOL = 'btcusdt'  # Binance standard symbol format
INTERVAL = '1m'     # WebSocket streams '1m' live candle updates
RSI_PERIOD = 14
PRICE_ALERT_THRESHOLD = 70000  # Example price alert threshold
ALERT_TRIGGERED = False        # Control flag to prevent repeat alerts

# ---- DataFrame Setup ---- #
price_data = pd.DataFrame(columns=['time', 'close'])

# ---- Alert Function ---- #
def send_alert(message):
    print(f"ALERT: {message}")
    # Extend this with email, Telegram bot, etc.

# ---- WebSocket Callback ---- #
def handle_socket_message(msg):
    global price_data, ALERT_TRIGGERED

    if msg['e'] != 'kline':
        return

    kline = msg['k']
    close_time = pd.to_datetime(kline['t'], unit='ms')
    close_price = float(kline['c'])

    # Append new candle close to DataFrame
    new_row = pd.DataFrame({'time': [close_time], 'close': [close_price]})
    price_data = pd.concat([price_data, new_row], ignore_index=True)
    price_data = price_data.tail(RSI_PERIOD + 1)  # Keep relevant rows

    if len(price_data) > RSI_PERIOD:
        price_data['rsi'] = ta.rsi(price_data['close'], length=RSI_PERIOD)

        latest_rsi = price_data['rsi'].iloc[-1]
        print(f"Price: {close_price:.2f} | RSI: {latest_rsi:.2f}")

        # ---- RSI Alerts ---- #
        if latest_rsi < 30 and not ALERT_TRIGGERED:
            send_alert(f"{SYMBOL.upper()} RSI is Oversold ({latest_rsi:.2f})")
            ALERT_TRIGGERED = True
        elif latest_rsi > 70 and not ALERT_TRIGGERED:
            send_alert(f"{SYMBOL.upper()} RSI is Overbought ({latest_rsi:.2f})")
            ALERT_TRIGGERED = True
        elif 30 <= latest_rsi <= 70:
            ALERT_TRIGGERED = False  # Reset flag when RSI is neutral

        # ---- Price Alerts ---- #
        if close_price > PRICE_ALERT_THRESHOLD:
            send_alert(f"{SYMBOL.upper()} crossed price threshold: {close_price}")

# ---- WebSocket Initialization ---- #
def start_socket():
    twm = ThreadedWebsocketManager()
    twm.start()
    twm.start_kline_socket(callback=handle_socket_message, symbol=SYMBOL, interval=INTERVAL)

# ---- Start Stream in Thread ---- #
try:

    ws_thread = threading.Thread(target=start_socket, daemon=True)
    ws_thread.start()

except KeyboardInterrupt:
    print("Interrupted!")
    
finally:
    ws_thread.stop()
    ws_thread.get_event_loop().stop()
    print("Socket closed cleanly.")