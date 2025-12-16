# Roblox Stock Exchange - Stock Data

This repository contains automatically updated stock price data for the Roblox Stock Exchange game.

## Overview

This repo fetches daily stock prices from [Stooq](https://stooq.com/) for:
- **RBLX** - Roblox Corporation
- **AAPL** - Apple Inc.
- **MSFT** - Microsoft Corporation

## Data Format

The `stock-prices.json` file contains:

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

## Automation

- **Daily Updates**: GitHub Actions runs daily at 6:00 AM UTC to fetch the latest stock prices
- **Manual Trigger**: Can be manually triggered from the Actions tab
- **Auto-commit**: Automatically commits updated data to the main branch

## Usage

### Access Raw JSON
```
https://raw.githubusercontent.com/Jamess-Nguyen/roblox-stock-exchange-data/main/stock-prices.json
```

### In Roblox Game
The main game repository reads this JSON file via HttpService to get updated stock prices.

## Future Plans

This GitHub Action workflow will eventually be migrated to a serverless function for more real-time updates.
