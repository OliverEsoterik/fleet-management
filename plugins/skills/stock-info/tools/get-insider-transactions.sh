#!/usr/bin/env bash
# get-insider-transactions.sh — Fetch recent insider transactions from yfinance
# Usage: bash get-insider-transactions.sh <ticker>
# Outputs JSON to stdout

set -euo pipefail

TICKER="${1:?Usage: get-insider-transactions.sh <ticker>}"

python3 -c "
import json, sys, yfinance as yf

try:
    stock = yf.Ticker('$TICKER')
    insiders = stock.insider_transactions
    if insiders is None or insiders.empty:
        print(json.dumps({'error': 'No insider transaction data for $TICKER', 'ticker': '$TICKER'})); sys.exit(0)
        sys.exit(0)

    results = []
    # insiders is a DataFrame with columns like: Shares, Value, Text, Insider, Position, Start Date
    for _, row in insiders.iterrows():
        entry = {}
        for col in insiders.columns:
            val = row[col]
            if hasattr(val, 'item'):
                val = val.item()
            elif hasattr(val, 'strftime'):
                val = val.strftime('%Y-%m-%d')
            elif hasattr(val, 'tolist'):
                val = val.tolist()
            # Skip NaN
            if val is None or (hasattr(val, '__class__') and 'nan' in str(val).lower()):
                val = None
            entry[str(col)] = val
        results.append(entry)

    print(json.dumps(results, indent=2, default=str))

except Exception as e:
    print(json.dumps({'error': str(e), 'ticker': '$TICKER'})); sys.exit(0)
    sys.exit(1)
"