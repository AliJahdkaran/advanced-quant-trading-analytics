import ccxt
import pandas as pd
import time

exchange = ccxt.binance({'enableRateLimit': True})

start_time = exchange.parse8601('2023-01-01T00:00:00Z')
all_candles = []
print('Fetching data for BTC/USDT...')

while True:
    batch_data = exchange.fetch_ohlcv(symbol='BTC/USDT',timeframe='4h' , since=start_time, limit=1000)
    if len(batch_data) == 0:
        break
    all_candles.extend(batch_data)
    start_time = batch_data[-1][0] + 1
    print(f'Downloaded {len(all_candles)} candles so far...')
    time.sleep(1)


df = pd.DataFrame(all_candles, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms').dt.tz_localize('UTC')
df.to_csv('data\\raw\\btcusdt-4h-2023-2026.csv', index=False)