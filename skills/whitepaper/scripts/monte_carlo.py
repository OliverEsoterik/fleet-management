#!/usr/bin/env python3
"""
Monte Carlo simulation for business projections.
Takes financial assumptions with probability distributions and
runs N iterations to produce confidence intervals.

Usage: python3 monte_carlo.py < assumptions.json > results.json
"""

import json
import sys
import random
from typing import Any


def run_monte_carlo(assumptions: dict, iterations: int = 10000) -> dict:
    """
    Run Monte Carlo simulation on financial assumptions.

    Args:
        assumptions: dict with keys:
            - revenue_growth: {"mean": float, "std": float}  # normal distribution
            - gross_margin: {"mean": float, "std": float}     # normal, clipped [0,1]
            - operating_margin: {"mean": float, "std": float} # normal, clipped
            - churn_rate: {"mean": float, "std": float}       # normal, clipped [0,1]
            - cac: {"mean": float, "std": float}              # normal
            - initial_revenue: float                          # base year revenue
            - projection_years: int                           # years to project
            - cost_structure: {"fixed": float, "variable_pct": float}
        iterations: number of simulation runs

    Returns:
        dict with keys: mean, median, p10, p90, var_95, distribution
    """
    results = []

    for _ in range(iterations):
        # Sample each assumption from its distribution
        rev_growth = random.gauss(
            assumptions["revenue_growth"]["mean"],
            assumptions["revenue_growth"]["std"]
        )
        gross_margin = max(0, min(1, random.gauss(
            assumptions["gross_margin"]["mean"],
            assumptions["gross_margin"]["std"]
        )))
        op_margin = random.gauss(
            assumptions["operating_margin"]["mean"],
            assumptions["operating_margin"]["std"]
        )
        churn = max(0, min(1, random.gauss(
            assumptions["churn_rate"]["mean"],
            assumptions["churn_rate"]["std"]
        )))
        cac = max(0, random.gauss(
            assumptions["cac"]["mean"],
            assumptions["cac"]["std"]
        ))

        # Project forward
        revenue = assumptions["initial_revenue"]
        annual_results = []
        for year in range(assumptions.get("projection_years", 5)):
            revenue *= (1 + rev_growth) * (1 - churn)
            gross_profit = revenue * gross_margin
            fixed_costs = assumptions["cost_structure"]["fixed"]
            variable_costs = revenue * assumptions["cost_structure"]["variable_pct"]
            op_income = gross_profit - fixed_costs - variable_costs
            annual_results.append({
                "year": year + 1,
                "revenue": round(revenue, 2),
                "gross_profit": round(gross_profit, 2),
                "operating_income": round(op_income, 2),
                "cac": round(cac, 2),
            })

        results.append(annual_results)

    # Compute statistics per year
    stats = []
    for year_idx in range(assumptions.get("projection_years", 5)):
        year_values = [r[year_idx] for r in results]
        revenues = [v["revenue"] for v in year_values]
        op_incomes = [v["operating_income"] for v in year_values]

        revenues.sort()
        op_incomes.sort()

        stats.append({
            "year": year_idx + 1,
            "revenue": {
                "mean": round(sum(revenues) / len(revenues), 2),
                "median": round(revenues[len(revenues) // 2], 2),
                "p10": round(revenues[int(len(revenues) * 0.1)], 2),
                "p90": round(revenues[int(len(revenues) * 0.9)], 2),
            },
            "operating_income": {
                "mean": round(sum(op_incomes) / len(op_incomes), 2),
                "median": round(op_incomes[len(op_incomes) // 2], 2),
                "p10": round(op_incomes[int(len(op_incomes) * 0.1)], 2),
                "p90": round(op_incomes[int(len(op_incomes) * 0.9)], 2),
            },
        })

    # VaR at 95%: the 5th percentile of year-5 operating income
    final_op_incomes = sorted(
        r[-1]["operating_income"] for r in results
    )
    var_95 = round(final_op_incomes[int(len(final_op_incomes) * 0.05)], 2)

    return {
        "iterations": iterations,
        "annual_stats": stats,
        "var_95": var_95,
        "summary": {
            "year_5_revenue_mean": stats[-1]["revenue"]["mean"],
            "year_5_revenue_median": stats[-1]["revenue"]["median"],
            "year_5_revenue_p10": stats[-1]["revenue"]["p10"],
            "year_5_revenue_p90": stats[-1]["revenue"]["p90"],
            "var_95_percentile": var_95,
        }
    }


def main():
    assumptions = json.load(sys.stdin)
    result = run_monte_carlo(assumptions)
    json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main()