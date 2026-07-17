#!/usr/bin/env bash
# get-price-history.sh — Fetch daily OHLCV price history from yfinance
# Usage: bash get-price-history.sh <ticker> [period]
#   period: yfinance period string (5y, 1y, 6mo, 3mo, 1mo, max). Default: 5y
# Outputs CSV to stdout

set -euo pipefail

TICKER="${1:?Usage: get-price-history.sh <ticker> [period]}"
PERIOD="${2:-5y}"

python3 -c "
import csv, io, sys, yfinance as yf

try:
    stock = yf.Ticker('$TICKER')
    hist = stock.history(period='$PERIOD')
    if hist is None or hist.empty:
        print(f'error: No price history data for $TICKER (period=$PERIOD)')
        sys.exit(1)

    # Output as CSV
    csv_out = io.StringIO()
    writer = csv.writer(csv_out)
    writer.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'])

    for date, row in hist.iterrows():
        date_str = date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date)[:10]
        writer.writerow([
            date_str,
            row.get('Open', ''),
            row.get('High', ''),
            row.get('Low', ''),
            row.get('Close', ''),
            row.get('Volume', ''),
            row.get('Dividends', 0),
            row.get('Stock Splits', 0),
        ])

    print(csv_out.getvalue().strip())

except Exception as e:
    print(f'error: {e}')
    sys.exit(1)
"