---
name: lyn-alden-dcf
description: Use this skill when performing Discounted Cash Flow (DCF) analysis to value businesses, stocks, projects, or bonds — following Lyn Alden's tutorial methodology
---

# Lyn Alden's Discounted Cash Flow Analysis

## Overview

Use this skill when you need to value an investment (business, stock, project, or bond) using the Discounted Cash Flow (DCF) method as taught by Lyn Alden. The core principle: **an investment now is worth the sum of all future cash flows it will produce, with each discounted to its present value.**

**Announce at start:** "I'm using the lyn-alden-dcf skill to perform discounted cash flow analysis."

---

## Core Formula

```
DCF = CF1/(1+r)^1 + CF2/(1+r)^2 + CF3/(1+r)^3 + ... + CFn/(1+r)^n
```

Where:
- **DCF** = fair value (sum of all future discounted cash flows)
- **CFn** = expected cash flow in year n
- **r** = discount rate (target rate of return, in decimal form)

**Net Present Value (NPV)** = DCF - initial investment

---

## Step-by-Step Process

### Step 1: Define the Discount Rate (r)

The discount rate represents your **target annualized rate of return**. Choice depends on context:

| Context | Typical Discount Rate |
|---------|----------------------|
| Private business (low liquidity) | 15%+ |
| Publicly traded stock | 8-12% (or WACC) |
| Corporate project evaluation | WACC (Weighted-Average Cost of Capital) |
| Bond pricing | Yield to maturity (market interest rate) |

### Step 2: Estimate Future Cash Flows

Break the problem into smaller pieces rather than guessing a single growth rate. For stock valuation, examine:

1. **Revenue growth** — historical volume changes, pricing trends, management guidance
2. **Profit margin changes** — fixed vs variable costs, management margin improvement plans
3. **Share count changes** — buybacks vs dilution
4. **Dividend policy** — payout ratio, growth rate vs EPS growth

For businesses/projects, estimate annual free cash flows explicitly for the forecast period (typically 5-25 years, plus terminal value).

### Step 3: Calculate Present Value of Each Cash Flow

For each year n:
```
PV(CFn) = CFn / (1 + r)^n
```

### Step 4: Sum All Present Values

```
DCF = Σ PV(CFn) for all years n
```

### Step 5: Compare to Current Price

- **Price < DCF** → potentially undervalued (margin of safety)
- **Price > DCF** → potentially overvalued

---

## Examples from Lyn Alden's Tutorial

### Example 1: Private Business Stake

**Scenario:** Buying a 20% stake in a business generating $500K/year FCF (your share: $100K/year), growing at 3%/year. Target return: 15%.

- Year 1 CF: $100,000
- Year 2 CF: $103,000
- Year 3 CF: $106,090
- ...growing at 3% forever

**Result:** DCF = $837,286 (maximum fair price for 15% return)
- First 25 years alone contribute $784,286 — the business doesn't need to last forever

### Example 2: Project Valuation (NPV)

**Scenario:** Company with 9% WACC choosing between two projects, each requiring $3M initial investment.

**Project A:** Growing income stream, then obsolescence.
- Sum of discounted CFs: $9,707,166
- NPV: $6,707,166

**Project B:** No sales for 5 years, then $14M buyout.
- Sum of discounted CFs: $9,099,039
- NPV: $6,099,039

**Decision:** Project A is better — earlier cash flows have higher present value, even though total nominal CF is lower ($12M vs $14M).

### Example 3: Bond Pricing

```
Bond Price = Coupon1/(1+i)^1 + Coupon2/(1+i)^2 + ... + (CouponN + Par)/(1+i)^N
```

- **i** = yield to maturity (target interest rate)
- Higher prevailing interest rates → lower bond prices (and vice versa)

---

## Tools: Python Implementation

When performing DCF analysis, the agent should write and execute a Python script to compute the valuation. A template follows:

```python
def dcf_valuation(cash_flows: list[float], discount_rate: float) -> float:
    """Calculate DCF from a list of annual cash flows and a discount rate."""
    present_values = []
    for year, cf in enumerate(cash_flows, start=1):
        pv = cf / (1 + discount_rate) ** year
        present_values.append(pv)
    return sum(present_values)

def terminal_value(growing_cf: float, growth_rate: float, discount_rate: float, perpetuity: bool = True) -> float:
    """
    Terminal value of a growing perpetuity: CF_next / (r - g)
    growing_cf = last known cash flow
    growth_rate (g) = perpetual growth rate (e.g., 0.03 for 3%)
    discount_rate (r) = target return
    """
    if perpetuity and discount_rate > growth_rate:
        next_cf = growing_cf * (1 + growth_rate)
        return next_cf / (discount_rate - growth_rate)
    return 0.0

def npv(initial_investment: float, cash_flows: list[float], discount_rate: float) -> float:
    """Net Present Value = DCF - initial investment."""
    return dcf_valuation(cash_flows, discount_rate) - initial_investment

def growing_cash_flows(start_cf: float, growth_rate: float, years: int) -> list[float]:
    """Generate a list of growing cash flows."""
    flows = []
    cf = start_cf
    for _ in range(years):
        flows.append(cf)
        cf *= (1 + growth_rate)
    return flows

# --- Gordon Growth Model (single-stage DCF for stable companies) ---
def gordon_growth_model(next_year_fcf: float, growth_rate: float, discount_rate: float) -> float:
    """Fair value = FCF_next / (r - g). Assumes stable perpetual growth."""
    return next_year_fcf / (discount_rate - growth_rate) if discount_rate > growth_rate else float('inf')
```

---

## Limitations & Safeguards

1. **Garbage in, garbage out** — the math is precise but the estimates are educated guesses. Break the growth estimate into volume, pricing, margin, and share count components.
2. **Margin of safety** — only buy at a price well below fair value (e.g., pay $45 for a $50 stock). This protects against estimation errors.
3. **Diversify** — no matter how good the analysis, any single investment can fail. Spread across multiple investments.
4. **Sensitivity analysis** — always test the valuation with different discount rates and growth rates to see how sensitive the result is.

---

## Application Checklist

When the user wants a DCF valuation, follow these steps:

1. Ask for or identify: current free cash flow (or EPS), growth rate estimate, discount rate (target return), number of years to project, terminal growth rate (if any)
2. Generate a table of projected cash flows and their present values
3. Compute total DCF (fair value)
4. For stocks: divide by shares outstanding → fair value per share
5. Compare to current market price
6. Calculate margin of safety %
7. Run sensitivity analysis (vary discount rate ±2%, growth rate ±1%)
8. Present a clear buy/hold/sell recommendation

---

## Key Concepts from the Article

- **DCF vs nominal CF:** A cash flow's present value shrinks each year when discount rate > growth rate. The sum of discounted CFs is finite even if the sum of nominal CFs is infinite.
- **Time preference:** Earlier cash flows are worth more than later ones (same total nominal amount but earlier timing = higher present value).
- **Bond price/interest rate relationship:** When the Fed raises rates, existing bond prices fall; when it cuts rates, existing bond prices rise.
- **StockDelver approach:** Top-down analysis from revenue → margin → EPS/FCF → share count changes → fair value per share.