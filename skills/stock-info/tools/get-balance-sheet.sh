#!/usr/bin/env bash
# get-balance-sheet.sh — Fetch annual balance sheets from yfinance
# Usage: bash get-balance-sheet.sh <ticker> [periods]
#   periods: number of years to fetch (default: 5)
# Outputs JSON to stdout

set -euo pipefail

TICKER="${1:?Usage: get-balance-sheet.sh <ticker> [periods]}"
PERIODS="${2:-5}"

python3 -c "
import json, sys, yfinance as yf

try:
    stock = yf.Ticker('$TICKER')
    bs = stock.balance_sheet
    if bs is None or bs.empty:
        print(json.dumps({'error': 'No balance sheet data for $TICKER', 'ticker': '$TICKER'})); sys.exit(0)
        sys.exit(0)

    results = []
    for col in bs.columns[:$PERIODS]:
        year = col.year if hasattr(col, 'year') else str(col)[:10]
        entry = {'year': year}
        for idx, val in bs[col].items():
            if idx is not None:
                name = str(idx).strip()
                if hasattr(val, 'item'):
                    val = val.item()
                elif hasattr(val, 'tolist'):
                    val = val.tolist()
                entry[name] = val
        results.append(entry)

    print(json.dumps(results, indent=2, default=str))

except Exception as e:
    print(json.dumps({'error': str(e), 'ticker': '$TICKER'})); sys.exit(0)
    sys.exit(1)
"