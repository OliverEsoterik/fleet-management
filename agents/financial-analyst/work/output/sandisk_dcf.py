#!/usr/bin/env python3
"""
Sandisk Corporation (SNDK) DCF Valuation
Lyn Alden Discounted Cash Flow Methodology
"""

def dcf_valuation(cash_flows, discount_rate):
    """Calculate DCF from a list of annual cash flows and a discount rate."""
    present_values = []
    for year, cf in enumerate(cash_flows, start=1):
        pv = cf / (1 + discount_rate) ** year
        present_values.append(pv)
    return sum(present_values), present_values

def terminal_value(growing_cf, growth_rate, discount_rate, perpetuity=True):
    """Terminal value of a growing perpetuity: CF_next / (r - g)"""
    if perpetuity and discount_rate > growth_rate:
        next_cf = growing_cf * (1 + growth_rate)
        return next_cf / (discount_rate - growth_rate)
    return 0.0

# ============================================================
# INPUTS
# ============================================================

current_price = 1915.92
market_cap = 283728150528
enterprise_value_reported = 280200118272
shares_outstanding = 148089758
diluted_shares = 157000000

total_cash = 3735000064
total_debt = 182000000
net_cash = total_cash - total_debt  # $3.553B net cash

ttm_fcf = 4460000000  # $4.46B
ttm_revenue = 13184000000

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
print(f"  Enterprise Value:         ${enterprise_value_reported/1e9:,.2f}B")
print(f"  Shares Outstanding:       {shares_outstanding/1e6:,.1f}M")
print(f"  Diluted Shares:           {diluted_shares/1e6:,.1f}M")
print(f"  TTM Revenue:              ${ttm_revenue/1e9:,.2f}B")
print(f"  TTM Free Cash Flow:       ${ttm_fcf/1e9:,.2f}B")
print(f"  Total Cash:               ${total_cash/1e9:,.2f}B")
print(f"  Total Debt:               ${total_debt/1e6:,.1f}M")
print(f"  Net Cash:                 ${net_cash/1e9:,.2f}B")
print(f"  Trailing P/E:             63.7x (distorted by spin-off charges)")
print(f"  Forward P/E:              9.4x")
print(f"  EV/Revenue:               21.3x")
print(f"  EV/EBITDA:                49.8x")
print(f"  Gross Margin:             {56.0:.1f}%")
print(f"  Operating Margin:         {70.0:.1f}%")
print(f"  Net Profit Margin:        {34.2:.1f}%")
print(f"  Revenue Growth (YoY Q1'26): ~251% (extraordinary AI-driven ramp)")

print(f"\n{'='*100}")
print("2. ASSUMPTIONS & RATIONALE")
print(f"{'='*100}")

print("""
DISCOUNT RATE: 12.0%
  Rationale: SanDisk is a standalone publicly-traded company in the cyclical
  NAND flash semiconductor industry. 12% accounts for:
  (a) Industry cyclicality - NAND flash is a commodity market with boom-bust
      pricing cycles (Samsung, Micron see 30-40% revenue swings)
  (b) Execution risk as a newly independent company post-WDC spin-off
  (c) Technology/competitive risk vs Samsung, Micron, Kioxia, YMTC
  (d) Per Lyn Alden's framework, public stocks range 10-12%; we use the
      upper end given the cyclical nature of the flash memory industry.

REVENUE/FCF GROWTH TRAJECTORY:
  TTM revenue of $13.2B and FCF of $4.46B reflect a cyclical upswing driven
  by AI/ML data center demand for high-capacity SSDs and enterprise storage.
  Recent quarterly ramp: $1.7B -> $1.9B -> $2.3B -> $3.0B -> $5.95B (Q1'26)
  This growth rate (~250% YoY) is NOT sustainable. We model a gradual
  normalization to long-term trends:

  Year 1 (2027):   +15%  - Strong AI tailwinds continue, capacity additions
  Year 2 (2028):   +15%  - Enterprise SSD adoption remains robust
  Year 3 (2029):   +15%  - Near-peak of current cycle
  Year 4 (2030):   +10.5% - Cycle begins normalizing
  Year 5 (2031):   +10.5% - Continued normalization
  Year 6 (2032):   +7.5%  - Mature growth phase
  Year 7 (2033):   +7.5%  - Steady state
  Year 8 (2034):   +5.0%  - Converging to terminal
  Year 9 (2035):   +4.0%  - Converging to terminal
  Year 10 (2036):  +3.0%  - Terminal growth rate

TERMINAL GROWTH RATE: 3.0%
  Rationale: Long-term GDP-like growth for a mature NAND flash company.
  NAND demand grows with global data generation, but pricing pressure from
  commoditization limits nominal revenue growth to ~GDP+ over full cycles.

FCF MARGIN: ~34% maintained (above industry average)
  Current FCF margins are exceptional (~34%). We conservatively project FCF
  growth at the same rate as the business, implying maintained margins.

FORECAST PERIOD: 10 years (explicit) + terminal value
""")

