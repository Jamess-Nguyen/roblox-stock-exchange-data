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

def generate_lua_module(data):
    """Generate Lua ModuleScript content from stock data in game-compatible format"""
    lua_lines = [
        "-- Stock Data Module",
        "-- Auto-generated from Stooq API",
        f"-- Last updated: {data['last_updated']}",
        "",
        "return {"
    ]

    # Map symbol to full name
    symbol_names = {
        "RBLX": "Roblox",
        "AAPL": "Apple",
        "MSFT": "Microsoft"
    }

    for symbol, stock in data['stocks'].items():
        lua_lines.append("\t{")
        lua_lines.append(f"\t\tName = \"{symbol_names.get(symbol, symbol)}\",")
        lua_lines.append(f"\t\tSymbol = \"{stock['symbol']}\",")
        lua_lines.append(f"\t\tCurrentPrice = {stock['close']}")
        lua_lines.append("\t},")

    lua_lines.append("}")

    return "\n".join(lua_lines)

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

    # Write to Lua ModuleScript
    lua_content = generate_lua_module(output)
    with open('StockData.lua', 'w') as f:
        f.write(lua_content)

    print(f"\n[OK] Successfully updated stock-prices.json with {len(stock_data)} stocks")
    print(f"[OK] Successfully generated StockData.lua ModuleScript")
    print(f"Updated at: {output['last_updated']}")

if __name__ == "__main__":
    main()
