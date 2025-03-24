from config import ALERT_THRESHOLDS

def evaluate_alerts(rsi_value):
    if rsi_value > ALERT_THRESHOLDS["RSI_OVERBOUGHT"]:
        print("[ALERT] RSI Overbought - Consider Selling")
    elif rsi_value < ALERT_THRESHOLDS["RSI_OVERSOLD"]:
        print("[ALERT] RSI Oversold - Consider Buying")


def warning_price(price):
    if(price > 1350):
        print("[ALERT] USDT/ARS > 1350!!!!")
