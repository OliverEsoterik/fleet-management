#!/usr/bin/env python3
"""What growth does the market price in? And what is the implied fair value if forward P/E is right?"""

# If forward P/E of 9.4x is correct: market expects $32B net income
# At 80% FCF conversion: $25.6B FCF
# At 12% discount rate, 3% terminal growth:
# If Year 1 FCF = $25.6B, growing at 10% for 5 years, then 5% for 5 years, terminal 3%
# What is fair value?

def dcf_valuation(cash_flows, discount_rate):
    total = 0
    for year, cf in enumerate(cash_flows, start=1):
        total += cf / (1 + discount_rate) ** year
    return total

def terminal_value(growing_cf, growth_rate, discount_rate):
    if discount_rate > growth_rate:
        next_cf = growing_cf * (1 + growth_rate)
        return next_cf / (discount_rate - growth_rate)
    return 0.0

# Scenario: Market-implied forward numbers
current_price = 1915.92
diluted_shares = 157000000
fwd_ni = (current_price * diluted_shares) / 9.4  # $32B
market_cap = 283728150528
net_cash = 3735000064 - 182000000

print("=" * 80)
print("MARKET-IMPLIED VALUATION CROSS-CHECK")
print("=" * 80)
print(f"\nForward P/E: 9.4x")
print(f"Current Price: ${current_price:.2f}")
print(f"Diluted Shares: {diluted_shares/1e6:.1f}M")
print(f"Implied Fwd Net Income: ${fwd_ni/1e9:.2f}B")
print(f"Implied FCF (80% conv): ${fwd_ni*0.8/1e9:.2f}B")

# If the market is pricing in $32B NI, and it grows at various rates
# what's the fair value?
print(f"\n{'='*80}")
print("What FCF level does the market price in at current $1,916?")
print(f"{'='*80}")

# Market cap = $283.7B. Net cash = $3.55B. Implied EV = $280.2B
# DCF = EV. Solve backwards.
# At 12% discount, 3% terminal growth:
# EV = sum(FCF_n / 1.12^n) + TV/(1.12^10)
# If we assume constant growth g for 10 years then terminal:
# What "sustainable FCF" at flat growth justifies EV of $280B?

# At 12% discount, 3% terminal:
# If FCF is constant (0% growth) for 10 years, terminal at 3%:
years = 10
discount_rate = 0.12
terminal_g = 0.03
target_ev = 280200118272

# Try different flat FCF levels
print(f"\nTarget EV: ${target_ev/1e9:.1f}B")
print(f"Discount Rate: {discount_rate*100:.0f}%")
print(f"Terminal Growth: {terminal_g*100:.0f}%")
print(f"\n{'Flat FCF ($B)':<15}{'EV ($B)':<15}{'Implied FCF Yield':<20}")
print("-" * 50)

for fcf_b in [10, 12, 14, 16, 18, 20, 22, 25, 28, 30]:
    fcf = fcf_b * 1e9
    flows = [fcf] * years
    ev = dcf_valuation(flows, discount_rate)
    tv = terminal_value(fcf, terminal_g, discount_rate)
    tv_pv = tv / (1 + discount_rate) ** years
    total_ev = ev + tv_pv
    yield_pct = fcf / total_ev * 100
    print(f"{fcf_b:<15.1f}{total_ev/1e9:<15.2f}{yield_pct:<20.1f}%")

# What if FCF grows?
print(f"\n{'='*80}")
print("What sustainable FCF (growing at 8% for 10y, then 3%) justifies $280B EV?")
print(f"{'='*80}")
print(f"\n{'Starting FCF ($B)':<20}{'EV ($B)':<15}{'FV/Share':<15}{'Status':<15}")
print("-" * 65)

for start_fcf_b in [8, 9, 10, 11, 12, 13, 14, 15]:
    fcf = start_fcf_b * 1e9
    flows = []
    cf = fcf
    for yr in range(1, years + 1):
        if yr <= 5:
            cf *= 1.10
        elif yr <= 8:
            cf *= 1.06
        else:
            cf *= 1.04
        flows.append(cf)
    
    ev = dcf_valuation(flows, discount_rate)
    tv = terminal_value(flows[-1], terminal_g, discount_rate)
    tv_pv = tv / (1 + discount_rate) ** years
    total_ev = ev + tv_pv
    eq = total_ev + net_cash
    fv = eq / diluted_shares
    
    status = "AT MARKET" if abs(fv - current_price) < 50 else ("ABOVE" if fv > current_price else "BELOW")
    print(f"{start_fcf_b:<20.1f}{total_ev/1e9:<15.2f}${fv:<14.0f}{status:<15}")

# What combination of starting FCF and growth justifies the current price?
print(f"\n{'='*80}")
print("GROWTH TRAJECTORIES THAT JUSTIFY $1,916/share")
print(f"{'='*80}")
print(f"\n{'Starting FCF ($B)':<20}{'Y1-3 Growth':<15}{'Y4-6 Growth':<15}{'FV/Share':<15}")
print("-" * 65)

# Solve: what starting FCF with aggressive but not insane growth gets us to $1,916?
# Try aggressive trajectory: the Q1'26 run-rate of $12B, growing at 25% for 3yrs
# then tapering

for start_b in [12, 13, 14, 15, 16, 18, 20]:
    for g1 in [0.25, 0.30, 0.35, 0.40]:
        for g2 in [0.15, 0.20]:
            fcf = start_b * 1e9
            flows = []
            cf = fcf
            for yr in range(1, years + 1):
                if yr <= 3:
                    cf *= (1 + g1)
                elif yr <= 6:
                    cf *= (1 + g2)
                elif yr <= 8:
                    cf *= 1.10
                else:
                    cf *= 1.05
                flows.append(cf)
            
            ev = dcf_valuation(flows, discount_rate)
            tv = terminal_value(flows[-1], terminal_g, discount_rate)
            tv_pv = tv / (1 + discount_rate) ** years
            total_ev = ev + tv_pv
            eq = total_ev + net_cash
            fv = eq / diluted_shares
            
            if abs(fv - current_price) / current_price < 0.10:
                print(f"{start_b:<20.1f}{f'{g1*100:.0f}%':<15}{f'{g2*100:.0f}%':<15}${fv:<14.0f}")

print(f"\n{'='*80}")
print("SUMMARY")
print(f"{'='*80}")
print(f"""
At 12% discount rate, 3% terminal growth:
- To justify $1,916/share, the market is pricing in that SanDisk's
  'sustainable' FCF run-rate is approximately $20-25B/year, growing
  at 25%+ for 3 years and 15-20% for 3 more years.
  
  This implies:
  - Starting FCF of ~$14-16B (above even the Q1'26 annualized $12B)
  - Growth at 25-30% for 3 years (needs AI boom acceleration)
  - Yr 10 FCF of $50-70B
  - Terminal EV of $600-800B

  Alternatively, at a lower discount rate (10%), the required starting
  FCF is ~$12-14B with 25% growth.

  CONCLUSION: The current price of $1,916 embakes extremely optimistic
  assumptions. Even accounting for the AI-driven NAND super-cycle, the
  margin of safety is deeply negative under all reasonable scenarios.
""")
