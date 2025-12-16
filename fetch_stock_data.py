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
from symbols import SYMBOLS, ETFS
from symbols_translations import SYMBOL_NAMES, ETF_NAMES

def get_date_range(days_back=5):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    return {
        "start": start_date.strftime("%Y%m%d"),
        "end": end_date.strftime("%Y%m%d")
    }

def fetch_stooq_data(symbol):
    dates = get_date_range()
    url = f"https://stooq.com/q/d/l/?s={symbol}&i=d&d1={dates['start']}&d2={dates['end']}"

    try:
        with urllib.request.urlopen(url) as response:
            csv_data = response.read().decode('utf-8')

        reader = csv.DictReader(StringIO(csv_data))
        rows = list(reader)

        if not rows:
            return None

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
    all_names = {k: v for d in (SYMBOL_NAMES, ETF_NAMES) for k, v in d.items()}

    lua_lines = [
        "-- Stock Data Module",
        "-- Auto-generated from Stooq API",
        f"-- Last updated: {data['last_updated']}",
        "",
        "return {"
    ]

    for symbol, stock in data['stocks'].items():
        lua_lines.append("\t{")
        lua_lines.append(f"\t\tName = \"{all_names.get(symbol, symbol)}\",")
        lua_lines.append(f"\t\tSymbol = \"{stock['symbol']}\",")
        lua_lines.append(f"\t\tCurrentPrice = {stock['close']}")
        lua_lines.append("\t},")

    lua_lines.append("}")

    return "\n".join(lua_lines)

def main():
    stock_data = {}

    for symbol in SYMBOLS + ETFS:
        data = fetch_stooq_data(symbol)
        if data:
            stock_data[data["symbol"]] = data

    output = {
        "last_updated": datetime.now().isoformat(),
        "stocks": stock_data
    }

    with open('stock-prices.json', 'w') as f:
        json.dump(output, f, indent=2)

    lua_content = generate_lua_module(output)
    with open('StockData.lua', 'w') as f:
        f.write(lua_content)

if __name__ == "__main__":
    main()
