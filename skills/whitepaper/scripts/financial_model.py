#!/usr/bin/env python3
"""
Financial projection model for whitepaper business cases.
Produces 5-year P&L, cash flow projection, and key metrics.

Usage: python3 financial_model.py < assumptions.json > projections.json
"""

import json
import sys
from typing import Any


def project_financials(assumptions: dict) -> dict:
    """
    Project financial statements over 5 years.

    Args:
        assumptions: dict with keys:
            - starting_revenue: float
            - revenue_growth_rates: list[float]  # 5 annual growth rates
            - cogs_percent: list[float]           # 5 annual COGS as % of revenue
            - op_ex_pct: list[float]              # 5 annual OPEX as % of revenue
            - tax_rate: float
            - capex_percent: float                # capex as % of revenue
            - dnb_percent: float                  # depreciation as % of revenue
            - working_capital_pct: float          # NWC as % of revenue change
            - debt: float
            - interest_rate: float
            - shares_outstanding: float

    Returns:
        dict with keys: income_statements, cash_flows, key_metrics
    """
    rev = assumptions["starting_revenue"]
    growth = assumptions["revenue_growth_rates"]
    cogs_pct = assumptions["cogs_percent"]
    opex_pct = assumptions["op_ex_pct"]
    tax_rate = assumptions["tax_rate"]
    capex_pct = assumptions["capex_percent"]
    dnb_pct = assumptions["dnb_percent"]
    wc_pct = assumptions["working_capital_pct"]
    debt = assumptions["debt"]
    interest = assumptions["interest_rate"]
    shares = assumptions["shares_outstanding"]

    income_statements = []
    cash_flows = []
    prev_rev = 0
    prev_wc = 0

    for year in range(5):
        rev *= (1 + growth[year])
        cogs = rev * cogs_pct[year]
        gross_profit = rev - cogs
        opex = rev * opex_pct[year]
        ebitda = gross_profit - opex
        dnb = rev * dnb_pct
        ebit = ebitda - dnb
        interest_exp = debt * interest
        ebt = ebit - interest_exp
        tax = max(0, ebt * tax_rate)
        net_income = ebt - tax

        income_statements.append({
            "year": year + 1,
            "revenue": round(rev, 2),
            "cogs": round(cogs, 2),
            "gross_profit": round(gross_profit, 2),
            "gross_margin": round(gross_profit / rev * 100, 1) if rev else 0,
            "opex": round(opex, 2),
            "ebitda": round(ebitda, 2),
            "ebitda_margin": round(ebitda / rev * 100, 1) if rev else 0,
            "depreciation": round(dnb, 2),
            "ebit": round(ebit, 2),
            "interest": round(interest_exp, 2),
            "ebt": round(ebt, 2),
            "tax": round(tax, 2),
            "net_income": round(net_income, 2),
            "eps": round(net_income / shares, 2) if shares else 0,
        })

        # Cash flow
        dnb_cf = dnb
        capex = rev * capex_pct
        delta_rev = rev - prev_rev if prev_rev else rev
        delta_wc = delta_rev * wc_pct
        operating_cf = net_income + dnb_cf - delta_wc
        free_cf = operating_cf - capex

        cash_flows.append({
            "year": year + 1,
            "net_income": round(net_income, 2),
            "depreciation_add_back": round(dnb_cf, 2),
            "working_capital_change": round(-delta_wc, 2),
            "operating_cash_flow": round(operating_cf, 2),
            "capex": round(-capex, 2),
            "free_cash_flow": round(free_cf, 2),
        })

        prev_rev = rev
        prev_wc = delta_wc

    # Key metrics
    final = income_statements[-1]
    key_metrics = {
        "year_5_revenue": final["revenue"],
        "year_5_ebitda": final["ebitda"],
        "year_5_net_income": final["net_income"],
        "year_5_eps": final["eps"],
        "total_fcf_5yr": round(sum(cf["free_cash_flow"] for cf in cash_flows), 2),
        "avg_revenue_growth": round(sum(growth) / len(growth) * 100, 1),
        "avg_ebitda_margin": round(sum(is_["ebitda_margin"] for is_ in income_statements) / 5, 1),
    }

    return {
        "income_statements": income_statements,
        "cash_flows": cash_flows,
        "key_metrics": key_metrics,
    }


def main():
    assumptions = json.load(sys.stdin)
    result = project_financials(assumptions)
    json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main()