#!/usr/bin/env bash
# get-earnings-history.sh — Fetch quarterly earnings history from yfinance
# Usage: bash get-earnings-history.sh <ticker>
# Outputs JSON to stdout (quarterly actual vs estimate with surprise %)

set -euo pipefail

TICKER="${1:?Usage: get-earnings-history.sh <ticker>}"

python3 -c "
import json, sys, yfinance as yf

try:
    stock = yf.Ticker('$TICKER')
    earnings = stock.earnings_dates
    if earnings is None or earnings.empty:
        print(json.dumps({'error': 'No earnings history data for $TICKER', 'ticker': '$TICKER'})); sys.exit(0)
        sys.exit(0)

    results = []
    for _, row in earnings.iterrows():
        entry = {}
        for col in earnings.columns:
            val = row[col]
            if hasattr(val, 'item'):
                val = val.item()
            elif hasattr(val, 'strftime'):
                val = val.strftime('%Y-%m-%d')
            elif hasattr(val, 'tolist'):
                val = val.tolist()
            if val is None or (hasattr(val, '__class__') and 'nan' in str(val).lower()):
                val = None
            entry[str(col)] = val
        results.append(entry)

    print(json.dumps(results, indent=2, default=str))

except Exception as e:
    print(json.dumps({'error': str(e), 'ticker': '$TICKER'})); sys.exit(0)
    sys.exit(1)
"