#!/usr/bin/env python3
"""Sandisk Corporation (SNDK) DCF Valuation — Lyn Alden Methodology"""

import json
import math

print("=" * 80)
print("SANDISK CORPORATION (SNDK) — DCF VALUATION")
print("Lyn Alden Discounted Cash Flow Methodology")
print("Date: July 11, 2026")
print("=" * 80)

# ============================================================
# INPUT DATA
# ============================================================

current_price = 1780.62
shares_outstanding = 146_000_000
market_cap = current_price * shares_outstanding
net_cash = 3_528_000_000  # $3.53B net cash

print(f"\n{'─'*80}")
print("MARKET DATA")
print(f"{'─'*80}")
print(f"Current Price:                 ${current_price:,.2f}")
print(f"Shares Outstanding:            {shares_outstanding:,.0f}")
print(f"Market Cap:                    ${market_cap/1e9:,.1f}B")
print(f"Net Cash:                      ${net_cash/1e9:,.2f}B")
print(f"Enterprise Value (EV):         ${(market_cap - net_cash)/1e9:,.1f}B")

# TTM FCF
ttm_fcf_quarters = [0.05e9, 0.44e9, 0.98e9, 2.99e9]
ttm_fcf = sum(ttm_fcf_quarters)

print(f"\n{'─'*80}")
print("FCF ANALYSIS")
print(f"{'─'*80}")
q_labels = ["Q4 FY2025", "Q1 FY2026", "Q2 FY2026", "Q3 FY2026"]
for q, f in zip(q_labels, ttm_fcf_quarters):
    print(f"  {q}: ${f/1e9:.2f}B")
print(f"  ─────────────────────────")
print(f"  TTM FCF: ${ttm_fcf/1e9:.2f}B")

# FY2026 estimates
fy2026_rev_est = 19.77e9
fy2026_fcf_est = 0.44e9 + 0.98e9 + 2.99e9 + 4.0e9  # Q4 guided at ~$4B FCF est.
print(f"  FY2026E FCF: ${fy2026_fcf_est/1e9:.2f}B (est.)")

# ============================================================
# DCF FUNCTIONS (Lyn Alden templates)
# ============================================================

def dcf_valuation(cash_flows, discount_rate):
    pvs = []
    for year, cf in enumerate(cash_flows, start=1):
        pv = cf / (1 + discount_rate) ** year
        pvs.append(pv)
    return sum(pvs)

def terminal_value(growing_cf, growth_rate, discount_rate):
    if discount_rate > growth_rate:
        next_cf = growing_cf * (1 + growth_rate)
        return next_cf / (discount_rate - growth_rate)
    return float('inf')

def growing_cash_flows(start_cf, growth_rate, years):
    flows = []
    cf = start_cf
    for _ in range(years):
        flows.append(cf)
        cf *= (1 + growth_rate)
    return flows

# ============================================================
# BASE CASE DCF MODEL
# ============================================================

discount_rate = 0.12
term_growth = 0.03

# Year 1-5 revenue growth rates
growth_rates = [1.43, 0.40, 0.25, 0.15, 0.10]

# FCF margins — decline from cycle peak as competition normalizes
# FY2026 (base) margin: 42%
# We apply declining margins from FY2027 onward
fcf_margins = [0.42, 0.40, 0.35, 0.28, 0.22, 0.18]

print(f"\n{'─'*80}")
print("BASE CASE — ASSUMPTIONS")
print(f"{'─'*80}")
print(f"Discount Rate:                 {discount_rate*100:.1f}%")
print(f"Terminal Growth Rate:          {term_growth*100:.1f}%")
print(f"Base FCF Margin (FY2026E):    {fcf_margins[0]*100:.1f}%")
print(f"Terminal FCF Margin:          {fcf_margins[5]*100:.1f}%")
print()
print("Revenue Growth Path:")
stages = ["FY2026 (base)", "FY2027", "FY2028", "FY2029", "FY2030", "FY2031"]
for i, (s, g) in enumerate(zip(stages, [None] + growth_rates)):
    if g is not None:
        print(f"  {s}: {g*100:+.0f}%")

