#!/usr/bin/env bash
# get-all.sh — Fetch all stock data in a single JSON document
# Usage: bash get-all.sh <ticker> [periods]
#   periods: number of years for financial statements (default: 5)
# Outputs JSON to stdout

TICKER="${1:?Usage: get-all.sh <ticker> [periods]}"
PERIODS="${2:-5}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Run each script individually — don't fail on individual errors
"$SCRIPT_DIR/get-info.sh" "$TICKER" > "$TMPDIR/info.json" 2>/dev/null || echo '{"error":"get-info.sh failed"}' > "$TMPDIR/info.json"
"$SCRIPT_DIR/get-income-statement.sh" "$TICKER" "$PERIODS" > "$TMPDIR/inc.json" 2>/dev/null || echo '[]' > "$TMPDIR/inc.json"
"$SCRIPT_DIR/get-balance-sheet.sh" "$TICKER" "$PERIODS" > "$TMPDIR/bs.json" 2>/dev/null || echo '[]' > "$TMPDIR/bs.json"
"$SCRIPT_DIR/get-cash-flow.sh" "$TICKER" "$PERIODS" > "$TMPDIR/cf.json" 2>/dev/null || echo '[]' > "$TMPDIR/cf.json"
"$SCRIPT_DIR/get-insider-transactions.sh" "$TICKER" > "$TMPDIR/insider.json" 2>/dev/null || echo '[]' > "$TMPDIR/insider.json"
"$SCRIPT_DIR/get-institutional-holders.sh" "$TICKER" > "$TMPDIR/holders.json" 2>/dev/null || echo '[]' > "$TMPDIR/holders.json"
"$SCRIPT_DIR/get-earnings-history.sh" "$TICKER" > "$TMPDIR/earnings.json" 2>/dev/null || echo '[]' > "$TMPDIR/earnings.json"
"$SCRIPT_DIR/get-calendar.sh" "$TICKER" > "$TMPDIR/cal.json" 2>/dev/null || echo '{}' > "$TMPDIR/cal.json"
"$SCRIPT_DIR/get-price-history.sh" "$TICKER" "5y" > "$TMPDIR/prices.csv" 2>/dev/null || echo "error" > "$TMPDIR/prices.csv"

python3 "$SCRIPT_DIR/_merge_all.py" "$TMPDIR"