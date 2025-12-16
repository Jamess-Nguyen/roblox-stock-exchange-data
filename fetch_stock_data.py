#!/usr/bin/env python3
"""
Fetch stock data from Stooq API for RBLX, AAPL, and MSFT
Based on implementation from stock-api-service repo
"""

import json
import urllib.request
from datetime import datetime, timedelta
import csv
from io import StringIO

# Stock symbols to fetch
SYMBOLS = ["RBLX.US", "AAPL.US", "MSFT.US"]

def get_date_range(days_back=5):
    """Get start and end dates for fetching stock data"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    return {
        "start": start_date.strftime("%Y%m%d"),
        "end": end_date.strftime("%Y%m%d")
    }

def fetch_stooq_data(symbol):
    """
    Fetch EOD data from Stooq API
    API: https://stooq.com/q/d/l/?s={symbol}&i=d&d1={startDate}&d2={endDate}
    Returns CSV format
    """
    dates = get_date_range()
    url = f"https://stooq.com/q/d/l/?s={symbol}&i=d&d1={dates['start']}&d2={dates['end']}"

    print(f"Fetching {symbol} from {url}")

    try:
        with urllib.request.urlopen(url) as response:
            csv_data = response.read().decode('utf-8')

        # Parse CSV
        reader = csv.DictReader(StringIO(csv_data))
        rows = list(reader)

        if not rows:
            return None

        # Get the most recent data (first row after header)
        latest = rows[0]

        return {
            "symbol": symbol.replace(".US", ""),
            "date": latest['Date'],
            "open": float(latest['Open']),
            "high": float(latest['High']),
            "low": float(latest['Low']),
            "close": float(latest['Close']),
            "volume": int(latest['Volume'])
        }
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def main():
    """Main function to fetch all stock data and write to JSON"""
    stock_data = {}

    for symbol in SYMBOLS:
        data = fetch_stooq_data(symbol)
        if data:
            stock_data[data["symbol"]] = data
            print(f"[OK] Fetched {data['symbol']}: ${data['close']}")

    # Add metadata
    output = {
        "last_updated": datetime.now().isoformat(),
        "stocks": stock_data
    }

    # Write to JSON file
    with open('stock-prices.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n[OK] Successfully updated stock-prices.json with {len(stock_data)} stocks")
    print(f"Updated at: {output['last_updated']}")

if __name__ == "__main__":
    main()
