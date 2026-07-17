---
name: stock-info
description: >
  Fetch comprehensive financial data for any publicly traded ticker using
  yfinance. Provides stock info, income statements, balance sheets, cash flow
  statements, historical prices, insider transactions, earnings calendar, and
  institutional holders. All data is fetched via local bash scripts — no
  external APIs or runtime tools required.
---

# Stock Info — Financial Data Provider

## Overview

Use this skill when you need financial data for a stock ticker. It provides
bash scripts that return structured data (JSON/markdown) for any publicly
traded ticker via yfinance.

**This is a data-provider skill.** Other skills (like `peter-lynch`,
`lyn-alden-dcf`) reference it as a dependency rather than reimplementing data
fetching.

---

## Available Scripts

All scripts live in `plugins/skills/stock-info/tools/`. Each accepts a ticker symbol
as the first argument and outputs structured data to stdout.

| Script | Output | Key Fields |
|--------|--------|------------|
| `get-info.sh` | JSON | Price, market cap, P/E, EPS, PEG, beta, dividend yield, debt/equity, current ratio, FCF, insider/inst holdings, 52wk range |
| `get-income-statement.sh` | JSON | Revenue, gross profit, operating income, net income, EPS, shares outstanding (annual, up to 5 years) |
| `get-balance-sheet.sh` | JSON | Cash, debt, equity, current assets/liabilities, book value, working capital, net debt (annual, up to 5 years) |
| `get-cash-flow.sh` | JSON | Operating CF, investing CF, financing CF, FCF, capex, buybacks, dividends (annual, up to 5 years) |
| `get-insider-transactions.sh` | JSON | Recent insider trades: who, what (buy/sell/gift), value, date, position |
| `get-institutional-holders.sh` | JSON | Top institutional holders with shares and value |
| `get-earnings-history.sh` | JSON | Historical quarterly EPS (actual vs estimate, surprise %) |
| `get-price-history.sh` | CSV | Daily OHLCV + dividends + splits (up to 5 years) |
| `get-calendar.sh` | JSON | Upcoming earnings date, dividend date, estimates |
| `get-all.sh` | JSON | Merges all of the above into a single JSON document |

Each script also accepts an optional second argument for the number of periods
(default: 5 for annual financials).

---

## Usage

### From another skill

In a SKILL.md file, reference the data tool via bash:

```bash
bash plugins/skills/stock-info/tools/get-info.sh AAPL
bash plugins/skills/stock-info/tools/get-balance-sheet.sh MSFT 3
bash plugins/skills/stock-info/tools/get-all.sh NVDA
```

### From the command line

```bash
bash plugins/skills/stock-info/tools/get-info.sh AAPL | python3 -m json.tool
bash plugins/skills/stock-info/tools/get-income-statement.sh MSFT
bash plugins/skills/stock-info/tools/get-all.sh NVDA > nvda-data.json
```

---

## Dependencies

- **yfinance** — Python package. Install: `pip install yfinance`
- **python3** — standard
- **bash** — standard

All scripts gracefully handle missing tickers (return valid JSON with an
`error` field) and missing data (return null for unavailable fields).

---

## Script Details

### `get-info.sh`

Ticker-level summary data. This is the fastest script — it fetches the `info`
dict from yfinance. Contains ~200 fields.

**Example:**
```json
{
  "ticker": "AAPL",
  "price": 318.80,
  "marketCap": 4682402496512,
  "trailingPE": 38.60,
  "forwardPE": 33.16,
  "pegRatio": 2.55,
  "epsTrailingTwelveMonths": 8.26,
  "epsCurrentYear": 8.75,
  "epsForward": 9.61,
  "dividendYield": 0.0034,
  "dividendRate": 1.08,
  "debtToEquity": 79.55,
  "currentRatio": 1.07,
  "quickRatio": 0.91,
  "freeCashflow": 101090746368,
  "operatingCashflow": 140222005248,
  "ebitda": 159975997440,
  "enterpriseValue": 4647420952576,
  "bookValue": 7.26,
  "priceToBook": 43.91,
  "beta": 1.10,
  "heldPercentInsiders": 0.016,
  "heldPercentInstitutions": 0.657,
  "fiftyTwoWeekHigh": 323.45,
  "fiftyTwoWeekLow": 201.50,
  "averageVolume": 54682654,
  "recommendationMean": 2.0,
  "sector": "Technology",
  "industry": "Consumer Electronics",
  "longBusinessSummary": "Apple Inc. designs..."
}
```

### `get-income-statement.sh` — Annual Income Statement

Returns annual income statement data as a JSON array of years.

```json
[
  {
    "year": 2026,
    "Total Revenue": 438456000000,
    "Cost Of Revenue": 223250000000,
    "Gross Profit": 215206000000,
    "Operating Income": 142319000000,
    "Net Income": 122575003648,
    "Diluted EPS": 7.91,
    "Basic EPS": 7.96,
    "Diluted Average Shares": 15502000000,
    "EBITDA": 159975997440,
    "EBIT": 142319000000,
    "Operating Expense": 142319000000,
    "Research And Development": 35000000000,
    "Selling General And Administration": 28000000000,
    "Pretax Income": 143000000000,
    "Tax Provision": 20000000000,
    "Interest Expense Non Operating": 1000000000,
    "Net Interest Income": -1000000000
  }
]
```

