#!/usr/bin/env python3
"""
Sandisk Corporation (SNDK) DCF Valuation - REFINED
Lyn Alden Discounted Cash Flow Methodology

Key insight: SanDisk's business has ramped dramatically. The TTM
FCF of $4.46B includes earlier, lower quarters. The Q1'26 annualized
FCF run rate is ~$12B. We model using a blended base FCF.
"""

def dcf_valuation(cash_flows, discount_rate):
    present_values = []
    for year, cf in enumerate(cash_flows, start=1):
        pv = cf / (1 + discount_rate) ** year
        present_values.append(pv)
    return sum(present_values), present_values

def terminal_value(growing_cf, growth_rate, discount_rate, perpetuity=True):
    if perpetuity and discount_rate > growth_rate:
        next_cf = growing_cf * (1 + growth_rate)
        return next_cf / (discount_rate - growth_rate)
    return 0.0

# ============================================================
# INPUTS
# ============================================================

current_price = 1915.92
market_cap = 283728150528
shares_outstanding = 148089758
diluted_shares = 157000000

total_cash = 3735000064
total_debt = 182000000
net_cash = total_cash - total_debt  # $3.553B

ttm_fcf = 4460000000
q1_2026_annualized_fcf = 2993000000 * 4
q4_2025_annualized_fcf = 980000000 * 4

print("=" * 100)
print("SANDISK CORPORATION (SNDK) - DCF VALUATION REPORT")
print("Lyn Alden Discounted Cash Flow Methodology")
print("Date: July 11, 2026")
print("=" * 100)

print(f"\n{'='*100}")
print("1. FINANCIAL SNAPSHOT")
print(f"{'='*100}")
print(f"  Current Price:            ${current_price:,.2f}")
print(f"  Market Cap:               ${market_cap/1e9:,.2f}B")
print(f"  Shares Outstanding:       {shares_outstanding/1e6:,.1f}M")
print(f"  Diluted Shares:           {diluted_shares/1e6:,.1f}M")
print(f"  TTM Revenue:              ${13184000000/1e9:,.2f}B")
print(f"  Q1'26 Quarterly Revenue:  $5.95B (annualized: $23.8B)")
print(f"  TTM Free Cash Flow:       ${ttm_fcf/1e9:,.2f}B")
print(f"  Q1'26 FCF Ann.:           ${q1_2026_annualized_fcf/1e9:.2f}B")
print(f"  Total Cash:               ${total_cash/1e9:,.2f}B")
print(f"  Total Debt:               ${total_debt/1e6:,.1f}M")
print(f"  Net Cash:                 ${net_cash/1e9:,.2f}B")
print(f"  Trailing P/E:             63.7x")
print(f"  Forward P/E:              9.4x")

print(f"\n{'='*100}")
print("2. MODEL ASSUMPTIONS")
print(f"{'='*100}")

base_fcf = (ttm_fcf + q1_2026_annualized_fcf) / 2  # $8.22B
base_fcf_ttm = ttm_fcf  # $4.46B

discount_rate = 0.12
terminal_growth = 0.03
years = 10

growth_rates_blended = [0.20, 0.20, 0.15, 0.12, 0.10, 0.08, 0.06, 0.05, 0.04, 0.03]

print(f"\nBase FCF (Blended):  ${base_fcf/1e9:.2f}B")
print(f"Discount Rate:       {discount_rate*100:.0f}%")
print(f"Terminal Growth:     {terminal_growth*100:.0f}%")
print(f"Forecast Period:     {years} years")
print(f"Growth:              front-loaded 20% tapering to 3%")

print(f"\n{'='*100}")
print("3A. PRIMARY MODEL: Blended Base FCF ($8.22B)")
print(f"{'='*100}")
print(f"{'Year':<8}{'Growth':<10}{'FCF ($B)':<12}{'PV Factor':<10}{'PV ($B)':<10}")
print("-" * 50)

flows_b = []
cf = base_fcf
for yr in range(1, years + 1):
    g = growth_rates_blended[yr - 1]
    cf *= (1 + g)
    flows_b.append(cf)
    pv_factor = 1 / (1 + discount_rate) ** yr
    pv = cf * pv_factor
    print(f"{yr:<8}{f'{g*100:.1f}%':<10}{f'${cf/1e9:.2f}':<12}{f'{pv_factor:.4f}':<10}{f'${pv/1e9:.2f}':<10}")

print("-" * 50)
total_pv_b, _ = dcf_valuation(flows_b, discount_rate)
last_cf_b = flows_b[-1]
tv_b = terminal_value(last_cf_b, terminal_growth, discount_rate)
tv_pv_b = tv_b / (1 + discount_rate) ** years

ev_b = total_pv_b + tv_pv_b
eq_b = ev_b + net_cash
fv_b = eq_b / diluted_shares
mos_b = (fv_b - current_price) / fv_b * 100

print(f"\nTerminal Value:             ${tv_b/1e9:.2f}B")
print(f"PV of Terminal Value:       ${tv_pv_b/1e9:.2f}B")
print(f"Enterprise Value:           ${ev_b/1e9:.2f}B")
print(f"Equity Value:               ${eq_b/1e9:.2f}B")
print(f"Fair Value / Share:         ${fv_b:,.2f}")
print(f"Current Price:              ${current_price:,.2f}")
print(f"Margin of Safety:           {mos_b:+.1f}%")
rec_b = "SELL / UNDERPERFORM" if mos_b < 0 else ("HOLD" if mos_b < 15 else ("BUY" if mos_b < 30 else "STRONG BUY"))
print(f"Recommendation:             {rec_b}")

