#!/usr/bin/env python3
"""Sandisk Corporation (SNDK) — Refined DCF Valuation (Lyn Alden Methodology)"""

import math

print("=" * 80)
print("SANDISK CORPORATION (SNDK) — REFINED DCF VALUATION")
print("Lyn Alden Discounted Cash Flow Methodology")
print("Date: July 11, 2026")
print("=" * 80)

# ============================================================
# MARKET DATA
# ============================================================

current_price = 1780.62
net_cash = 3_528_000_000

# Yahoo reports sharesOutstanding=148,089,758 and marketCap=283,728,150,528
# But 148,089,758 * 1780.62 = $263.7B, not $283.7B
# The discrepancy may be due to Yahoo computing market cap differently
# Let's use the data internally consistently
shares_yahoo = 148_090_000
shares_reported = 146_000_000  # From financial statement line items

print(f"\n{'─'*80}")
print("MARKET DATA")
print(f"{'─'*80}")
print(f"Current Price:                 ${current_price:,.2f}")
print(f"Shares Outstanding (Yahoo):    {shares_yahoo:,.0f}")
print(f"Shares Outstanding (Fin St.):  {shares_reported:,.0f}")
print(f"Net Cash:                      ${net_cash/1e9:,.2f}B")
print(f"Enterprise Value (reported):   $280.2B")

# Trailing data
ttm_fcf = 4.46e9
ttm_revenue = 13.18e9
print(f"\nTTM Revenue:                   ${ttm_revenue/1e9:.2f}B")
print(f"TTM FCF:                       ${ttm_fcf/1e9:.2f}B")

# ============================================================
# FY2026 Actual/Estimated
# ============================================================

fy26_q1_rev = 2.31e9
fy26_q2_rev = 3.03e9
fy26_q3_rev = 5.95e9
fy26_q4_rev_guide = 8.05e9  # Midpoint $7.8-8.3B

fy26_q1_fcf = 0.44e9
fy26_q2_fcf = 0.98e9
fy26_q3_fcf = 2.99e9
fy26_q4_fcf_est = 4.0e9

fy26_revenue = fy26_q1_rev + fy26_q2_rev + fy26_q3_rev + fy26_q4_rev_guide
fy26_fcf = fy26_q1_fcf + fy26_q2_fcf + fy26_q3_fcf + fy26_q4_fcf_est

print(f"\nFY2026 (ending Jun 30, 2026) — Current Fiscal Year")
print(f"  Revenue: ${fy26_revenue/1e9:.2f}B")
print(f"  FCF:     ${fy26_fcf/1e9:.2f}B")
print(f"  FCF Margin: {fy26_fcf/fy26_revenue*100:.1f}%")
print(f"  Revenue Run-rate (Q4): ${fy26_q4_rev_guide*4/1e9:.0f}B annualized")

# ============================================================
# DCF HELPERS
# ============================================================

def pv(cf, r, n):
    return cf / (1 + r) ** n

def terminal_value(fcf_last, g, r):
    next_cf = fcf_last * (1 + g)
    return next_cf / (r - g)

# ============================================================
# SCENARIO A: BASE CASE
# ============================================================

print(f"\n{'='*80}")
print("SCENARIO A: BASE CASE — Moderate Margin Normalization")
print(f"{'='*80}")
print("r = 12%, g = 3%")
print("Growth: +143%, +40%, +25%, +15%, +10%")
print("Margins: 40%, 35%, 28%, 22%, 18%")

r_a, g_a = 0.12, 0.03
growth_a = [1.43, 0.40, 0.25, 0.15, 0.10]
margin_a = [0.40, 0.35, 0.28, 0.22, 0.18]

