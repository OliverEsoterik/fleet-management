#!/usr/bin/env bash
# get-info.sh — Fetch ticker-level summary data from yfinance
# Usage: bash get-info.sh <ticker>
# Outputs JSON to stdout

set -euo pipefail

TICKER="${1:?Usage: get-info.sh <ticker>}"

python3 -c "
import json, sys, yfinance as yf

try:
    stock = yf.Ticker('$TICKER')
    info = stock.info

    # Select the most useful subset of fields
    fields = [
        # Identifiers
        'ticker', 'shortName', 'longName', 'exchange', 'sector', 'industry',
        # Price
        'currentPrice', 'regularMarketPrice', 'previousClose', 'open',
        'dayHigh', 'dayLow', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow',
        'fiftyDayAverage', 'twoHundredDayAverage',
        # Volume
        'averageVolume', 'averageVolume10days', 'regularMarketVolume',
        # Valuation
        'trailingPE', 'forwardPE', 'pegRatio', 'priceToBook', 'priceToSalesTrailing12Months',
        'enterpriseValue', 'enterpriseToRevenue', 'enterpriseToEbitda',
        # EPS
        'epsTrailingTwelveMonths', 'epsForward', 'epsCurrentYear',
        # Growth
        'earningsGrowth', 'revenueGrowth', 'profitMargins', 'operatingMargins',
        'grossMargins', 'ebitdaMargins',
        # Dividends
        'dividendRate', 'dividendYield', 'fiveYearAvgDividendYield', 'payoutRatio',
        'exDividendDate', 'dividendDate',
        # Balance sheet
        'bookValue', 'debtToEquity', 'currentRatio', 'quickRatio',
        # Cash flow
        'freeCashflow', 'operatingCashflow', 'ebitda', 'capitalExpenditure',
        # Returns
        'beta', 'returnOnAssets', 'returnOnEquity',
        # Ownership
        'heldPercentInsiders', 'heldPercentInstitutions', 'sharesOutstanding',
        'floatShares', 'sharesShort', 'shortRatio', 'dateShortInterest',
        'shortPercentOfFloat',
        # Miscellaneous
        'marketCap', 'recommendationKey', 'recommendationMean',
        'numberOfAnalystOpinions', 'targetMeanPrice', 'targetHighPrice',
        'targetLowPrice',
        # Corporate
        'fullTimeEmployees', 'country', 'city', 'address1',
        'longBusinessSummary',
    ]

    out = {'ticker': info.get('symbol', '$TICKER')}
    for f in fields:
        if f in info and info[f] is not None:
            val = info[f]
            # Convert numpy types
            if hasattr(val, 'item'):
                val = val.item()
            out[f] = val
        else:
            out[f] = None

    # Always include business summary (it's long but important)
    out['longBusinessSummary'] = info.get('longBusinessSummary', None)

    print(json.dumps(out, indent=2, default=str))

except Exception as e:
    print(json.dumps({'error': str(e), 'ticker': '$TICKER'})); sys.exit(0)
    sys.exit(1)
"
