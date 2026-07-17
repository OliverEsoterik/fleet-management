#!/usr/bin/env bash
# get-institutional-holders.sh — Fetch top institutional holders from yfinance
# Usage: bash get-institutional-holders.sh <ticker>
# Outputs JSON to stdout

set -euo pipefail

TICKER="${1:?Usage: get-institutional-holders.sh <ticker>}"

python3 -c "
import json, sys, yfinance as yf

try:
    stock = yf.Ticker('$TICKER')
    holders = stock.institutional_holders
    if holders is None or holders.empty:
        print(json.dumps({'error': 'No institutional holder data for $TICKER', 'ticker': '$TICKER'})); sys.exit(0)
        sys.exit(0)

    results = []
    for _, row in holders.iterrows():
        entry = {}
        for col in holders.columns:
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