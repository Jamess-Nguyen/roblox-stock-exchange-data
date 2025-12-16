# Roblox Stock Exchange - Stock Data

This repository contains automatically updated stock price data for the Roblox Stock Exchange game.

## Overview

This repo fetches daily stock prices from [Stooq](https://stooq.com/) for:
- **RBLX** - Roblox Corporation
- **AAPL** - Apple Inc.
- **MSFT** - Microsoft Corporation

## How It Works

1. **Daily Automation** (6:00 AM UTC)
   - GitHub Action fetches latest stock prices from Stooq API
   - Generates JSON file with current prices
   - Commits updated file to this repository

2. **In-Game Usage**
   - Your Roblox game uses HttpService to fetch the JSON from GitHub
   - Data is served free via GitHub's raw file URL
   - Updates automatically every day

## Data Formats

### JSON Format (`stock-prices.json`)
```json
{
  "last_updated": "ISO 8601 timestamp",
  "stocks": {
    "SYMBOL": {
      "symbol": "SYMBOL",
      "date": "YYYY-MM-DD",
      "open": 0.00,
      "high": 0.00,
      "low": 0.00,
      "close": 0.00,
      "volume": 0
    }
  }
}
```

## Usage in Roblox

```lua
-- Enable HttpService in game settings first!
local HttpService = game:GetService("HttpService")

-- Fetch the latest stock data
local DATA_URL = "https://raw.githubusercontent.com/Jamess-Nguyen/roblox-stock-exchange-data/main/stock-prices.json"

local success, response = pcall(function()
    return HttpService:GetAsync(DATA_URL)
end)

if success then
    local data = HttpService:JSONDecode(response)

    -- Access stock prices
    local rblxPrice = data.stocks.RBLX.close
    print("RBLX Price:", rblxPrice)

    -- Loop through all stocks
    for symbol, stock in pairs(data.stocks) do
        print(symbol, stock.close)
    end
else
    warn("Failed to fetch stock data:", response)
end
```

**Important:** Make sure to enable HttpService in your game settings:
- Game Settings → Security → Allow HTTP Requests = ON

## Future Plans

This GitHub Action workflow will eventually be migrated to a serverless function for more real-time updates.
