#!/usr/bin/env bash
# get-income-statement.sh — Fetch annual income statements from yfinance
# Usage: bash get-income-statement.sh <ticker> [periods]
#   periods: number of years to fetch (default: 5)
# Outputs JSON to stdout

set -euo pipefail

TICKER="${1:?Usage: get-income-statement.sh <ticker> [periods]}"
PERIODS="${2:-5}"

python3 -c "
import json, sys, yfinance as yf

try:
    stock = yf.Ticker('$TICKER')
    # annual income statement
    inc = stock.income_stmt
    if inc is None or inc.empty:
        print(json.dumps({'error': 'No income statement data for $TICKER', 'ticker': '$TICKER'})); sys.exit(0)
        sys.exit(0)

    # inc is a DataFrame: rows = line items, columns = dates
    results = []
    for col in inc.columns[:$PERIODS]:
        year = col.year if hasattr(col, 'year') else str(col)[:10]
        entry = {'year': year}
        for idx, val in inc[col].items():
            if idx is not None:
                # Clean up line item names
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