print(f"\n{'Year':<12}{'Growth':<10}{'Revenue':<14}{'FCF Margin':<12}{'FCF':<14}{'PV(FCF)':<12}")
print("-" * 74)
rev = fy26_revenue
total_pv = 0.0
for yr in range(1, 6):
    g = growth_a[yr-1]
    rev = rev * (1 + g)
    f = rev * margin_a[yr-1]
    pv_f = pv(f, r_a, yr)
    total_pv += pv_f
    print(f"FY{2026+yr:<5}{g*100:>+7.1f}%  ${rev/1e9:<7.2f}B  {margin_a[yr-1]*100:>5.1f}%     ${f/1e9:<6.2f}B  ${pv_f/1e9:<.2f}B")

tv_a = terminal_value(f, g_a, r_a)
pv_tv_a = pv(tv_a, r_a, 5)
ev_a = total_pv + pv_tv_a
eq_a = ev_a + net_cash

print("-" * 74)
print(f"Terminal Value:              ${tv_a/1e9:.2f}B")
print(f"PV of Terminal Value:        ${pv_tv_a/1e9:.2f}B")

fv_a = eq_a / shares_yahoo
fv_a2 = eq_a / shares_reported
ms_a = (fv_a - current_price) / fv_a * 100
ms_a2 = (fv_a2 - current_price) / fv_a2 * 100

print(f"\nEnterprise Value:  ${ev_a/1e9:.2f}B")
print(f"Equity Value:      ${eq_a/1e9:.2f}B")
print(f"FV/Share (Yahoo sh): ${fv_a:,.0f}  (MS: {ms_a:.1f}%)")
print(f"FV/Share (F/S sh):   ${fv_a2:,.0f}  (MS: {ms_a2:.1f}%)")

# ============================================================
# SCENARIO B: BULL CASE
# ============================================================

print(f"\n\n{'='*80}")
print("SCENARIO B: BULL CASE — Sustained AI Super-cycle")
print(f"{'='*80}")
print("r = 11%, g = 3.5%")
print("Growth: +143%, +45%, +30%, +20%, +15%")
print("Margins: 42%, 38%, 35%, 30%, 25%")

r_b, g_b = 0.11, 0.035
growth_b = [1.43, 0.45, 0.30, 0.20, 0.15]
margin_b = [0.42, 0.38, 0.35, 0.30, 0.25]

print(f"\n{'Year':<12}{'Growth':<10}{'Revenue':<14}{'FCF Margin':<12}{'FCF':<14}{'PV(FCF)':<12}")
print("-" * 74)
rev = fy26_revenue
total_pv_b = 0.0
for yr in range(1, 6):
    g = growth_b[yr-1]
    rev = rev * (1 + g)
    f = rev * margin_b[yr-1]
    pv_f = pv(f, r_b, yr)
    total_pv_b += pv_f
    print(f"FY{2026+yr:<5}{g*100:>+7.1f}%  ${rev/1e9:<7.2f}B  {margin_b[yr-1]*100:>5.1f}%     ${f/1e9:<6.2f}B  ${pv_f/1e9:<.2f}B")

tv_b = terminal_value(f, g_b, r_b)
pv_tv_b = pv(tv_b, r_b, 5)
ev_b = total_pv_b + pv_tv_b
eq_b = ev_b + net_cash
fv_b = eq_b / shares_reported
ms_b = (fv_b - current_price) / fv_b * 100

print("-" * 74)
print(f"Terminal Value:              ${tv_b/1e9:.2f}B")
print(f"PV of Terminal Value:        ${pv_tv_b/1e9:.2f}B")
print(f"\nEnterprise Value:  ${ev_b/1e9:.2f}B")
print(f"Equity Value:      ${eq_b/1e9:.2f}B")
print(f"FV/Share: ${fv_b:,.0f}  (MS: {ms_b:.1f}%)")

# ============================================================
# SCENARIO C: CONSERVATIVE
# ============================================================

print(f"\n\n{'='*80}")
print("SCENARIO C: CONSERVATIVE — NAND Cyclical Downturn")
print(f"{'='*80}")
print("r = 14%, g = 3%")
print("Growth: +143%, +15%, -20%, +10%, +25%")
print("Margins: 35%, 20%, 10%, 15%, 20%")

r_c, g_c = 0.14, 0.03
growth_c = [1.43, 0.15, -0.20, 0.10, 0.25]
margin_c = [0.35, 0.20, 0.10, 0.15, 0.20]

