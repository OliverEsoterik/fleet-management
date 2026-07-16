#!/usr/bin/env python3
# _merge_all.py — Merge stock-info temp files into a single JSON document
# Usage: python3 _merge_all.py <tmpdir>
# Reads: info.json, inc.json, bs.json, cf.json, prices.csv, insider.json,
#        holders.json, earnings.json, cal.json from <tmpdir>
# Outputs merged JSON to stdout

import json
import os
import sys


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def load_csv(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return ""


def main():
    tmpdir = sys.argv[1]

    data = {
        "info": load_json(os.path.join(tmpdir, "info.json")),
        "income_statement": load_json(os.path.join(tmpdir, "inc.json")),
        "balance_sheet": load_json(os.path.join(tmpdir, "bs.json")),
        "cash_flow": load_json(os.path.join(tmpdir, "cf.json")),
        "historical_prices": load_csv(os.path.join(tmpdir, "prices.csv")),
        "insider_transactions": load_json(os.path.join(tmpdir, "insider.json")),
        "institutional_holders": load_json(os.path.join(tmpdir, "holders.json")),
        "earnings_history": load_json(os.path.join(tmpdir, "earnings.json")),
        "calendar": load_json(os.path.join(tmpdir, "cal.json")),
    }

    print(json.dumps(data, indent=2, default=str))


if __name__ == "__main__":
    main()