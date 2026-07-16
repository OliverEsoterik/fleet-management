#!/usr/bin/env bash
# get-calendar.sh — Fetch upcoming earnings/dividend calendar from yfinance
# Usage: bash get-calendar.sh <ticker>
# Outputs JSON to stdout

set -euo pipefail

TICKER="${1:?Usage: get-calendar.sh <ticker>}"

python3 -c "
import json, sys, yfinance as yf

try:
    stock = yf.Ticker('$TICKER')
    cal = stock.calendar
    if cal is None:
        print(json.dumps({'error': 'No calendar data for $TICKER', 'ticker': '$TICKER'})); sys.exit(0)
        sys.exit(0)
    # Calendar can be a Series or dict-like
    try:
        items = cal.items()
    except AttributeError:
        try:
            items = cal.to_dict().items()
        except AttributeError:
            items = cal.items() if hasattr(cal, 'items') else {}

    out = {'ticker': '$TICKER'}
    for idx, val in items:
        key = str(idx).strip()
        if hasattr(val, 'strftime'):
            val = val.strftime('%Y-%m-%d')
        elif hasattr(val, 'item'):
            val = val.item()
        elif isinstance(val, list):
            val = [v.strftime('%Y-%m-%d') if hasattr(v, 'strftime') else v for v in val]
        if val is None or (hasattr(val, '__class__') and 'nan' in str(val).lower()):
            val = None
        out[key] = val

    print(json.dumps(out, indent=2, default=str))

except Exception as e:
    print(json.dumps({'error': str(e), 'ticker': '$TICKER'})); sys.exit(0)
    sys.exit(0)  # exit 0 — error is in the JSON
"