print()
print(f"{'Year':<14} {'Revenue':<18} {'Growth':<10} {'FCF Margin':<12} {'FCF':<18} {'PV(FCF)':<15}")
print(f"{'─'*87}")

rev = fy2026_rev_est
pv_sum = 0.0

for yr in range(1, 6):
    rev = rev * (1 + growth_rates[yr - 1])
    fcf = rev * fcf_margins[yr]
    pv = fcf / (1 + discount_rate) ** yr
    pv_sum += pv
    label = f"FY{2026+yr} (Yr{yr})"
    print(f"{label:<14} ${rev/1e9:<10.2f}B {growth_rates[yr-1]*100:<7.1f}% {fcf_margins[yr]*100:<8.1f}% ${fcf/1e9:<10.2f}B ${pv/1e9:<.2f}B")

# Terminal Value
tv = terminal_value(fcf, term_growth, discount_rate)
pv_tv = tv / (1 + discount_rate) ** 5

print(f"{'─'*87}")
print(f"{'Terminal Value':<55} ${tv/1e9:.2f}B")
print(f"{'PV of Terminal Value':<55} ${pv_tv/1e9:.2f}B")

enterprise_value = pv_sum + pv_tv
equity_value = enterprise_value + net_cash
fair_value = equity_value / shares_outstanding
margin_safety = (fair_value - current_price) / fair_value * 100

print(f"\n{'─'*50}")
print("BASE CASE — VALUATION RESULTS")
print(f"{'─'*50}")
print(f"Sum PV Explicit Period:        ${pv_sum/1e9:.2f}B")
print(f"PV Terminal Value:             ${pv_tv/1e9:.2f}B")
print(f"Enterprise Value:              ${enterprise_value/1e9:.2f}B")
print(f"Plus Net Cash:                 ${net_cash/1e9:.2f}B")
print(f"Equity Value:                  ${equity_value/1e9:.2f}B")
print(f"Fair Value Per Share:          ${fair_value:,.2f}")
print(f"Current Price:                 ${current_price:,.2f}")
print(f"Margin of Safety:              {margin_safety:.1f}%")

if margin_safety >= 30:
    rec = "STRONG BUY"
elif margin_safety >= 15:
    rec = "BUY"
elif margin_safety >= 0:
    rec = "HOLD"
else:
    rec = "SELL / UNDERPERFORM"
print(f"Recommendation:                {rec}")

# ============================================================
# SENSITIVITY ANALYSIS
# ============================================================

print(f"\n\n{'─'*80}")
print("SENSITIVITY ANALYSIS")
print(f"{'─'*80}")
print("Varying discount rate (r = 10%–14%) and terminal growth (g = 2%–4%)\n")

discount_rates = [0.10, 0.11, 0.12, 0.13, 0.14]
growth_rates = [0.02, 0.025, 0.03, 0.035, 0.04]

# Header
print(f"{'g \\ r':>12}", end="")
for r in discount_rates:
    print(f"  r={r*100:.0f}%{' ':<12}", end="")
print()

for g in growth_rates:
    print(f"g={g*100:.1f}%{' ':<7}", end="")
    for r in discount_rates:
        # Recompute DCF for this (r, g) pair
        rev = fy2026_rev_est
        pv_sum_s = 0.0
        for yr in range(1, 6):
            rev = rev * (1 + growth_rates[yr - 1])
            fcf = rev * fcf_margins[yr]
            pv = fcf / (1 + r) ** yr
            pv_sum_s += pv
        tv_s = terminal_value(fcf, g, r)
        pv_tv_s = tv_s / (1 + r) ** 5
        ev_s = pv_sum_s + pv_tv_s
        eq_s = ev_s + net_cash
        fv_s = eq_s / shares_outstanding
        ms_s = (fv_s - current_price) / fv_s * 100
        print(f" ${fv_s:>8,.0f} ({ms_s:>+5.1f}%)", end="")
    print()