print(f"\n{'='*100}")
print("3B. CONSERVATIVE MODEL: TTM FCF ($4.46B) base")
print(f"{'='*100}")
print(f"{'Year':<8}{'Growth':<10}{'FCF ($B)':<12}{'PV Factor':<10}{'PV ($B)':<10}")
print("-" * 50)

flows_c = []
cf = base_fcf_ttm
for yr in range(1, years + 1):
    g = growth_rates_blended[yr - 1]
    cf *= (1 + g)
    flows_c.append(cf)
    pv_factor = 1 / (1 + discount_rate) ** yr
    pv = cf * pv_factor
    print(f"{yr:<8}{f'{g*100:.1f}%':<10}{f'${cf/1e9:.2f}':<12}{f'{pv_factor:.4f}':<10}{f'${pv/1e9:.2f}':<10}")

print("-" * 50)
total_pv_c, _ = dcf_valuation(flows_c, discount_rate)
last_cf_c = flows_c[-1]
tv_c = terminal_value(last_cf_c, terminal_growth, discount_rate)
tv_pv_c = tv_c / (1 + discount_rate) ** years
ev_c = total_pv_c + tv_pv_c
eq_c = ev_c + net_cash
fv_c = eq_c / diluted_shares
mos_c = (fv_c - current_price) / fv_c * 100

print(f"\nEnterprise Value:           ${ev_c/1e9:.2f}B")
print(f"Equity Value:               ${eq_c/1e9:.2f}B")
print(f"Fair Value / Share:         ${fv_c:,.2f}")
print(f"Margin of Safety:           {mos_c:+.1f}%")
rec_c = "SELL / UNDERPERFORM" if mos_c < 0 else ("HOLD" if mos_c < 15 else ("BUY" if mos_c < 30 else "STRONG BUY"))
print(f"Recommendation:             {rec_c}")

# ============================================================
# SENSITIVITY ANALYSIS
# ============================================================

print(f"\n{'='*100}")
print("4. SENSITIVITY ANALYSIS (Primary Model)")
print(f"{'='*100}")

drs = [0.10, 0.11, 0.12, 0.13, 0.14]
tgs = [0.02, 0.025, 0.03, 0.035, 0.04]

print(f"{'r \\ g':<10}", end="")
for tg in tgs:
    print(f"{tg*100:.1f}%{'':<14}", end="")
print()
print("-" * (10 + 18 * len(tgs)))

for r in drs:
    print(f"{f'{r*100:.0f}%':<10}", end="")
    for tg in tgs:
        flows = []
        cf = base_fcf
        for yr in range(1, years + 1):
            g = growth_rates_blended[yr - 1]
            cf *= (1 + g)
            flows.append(cf)
        tp, _ = dcf_valuation(flows, r)
        tv = terminal_value(flows[-1], tg, r)
        tvp = tv / (1 + r) ** years
        ev = tp + tvp
        eq = ev + net_cash
        fv = eq / diluted_shares
        print(f"${fv:<8.0f}{'':<10}", end="")
    print()

# ============================================================
# SCENARIO ANALYSIS
# ============================================================

print(f"\n{'='*100}")
print("5. SCENARIO ANALYSIS")
print(f"{'='*100}")

scenarios = {
    "Optimistic": [0.25, 0.25, 0.20, 0.15, 0.12, 0.10, 0.08, 0.05, 0.04, 0.03],
    "Base Case": growth_rates_blended,
    "Cautious":   [0.15, 0.12, 0.10, 0.08, 0.06, 0.05, 0.04, 0.03, 0.03, 0.03],
    "Bearish":    [0.05, 0.03, -0.05, -0.10, 0.05, 0.08, 0.06, 0.04, 0.03, 0.03],
}

for sname, grates in scenarios.items():
    flows = []
    cf = base_fcf
    for yr in range(1, years + 1):
        g = grates[yr - 1]
        cf *= (1 + g)
        flows.append(cf)
    tp, _ = dcf_valuation(flows, discount_rate)
    tv = terminal_value(flows[-1], terminal_growth, discount_rate)
    tvp = tv / (1 + discount_rate) ** years
    ev = tp + tvp
    eq = ev + net_cash
    fv = eq / diluted_shares
    mos = (fv - current_price) / fv * 100
    srec = "SELL" if mos < 0 else ("HOLD" if mos < 15 else ("BUY" if mos < 30 else "STRONG BUY"))
    print(f"\n{sname:<15} FV: ${fv:>6.0f}  {srec:>12} ({mos:+.1f}%)")

# ============================================================
# FORWARD P/E CROSS-CHECK
# ============================================================
print(f"\n{'='*100}")
print("6. FORWARD P/E CROSS-CHECK")
print(f"{'='*100}")
implied_fwd_ni = (current_price * diluted_shares) / 9.4
print(f"\n  Forward P/E: 9.4x")
print(f"  Implied Forward Net Income: ${implied_fwd_ni/1e9:.2f}B")
print(f"  Implied FCF (80% conv):    ${implied_fwd_ni*0.8/1e9:.2f}B")
print(f"  TTM FCF Yield:             {ttm_fcf/market_cap*100:.1f}%")
print(f"  EV/TTM FCF:                {280200118272/ttm_fcf:.1f}x")
print(f"  EV/Blended FCF:            {280200118272/base_fcf:.1f}x")

print(f"\n{'='*100}")
print("7. KEY RISKS")
print(f"{'='*100}")
print("""
  1. NAND flash cyclicality - peak-cycle margins may not persist
  2. Intense competition (Samsung, Micron, Kioxia, YMTC)
  3. AI demand concentration
  4. Spin-off execution risk
  5. Already priced for perfection at current market cap
""")
