import websocket
import json
from tabulate import tabulate

FIELDS = [
    "instrument", "sequence", "bid_qty", "last_price", "ask_price", "volume",
    "prev_close", "timestamp", "trades", "turnover", "turnover_clean",
    "open", "high", "low", "open_interest",
    "settlement_price", "settlement_date",
    "previous_settlement_price", "previous_settlement_date",
    "reference_price", "reference_date"
]

def parse_market_message(raw_msg):
    if raw_msg.startswith("M:"):
        content = raw_msg[2:].split("|")
        if len(content) != len(FIELDS):
            print("Field count mismatch:", len(content))
            return None
        return dict(zip(FIELDS, content))
    return None


def on_message(ws, message):
    if isinstance(message, bytes):
        message = message.decode('utf-8')

    if isinstance(message, str):
        if message.startswith("M:"):
            parsed = parse_market_message(message)
            
            if parsed:
                #print(parsed.keys)
                # fields = ["instrument", "last_price", "ask_price", "last_price", "open_interest", "volume"]
                # row = [[parsed[k] for k in fields]]

                # print(tabulate(row, headers=fields, tablefmt="plain"))
                
                for key in [ 'high', 'low', 'last_price', 'prev_close', 'ask_price']:
                    if parsed.get(key) is not None:
                        parsed[key] = float(parsed[key])
                        
                
                
                contract_size = 1000                  # contract multiplier

                vwap = float(parsed["turnover"]) / float((parsed["turnover_clean"]))

                momentum = parsed['high'] - parsed['low']
                price_change = float(parsed['prev_close']) - float(parsed['previous_settlement_price'])
                spread = parsed['ask_price'] - parsed['last_price']

                # Output: formatted as a horizontal table
                output = {
                    'Instrument': parsed['instrument'],
                    'Bid Volume': parsed['bid_qty'],
                    'bid Price': parsed['last_price'],
                    
                    'ask Volume': parsed['volume'],
                    'ask price': parsed['ask_price'],
                    'last': parsed['prev_close'],
                    
                    'VWAP': round(vwap, 2),
                    'Momentum': round(momentum, 2),
                    'Change': round(price_change, 2),
                    'Spread': round(spread, 2),
                    'Open Interest': parsed['open_interest'],
                    'Volume': parsed['trades']
                    
                }

                # Tabulate horizontally
                print(tabulate([output.values()], headers=output.keys(), tablefmt='grid'))

                #print(" | ".join(f"{k}: {v}" for k, v in parsed.items()))
                
                #print("Market Update:", parsed)
        elif message.startswith("X:"):
            try:
                clock_data = json.loads(message[2:])
                print("Meta:", clock_data)
            except json.JSONDecodeError:
                print("Malformed X:", message)
        else:
            try:
                decoded = json.loads(message)
                print("JSON:", decoded)
            except json.JSONDecodeError:
                print("Raw:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Closed")

def on_open(ws):
    # First subscription
    ws.send(json.dumps({
        "_req": "S",
        "topicType": "md",
        "topics": [
            "md.bm_MERV_PESOS_7D", "md.bm_MERV_PESOS_6D", "md.bm_MERV_PESOS_5D",
            "md.bm_MERV_PESOS_4D", "md.bm_MERV_PESOS_3D", "md.bm_MERV_PESOS_2D",
            "md.bm_MERV_PESOS_1D"
        ],
        "replace": False
    }))

    # Second subscription
    ws.send(json.dumps({
        "_req": "S",
        "topicType": "md",
        "topics": ["md.rx_DDF_DLR_JUL25", "md.rx_DDF_DLR_JUL25A"],
        "replace": False
    }))
    
    
if __name__ == "__main__":
    
    ws_url = "wss://matbarofex.primary.ventures/ws?session_id=&conn_id="

    headers = [
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
        "Pragma: no-cache",
        "Cache-Control: no-cache"
    ]

    ws = websocket.WebSocketApp(
        ws_url,
        header=headers,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever()