# ============================================================
# DCF MODEL
# ============================================================

discount_rate = 0.12
terminal_growth = 0.03
base_fcf = ttm_fcf
years = 10

growth_rates = [0.15, 0.15, 0.15, 0.105, 0.105, 0.075, 0.075, 0.05, 0.04, 0.03]

print(f"{'='*100}")
print("3. PROJECTED FREE CASH FLOWS (10-Year Explicit Period)")
print(f"{'='*100}")
print(f"{'Year':<8}{'Growth':<12}{'FCF ($M)':<18}{'PV Factor':<12}{'PV of FCF ($M)':<15}")
print("-" * 65)

flows = []
cf = base_fcf
for yr in range(1, years + 1):
    g = growth_rates[yr - 1]
    cf *= (1 + g)
    flows.append(cf)
    pv_factor = 1 / (1 + discount_rate) ** yr
    pv = cf * pv_factor
    print(f"{yr:<8}{f'{g*100:.1f}%':<12}{f'${cf/1e6:,.0f}':<18}{f'{pv_factor:.4f}':<12}{f'${pv/1e6:,.0f}':<15}")

print("-" * 65)
total_pv, pvs = dcf_valuation(flows, discount_rate)
print(f"{'Total PV (10yr):':<30} ${total_pv/1e6:,.0f}M  (${total_pv/1e9:.2f}B)")

last_cf = flows[-1]
tv = terminal_value(last_cf, terminal_growth, discount_rate)
tv_pv = tv / (1 + discount_rate) ** years

print(f"{'Terminal Value (undiscounted):':<30} ${tv/1e6:,.0f}M  (${tv/1e9:.2f}B)")
print(f"{'PV of Terminal Value:':<30} ${tv_pv/1e6:,.0f}M  (${tv_pv/1e9:.2f}B)")
print()

# ============================================================
# VALUATION SUMMARY
# ============================================================

enterprise_value = total_pv + tv_pv
equity_value = enterprise_value + net_cash

fair_value_per_share_diluted = equity_value / diluted_shares
fair_value_per_share_basic = equity_value / shares_outstanding

print(f"\n{'='*100}")
print("4. VALUATION SUMMARY")
print(f"{'='*100}")
print(f"{'PV of Explicit Period FCFs:':<40} ${total_pv/1e9:,.2f}B")
print(f"{'PV of Terminal Value:':<40} ${tv_pv/1e9:,.2f}B")
print(f"{'Enterprise Value (DCF):':<40} ${enterprise_value/1e9:,.2f}B")
print(f"{'Plus: Net Cash:':<40} ${net_cash/1e9:,.2f}B")
print(f"{'Equity Value:':<40} ${equity_value/1e9:,.2f}B")
print(f"{'Diluted Shares Outstanding:':<40} {diluted_shares/1e6:,.1f}M")
print(f"{'Fair Value Per Share (diluted):':<40} ${fair_value_per_share_diluted:,.2f}")
print(f"{'Current Market Price:':<40} ${current_price:,.2f}")

margin_of_safety = (fair_value_per_share_diluted - current_price) / fair_value_per_share_diluted * 100

print(f"\n{'='*100}")
print("5. MARGIN OF SAFETY & RECOMMENDATION")
print(f"{'='*100}")
print(f"  Fair Value per Share:      ${fair_value_per_share_diluted:,.2f}")
print(f"  Current Price:             ${current_price:,.2f}")
print(f"  Premium/(Discount) to FV:  {margin_of_safety:+.1f}%")

if margin_of_safety >= 30:
    rec = "STRONG BUY"
elif margin_of_safety >= 15:
    rec = "BUY"
elif margin_of_safety >= 0:
    rec = "HOLD"
else:
    rec = "SELL / UNDERPERFORM"

print(f"  Recommendation:            {rec}")

print(f"\n{'='*100}")
print("6. SENSITIVITY ANALYSIS")
print(f"{'='*100}")
print("Fair Value Per Share ($) - Varying Discount Rate (r) and Terminal Growth (g)")
print(f"Base case: r=12.0%, terminal g=3.0%  |  Base FCF: ${base_fcf/1e9:.2f}B")
print(f"{'='*100}")

discount_rates_to_test = [0.10, 0.11, 0.12, 0.13, 0.14]
terminal_g_to_test = [0.02, 0.025, 0.03, 0.035, 0.04]

print(f"\n{'r \\ g':<12}", end="")
for tg in terminal_g_to_test:
    print(f"{tg*100:.1f}%{'':<16}", end="")
print()
print("-" * (12 + len(terminal_g_to_test) * 20))