print(f"\n{'Year':<12}{'Growth':<10}{'Revenue':<14}{'FCF Margin':<12}{'FCF':<14}{'PV(FCF)':<12}")
print("-" * 74)
rev = fy26_revenue
total_pv_c = 0.0
for yr in range(1, 6):
    g = growth_c[yr-1]
    rev = rev * (1 + g)
    f = rev * margin_c[yr-1]
    pv_f = pv(f, r_c, yr)
    total_pv_c += pv_f
    print(f"FY{2026+yr:<5}{g*100:>+7.1f}%  ${rev/1e9:<7.2f}B  {margin_c[yr-1]*100:>5.1f}%     ${f/1e9:<6.2f}B  ${pv_f/1e9:<.2f}B")

tv_c = terminal_value(f, g_c, r_c)
pv_tv_c = pv(tv_c, r_c, 5)
ev_c = total_pv_c + pv_tv_c
eq_c = ev_c + net_cash
fv_c = eq_c / shares_reported
ms_c = (fv_c - current_price) / fv_c * 100

print("-" * 74)
print(f"Terminal Value:              ${tv_c/1e9:.2f}B")
print(f"PV of Terminal Value:        ${pv_tv_c/1e9:.2f}B")
print(f"\nEnterprise Value:  ${ev_c/1e9:.2f}B")
print(f"Equity Value:      ${eq_c/1e9:.2f}B")
print(f"FV/Share: ${fv_c:,.0f}  (MS: {ms_c:.1f}%)")

# ============================================================
# SENSITIVITY MATRIX (Base Case parameters)
# ============================================================

print(f"\n\n{'='*80}")
print("SENSITIVITY ANALYSIS")
print(f"{'='*80}")
print("Varying discount rate (r) and terminal growth (g)")
print("Values shown: Fair Value per Share and Margin of Safety")
print()

discount_rates = [0.10, 0.11, 0.12, 0.13, 0.14]
growth_rates = [0.02, 0.025, 0.03, 0.035, 0.04]

# Use base case growth and margin trajectory for sensitivity
print(f"{'':>12}", end="")
for r in discount_rates:
    print(f"  r={r*100:.0f}%{' ':<15}", end="")
print()
print(f"{'':>12}", end="")
for r in discount_rates:
    print(f"{'FV      MS%':>20}", end="")
print()

for g in growth_rates:
    print(f"g={g*100:.1f}%{' ':<7}", end="")
    for r in discount_rates:
        rev = fy26_revenue
        pv_sum = 0.0
        for yr in range(1, 6):
            rev = rev * (1 + growth_a[yr-1])
            f = rev * margin_a[yr-1]
            pv_sum += pv(f, r, yr)
        tv = terminal_value(f, g, r)
        pv_tv_g = pv(tv, r, 5)
        ev = pv_sum + pv_tv_g
        eq = ev + net_cash
        fv_g = eq / shares_reported
        ms_g = (fv_g - current_price) / fv_g * 100
        print(f"  ${fv_g:>7,.0f} ({ms_g:>+5.1f}%)", end="")
    print()

# ============================================================
# MULTIPLES CHECK
# ============================================================

print(f"\n\n{'='*80}")
print("MULTIPLES CROSS-CHECK")
print(f"{'='*80}")

fy2027_eps_est = 204.47
fy2026_eps_est = 66.41

print(f"""
Current Price: ${current_price:,.2f}
Forward P/E (FY2026E @ ${fy2026_eps_est:.2f}): {current_price/fy2026_eps_est:.1f}x
Forward P/E (FY2027E @ ${fy2027_eps_est:.2f}): {current_price/fy2027_eps_est:.1f}x
Price/Sales (TTM):              ${current_price * shares_reported / ttm_revenue:.1f}x
EV/TTM FCF:                     ${(current_price*shares_reported - net_cash)/ttm_fcf:.1f}x

Comparable: WDC trades at ~$572, P/E ~12x
Comparable: Micron (MU) trades at ~15x forward earnings
NAND cyclical stocks historically trade at 5-12x peak earnings

At 8.7x FY2027 consensus EPS of $204.47 → implied price of $1,779
This is EXACTLY the current price — the market is pricing in FY2027 EPS with zero growth multiple.

The key question is whether FY2027 EPS is sustainable or is a cyclical peak.
""")