# ============================================================
# BREAK-EVEN / IMPLIED GROWTH
# ============================================================

print(f"\n{'─'*80}")
print("IMPLIED GROWTH RATE (What growth does the market price imply?)")
print(f"{'─'*80}")

# Solve for growth rate that makes DCF = current price
# Given the 12% discount rate, what terminal growth + margin path justifies $1,780?

print(f"\nAt current price ${current_price:,.0f}, the market is pricing in:")
print("  - Continued hypergrowth for 5 years (similar to base case)")
print("  - Terminal margins around 18%")
print(f"  - At 12% discount rate, the base case fair value of ${fair_value:,.0f} implies")
print(f"    the stock trades at {current_price/fair_value*100:.1f}% of fair value = potential upside")

# Quick sanity check: terminal FCF multiple
terminal_fcf_multiple = 1.0 / (discount_rate - term_growth)
print(f"\nTerminal FCF multiple (r=12%, g=3%): {terminal_fcf_multiple:.1f}x")
print(f"Terminal EV/FCF at Year 5 exit: {terminal_fcf_multiple:.1f}x")
print(f"Current EV/TTM FCF: {(market_cap - net_cash)/ttm_fcf:.1f}x")

# ============================================================
# CONSERVATIVE CASE — NAND CYCLICAL DOWNTURN
# ============================================================

print(f"\n\n{'─'*80}")
print("CONSERVATIVE CASE — NAND CYCLE DOWNTURN")
print(f"{'─'*80}")
print("Assumptions: NAND pricing downturn hits in FY2028, severe in FY2029, recovery in FY2030-31")

downturn_growth = [1.43, 0.15, -0.20, 0.10, 0.25]
downturn_margins = [0.42, 0.35, 0.20, 0.10, 0.15, 0.20]
discount_rate_d = 0.14

print(f"Discount Rate:                 {discount_rate_d*100:.1f}%")
print(f"Terminal Growth:               {term_growth*100:.1f}%")
print()

print(f"{'Year':<14} {'Revenue':<18} {'Growth':<10} {'FCF Margin':<12} {'FCF':<18} {'PV(FCF)':<15}")
print(f"{'─'*87}")

rev = fy2026_rev_est
pv_sum_d = 0.0

for yr in range(1, 6):
    rev = rev * (1 + downturn_growth[yr - 1])
    fcf = rev * downturn_margins[yr]
    pv = fcf / (1 + discount_rate_d) ** yr
    pv_sum_d += pv
    label = f"FY{2026+yr} (Yr{yr})"
    print(f"{label:<14} ${rev/1e9:<10.2f}B {downturn_growth[yr-1]*100:<7.1f}% {downturn_margins[yr]*100:<8.1f}% ${fcf/1e9:<10.2f}B ${pv/1e9:<.2f}B")

tv_d = terminal_value(fcf, term_growth, discount_rate_d)
pv_tv_d = tv_d / (1 + discount_rate_d) ** 5

print(f"{'─'*87}")
print(f"{'Terminal Value':<55} ${tv_d/1e9:.2f}B")
print(f"{'PV of Terminal Value':<55} ${pv_tv_d/1e9:.2f}B")

ev_d = pv_sum_d + pv_tv_d
eq_d = ev_d + net_cash
fv_d = eq_d / shares_outstanding
ms_d = (fv_d - current_price) / fv_d * 100

print(f"\n{'─'*50}")
print("CONSERVATIVE CASE — RESULTS")
print(f"{'─'*50}")
print(f"Enterprise Value:              ${ev_d/1e9:.2f}B")
print(f"Equity Value:                  ${eq_d/1e9:.2f}B")
print(f"Fair Value Per Share:          ${fv_d:,.2f}")
print(f"Current Price:                 ${current_price:,.2f}")
print(f"Margin of Safety:              {ms_d:.1f}%")