for r in discount_rates_to_test:
    print(f"{f'{r*100:.0f}%':<12}", end="")
    for tg in terminal_g_to_test:
        flows = []
        cf = base_fcf
        for yr in range(1, years + 1):
            g = growth_rates[yr - 1]
            cf *= (1 + g)
            flows.append(cf)
        
        total_pv, _ = dcf_valuation(flows, r)
        tv = terminal_value(flows[-1], tg, r)
        tv_pv = tv / (1 + r) ** years
        ev = total_pv + tv_pv
        eq = ev + net_cash
        fv = eq / diluted_shares
        print(f"${fv:<8.0f}{'':<12}", end="")
    print()

# ============================================================
# SECOND SENSITIVITY: DIFFERENT GROWTH SCENARIOS
# ============================================================

print(f"\n{'='*100}")
print("7. SCENARIO ANALYSIS (Alternate Growth Paths)")
print(f"{'='*100}")

scenarios = {
    "Bull Case (AI super-cycle continues): Growth +20% y1-3, +15% y4-5, +10% y6-7, then taper": 
        [0.20, 0.20, 0.20, 0.15, 0.15, 0.10, 0.10, 0.06, 0.04, 0.03],
    "Base Case (Strong but normalizing):": growth_rates,
    "Bear Case (Cycle turns down): Growth +8% y1-2, +5% y3-5, +3% thereafter":
        [0.08, 0.08, 0.05, 0.05, 0.05, 0.03, 0.03, 0.03, 0.03, 0.03],
    "Severe Bear (NAND glut / recession): Growth -10% y1, flat y2-3, +5% recovery":
        [-0.10, 0.00, 0.00, 0.05, 0.08, 0.08, 0.05, 0.04, 0.03, 0.03],
}

for scenario_name, grates in scenarios.items():
    flows = []
    cf = base_fcf
    for yr in range(1, years + 1):
        g = grates[yr - 1]
        cf *= (1 + g)
        flows.append(cf)
    
    total_pv, _ = dcf_valuation(flows, discount_rate)
    tv = terminal_value(flows[-1], terminal_growth, discount_rate)
    tv_pv = tv / (1 + discount_rate) ** years
    ev = total_pv + tv_pv
    eq = ev + net_cash
    fv = eq / diluted_shares
    mos = (fv - current_price) / fv * 100
    
    print(f"\n{scenario_name}")
    print(f"  Fair Value: ${fv:,.0f}  |  Upside: {mos:+.1f}%")
    last_yr_cf = flows[-1]
    print(f"  Year 10 FCF: ${last_yr_cf/1e9:.2f}B  |  EV/10yr-FCF: {ev/last_yr_cf:.1f}x")

print(f"\n{'='*100}")
print("8. KEY RISKS")
print(f"{'='*100}")
print("""
1. NAND FLASH CYCLICALITY: The memory industry is notoriously cyclical.
   Current peak-cycle metrics (70% op margins, 34% FCF margins) likely
   overstate normalized earnings potential.

2. COMPETITIVE LANDSCAPE: Samsung, Micron, Kioxia, and Chinese YMTC all
   compete aggressively. Oversupply can crash NAND prices rapidly.

3. AI DEMAND SUSTAINABILITY: Current growth is AI-driven. If AI capex
   spending normalizes or disappoints, demand could slow sharply.

4. SPIN-OFF EXECUTION RISK: SanDisk is newly independent from WDC. 
   Operational separation, IT systems, and standalone overhead costs 
   create uncertainty in normalized cost structure.

5. CUSTOMER CONCENTRATION: Large cloud hyperscalers (AWS, Azure, GCP) 
   represent significant portions of enterprise SSD demand.

6. TECHNOLOGY TRANSITIONS: Transition to PLC (penta-level cell), 3D NAND
   scaling limits, and emerging storage class memory technologies.

7. CURRENT VALUATION: At ~$1,916/share, P/E of 63.7x trailing (distorted)
   but forward P/E of 9.4x implies the market expects massive earnings 
   growth that we may be underestimating, or that the cycle will peak 
   and decline.
""")

print(f"{'='*100}")
print("9. COMPARABLE COMPANY ANALYSIS (Cross-Check)")
print(f"{'='*100}")
print("""
                   SNDK      Micron (MU)   Samsung  WDC (HDD+Flash)
  P/E (Fwd):       9.4x      ~12-15x       ~10-12x   ~8-10x
  EV/Revenue:      21.3x     ~5-6x         ~2-3x     ~1.5-2x
  EV/EBITDA:       49.8x     ~8-10x        ~6-8x     ~5-7x
  Rev Growth:      ~251%     ~50-80%       ~10-20%   ~5-15%
  
  SanDisk trades at a significant premium on revenue/EBITDA multiples
  vs peers because of its extraordinary recent growth rate. As growth
  normalizes, multiple compression is likely. This reinforces the need
  for a conservative DCF approach and using a higher discount rate.
""")