# ============================================================
# FINAL RECOMMENDATION
# ============================================================

print(f"\n{'='*80}")
print("FINAL INVESTMENT RECOMMENDATION")
print(f"{'='*80}")

print(f"""
Based on Lyn Alden DCF methodology across three scenarios:

SCENARIO          Fair Value     Margin of Safety
Base Case:        ${fv_a2:,.0f}         {ms_a2:.1f}%
Bull Case:        ${fv_b:,.0f}         {ms_b:.1f}%
Conservative:     ${fv_c:,.0f}         {ms_c:.1f}%

RECOMMENDATION: {'BUY' if ms_a2 >= 10 else 'HOLD'} (Base case) / {'STRONG BUY' if ms_a2 >= 30 else 'BUY' if ms_a2 >= 15 else 'HOLD'} 

SANDISK (SNDK) — Key Investment Thesis:

BULLISH FACTORS:
• AI data center demand exceeding supply; NAND TAM projected to grow 281% in 2026
• Zero net debt; $3.5B net cash position provides balance sheet resilience
• Pure-play NAND exposure in a structural AI-driven upcycle
• 4 consecutive earnings beats with accelerating magnitude
• Forward P/E of 8.7x on FY2027 consensus — inexpensive for 143% revenue growth
• HBF (High Bandwidth Flash) with SK Hynix opens new market in 2027+

BEARISH FACTORS:
• NAND is highly cyclical — prices can fall 40-60% peak-to-trough
• Current 78% gross margins are at/near cycle peak levels
• 5th in NAND market share (~12%) behind larger competitors
• Spinoff overhang from WDC monetization
• Base case DCF suggests fair value in ${fv_a2:,.0f}-{fv_b:,.0f} range
• Conservative downturn scenario implies significant downside to ${fv_c:,.0f}

CONCLUSION:
At ${current_price:,.0f}, Sandisk trades at ~8.7x FY2027 consensus EPS, which is 
inexpensive for its growth rate. This is the critical split: DCF says the stock is 
{'expensive' if ms_a2 < 0 else 'fairly valued to cheap' if ms_a2 < 15 else 'attractively priced'} 
relative to fundamental fair value, while the P/E multiple suggests it is pricing in 
a cyclical peak that may not materialize. The bull case requires sustained AI-driven 
NAND demand beyond FY2027. The conservative case shows what happens if the cycle turns.

The key decision factor is whether the current NAND super-cycle is structural (AI 
driving permanent demand shift) or cyclical (supply constraints + temporary 
hyperscaler capex). TrendForce's $270B+ NAND TAM projection for 2026 supports the 
structural thesis, but NAND history argues for cyclicality.

RISK-ADJUSTED VIEW:
```
Scenario      | Probability | Fair Value | Weighted
Base Case     | 50%         | ${fv_a2:,.0f}      | ${fv_a2*0.50:,.0f}
Bull Case     | 25%         | ${fv_b:,.0f}      | ${fv_b*0.25:,.0f}
Conservative  | 25%         | ${fv_c:,.0f}      | ${fv_c*0.25:,.0f}
Weighted Avg  |             |            | ${fv_a2*0.5 + fv_b*0.25 + fv_c*0.25:,.0f}
```

At ${current_price:,.0f}, the probability-weighted fair value suggests the stock is 
{'overvalued' if current_price > (fv_a2*0.5 + fv_b*0.25 + fv_c*0.25) else 'undervalued'}.

TRADING RECOMMENDATION:
{'SELL' if ms_a2 < -10 else 'HOLD (wait for better entry)' if ms_a2 < 10 else 'BUY' if ms_a2 < 30 else 'STRONG BUY'}