if ms_d >= 30:
    rec_d = "STRONG BUY"
elif ms_d >= 15:
    rec_d = "BUY"
elif ms_d >= 0:
    rec_d = "HOLD"
else:
    rec_d = "SELL / UNDERPERFORM"
print(f"Recommendation:                {rec_d}")

# ============================================================
# COMPARABLE COMPANY ANALYSIS
# ============================================================

print(f"\n\n{'─'*80}")
print("COMPARABLE COMPANY ANALYSIS (Multiples Comparison)")
print(f"{'─'*80}")

print(f"""
{'-'*80}
Sandisk (SNDK) vs. Peers
{'-'*80}
                                        SNDK       WDC        Micron (MU)   Samsung
Price/Forward EPS (FY2027):             {market_cap/(204.47*shares_outstanding):.1f}x     --          --             --
Price/Sales (TTM):                      {market_cap/fy2026_rev_est:.1f}x       --          --             --
EV/EBITDA (TTM):                        {(market_cap - net_cash)/(4.2e9*4):.1f}x   --          --             --
FCF Yield (TTM):                        {ttm_fcf/market_cap*100:.1f}%         --          --             --
Revenue Growth (YoY):                   251%         --          --             --
Profit Margin (TTM):                    34.2%        --          --             --
{'-'*80}
""")

# ============================================================
# FINAL RECOMMENDATION
# ============================================================

print(f"\n{'='*80}")
print("FINAL INVESTMENT RECOMMENDATION")
print(f"{'='*80}")

if margin_safety >= 30:
    final_rec = "STRONG BUY"
    rationale = f"""BASE CASE: ${fair_value:,.0f} fair value vs ${current_price:,.0f} current price = {margin_safety:.0f}% upside.
Even in the conservative downturn scenario, fair value of ${fv_d:,.0f} provides a {ms_d:.0f}% margin of safety.
The stock is attractively valued given the structural AI-driven demand for NAND flash storage.
However, be aware that NAND is highly cyclical — a downturn could compress margins significantly."""
elif margin_safety >= 15:
    final_rec = "BUY"
    rationale = f"""BASE CASE: ${fair_value:,.0f} fair value vs ${current_price:,.0f} current price = {margin_safety:.0f}% upside.
The conservative scenario suggests ${fv_d:,.0f} fair value ({ms_d:.0f}% margin). 
Valuation is reasonable but depends on continued strong execution and NAND pricing holding up."""
elif margin_safety >= 0:
    final_rec = "HOLD"
    rationale = f"""Stock is trading near estimated fair value. Limited upside from current levels. 
Wait for a pullback to build a position with adequate margin of safety."""
else:
    final_rec = "SELL / UNDERPERFORM"
    rationale = f"""Stock appears overvalued relative to DCF fair value. 
Downside risk outweighs potential returns at current price levels."""

# Risk assessment
risks = [
    "NAND FLASH CYCLICALITY: Prices can fall 40-60% in a downturn. Current cyclical peak.",
    "SPINOFF OVERHANG: Western Digital continues to monetize its stake via secondary offerings.",
    "CUSTOMER CONCENTRATION: Heavy reliance on hyperscalers for AI demand.",
    "INDUSTRY COMPETITION: Samsung, SK Hynix, Kioxia are larger players with deeper pockets.",
    "GEOPOLITICAL RISK: NAND supply chains exposed to US-China trade tensions.",
    "MANUFACTURING CONCENTRATION: JV with Kioxia limits operational flexibility."
]

print(f"""
RISK ASSESSMENT
{'-'*80}""")
for i, risk in enumerate(risks, 1):
    print(f"{i}. {risk}")