### `get-balance-sheet.sh` — Annual Balance Sheet

Returns annual balance sheet data as a JSON array of years.

```json
[
  {
    "year": 2026,
    "Total Assets": 380000000000,
    "Total Liabilities Net Minority Interest": 300000000000,
    "Stockholders Equity": 80000000000,
    "Cash And Cash Equivalents": 30000000000,
    "Long Term Debt": 85000000000,
    "Net Debt": 55000000000,
    "Current Assets": 120000000000,
    "Current Liabilities": 110000000000,
    "Working Capital": 10000000000,
    "Tangible Book Value": 70000000000,
    "Invested Capital": 150000000000,
    "Total Capitalization": 165000000000,
    "Common Stock Equity": 80000000000,
    "Retained Earnings": 50000000000,
    "Capital Stock": 60000000000,
    "Total Debt": 100000000000,
    "Current Deferred Revenue": 7000000000,
    "Long Term Debt And Capital Lease Obligation": 85000000000,
    "Goodwill And Intangible Assets": 10000000000
  }
]
```

### `get-cash-flow.sh` — Annual Cash Flow Statement

Returns annual cash flow data as a JSON array of years.

```json
[
  {
    "year": 2026,
    "Free Cash Flow": 101090746368,
    "Operating Cash Flow": 140222005248,
    "Investing Cash Flow": -45000000000,
    "Financing Cash Flow": -95000000000,
    "Capital Expenditure": -39131258880,
    "Repurchase Of Capital Stock": -80000000000,
    "Common Stock Dividend Paid": -15000000000,
    "Issuance Of Debt": 10000000000,
    "Repayment Of Debt": -15000000000,
    "Issuance Of Capital Stock": 5000000000,
    "Cash Dividends Paid": -15000000000,
    "End Cash Position": 30000000000,
    "Beginning Cash Position": 35000000000,
    "Changes In Cash": -5000000000,
    "Interest Paid Supplemental Data": 1000000000,
    "Income Tax Paid Supplemental Data": 20000000000
  }
]
```

### `get-insider-transactions.sh` — Insider Transactions

Returns recent insider transactions.

```json
[
  {
    "insider": "LEVINSON ARTHUR D",
    "position": "Director",
    "transaction": "",
    "shares": 50000,
    "value": 15551000,
    "date": "2026-05-27",
    "text": "Sale at price 311.02 per share.",
    "ownership": "D"
  }
]
```

### `get-institutional-holders.sh` — Institutional Holders

Returns top institutional holders.

```json
[
  {
    "holder": "VANGUARD GROUP INC",
    "shares": 1300000000,
    "value": 390000000000,
    "report_date": "2026-03-31"
  }
]
```

### `get-earnings-history.sh` — Quarterly Earnings History

Returns quarterly EPS data.

```json
[
  {
    "quarter": "2026-07-30",
    "actual": 2.15,
    "estimate": 1.94,
    "surprise": 0.21,
    "surprisePercent": 10.82
  }
]
```

### `get-price-history.sh` — Historical Prices

Returns daily OHLCV data as CSV (not JSON, for easy use with analysis tools).

```
Date,Open,High,Low,Close,Volume,Dividends,Stock Splits
2021-07-13,144.50,145.15,143.55,144.87,75000000,0.0,0.0
```

The default period is 5 years. Accept an optional second argument in yfinance
period format: `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `max`.

Example: `bash get-price-history.sh AAPL 1y`

### `get-calendar.sh` — Earnings and Dividend Calendar

Returns upcoming events.

```json
{
  "earnings_date": "2026-07-30",
  "earnings_high": 1.99,
  "earnings_low": 1.83,
  "earnings_average": 1.89,
  "dividend_date": "2026-05-14",
  "ex_dividend_date": "2026-05-11"
}
```

### `get-all.sh` — Complete Data

Merges all scripts into a single JSON document. Useful when you want a full
snapshot without running 9 separate commands. Structure:

```json
{
  "info": { ... },
  "income_statement": [ ... ],
  "balance_sheet": [ ... ],
  "cash_flow": [ ... ],
  "historical_prices": "Date,Open,High,Low,Close,Volume...",
  "insider_transactions": [ ... ],
  "institutional_holders": [ ... ],
  "earnings_history": [ ... ],
  "calendar": { ... }
}
```

---

## Integration Guide for Other Skills

To make your skill depend on `stock-info`, add this note in your SKILL.md:

```
> **Data source:** This skill uses the `stock-info` skill for financial data.
> Install it at: `plugins/skills/stock-info/`
> Fetch data via: `bash plugins/skills/stock-info/tools/get-info.sh <ticker>`
> `bash plugins/skills/stock-info/tools/get-balance-sheet.sh <ticker>`
```

And in agent instructions, replace:

> `get_stock_info` tool

with:

> `bash plugins/skills/stock-info/tools/get-info.sh <ticker>` (parsed with python3 - json.tool or jq)