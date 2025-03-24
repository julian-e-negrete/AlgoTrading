from data_stream import BinanceMonitor
import signal
import os

def shutdown_handler(signum, frame):
    print("Shutting down...")
    monitor.stop()
    exit(0)
    
if __name__ == "__main__":
    os.system("clear")
    monitor = BinanceMonitor()
    try:
        signal.signal(signal.SIGINT, shutdown_handler)
        monitor.start()
    except KeyboardInterrupt:
        print("[INFO] Shutting down...")
