import requests
import pandas as pd
from datetime import datetime, timedelta

def binance_history(
    symbol='BTCUSDT',
    interval='5m',
    start_time=None,
    end_time=None,
    limit=1000):
    
    base_url = 'https://api.binance.com/api/v3/klines'
    
    # Convert datetime to milliseconds if needed
    if isinstance(start_time, datetime):
        start_time = int(start_time.timestamp() * 1000)
    if isinstance(end_time, datetime):
        end_time = int(end_time.timestamp() * 1000)
    
    all_klines = []
    current_start = start_time

    while True:
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        if current_start:
            params['startTime'] = current_start
        if end_time:
            params['endTime'] = end_time

        response = requests.get(base_url, params=params)
        response.raise_for_status()
        klines = response.json()

        if not klines:
            break

        all_klines.extend(klines)
        
        # Get the close time of the last kline (in ms)
        last_close_time = klines[-1][6]  # Close time field
        current_start = last_close_time + 1  # Avoid duplicate

        # Stop if we've passed end_time
        if end_time and last_close_time >= end_time:
            break

        # Binance may return fewer than 'limit' when near end
        if len(klines) < limit:
            break

    # Convert to DataFrame
    df = pd.DataFrame(all_klines, columns=[
        'Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Close time', 'Quote asset volume', 'Number of trades',
        'Taker buy base', 'Taker buy quote', 'Ignore'
    ])

    # Clean up
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = pd.to_numeric(df[col])

    # Remove duplicates just in case
    df = df.drop_duplicates(subset=['Open time']).reset_index(drop=True)
    return df
