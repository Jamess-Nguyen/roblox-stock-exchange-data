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
   - Generates both JSON and Lua ModuleScript formats
   - Uploads ModuleScript to Roblox asset **91072619691201** via Open Cloud API
   - Commits updated files to this repository

2. **In-Game Usage**
   - Your Roblox game can `require(91072619691201)` to get the latest stock data
   - No HttpService needed, just require the asset!
   - Data updates automatically every day

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

### Lua ModuleScript Format (`StockData.lua`)
```lua
return {
    last_updated = "2025-12-15T18:29:40.780506",
    stocks = {
        RBLX = {
            symbol = "RBLX",
            date = "2025-12-10",
            close = 94.36,
            ...
        },
        ...
    }
}
```

## Setup Requirements

### GitHub Secrets
Add `ROBLOX_API_KEY` to repository secrets with:
- Permission: **Asset Write** for asset 91072619691201
- Created at: https://create.roblox.com/credentials

## Usage in Roblox

```lua
-- In your game, simply require the asset
local StockData = require(91072619691201)

-- Access stock prices
local rblxPrice = StockData.stocks.RBLX.close
print("RBLX Price:", rblxPrice)
```

## Future Plans

This GitHub Action workflow will eventually be migrated to a serverless function for more real-time updates.
