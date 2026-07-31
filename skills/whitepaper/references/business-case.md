# Business Case & Financial Modeling Reference

## Porter's Five Forces Framework

Use this framework to analyze industry attractiveness:

| Force | What to assess | High threat signals | Low threat signals |
|-------|---------------|-------------------|-------------------|
| **Threat of new entrants** | How easy is it to enter this market? | Low capital requirements, no patents, simple technology | High capital requirements, regulatory barriers, patents, economies of scale |
| **Bargaining power of suppliers** | How much leverage do suppliers have? | Few suppliers, unique inputs, high switching costs | Many suppliers, commoditized inputs, low switching costs |
| **Bargaining power of buyers** | How much leverage do customers have? | Few buyers, low switching costs, price-sensitive buyers, commodity product | Many buyers, high switching costs, differentiated product |
| **Threat of substitutes** | What else can customers use instead? | Many alternatives, low switching costs, good performance | Few alternatives, high switching costs, worse performance |
| **Competitive rivalry** | How intense is the competition? | Many competitors, slow growth, undifferentiated products, high exit barriers | Few competitors, fast growth, differentiated products |

## Unit Economics

### Key Metrics

| Metric | Formula | What it tells you |
|--------|---------|-------------------|
| ARPU (Average Revenue Per User) | Total revenue / Total customers | How much each customer is worth per period |
| ARR (Annual Recurring Revenue) | Monthly recurring revenue × 12 | Annualized subscription revenue (SaaS) |
| Gross Margin | (Revenue - COGS) / Revenue | Profitability of each unit sold |
| CAC (Customer Acquisition Cost) | Total sales & marketing / New customers | Cost to acquire one customer |
| LTV (Lifetime Value) | ARPU / Churn rate | Total revenue from one customer over their lifetime |
| LTV/CAC Ratio | LTV / CAC | Efficiency of acquisition (healthy > 3:1) |
| Payback Period | CAC / (ARPU - COGS per customer) | Months to recover acquisition cost |
| Churn Rate | Customers lost / Total customers at start | How fast you're losing customers |

### Cohort Analysis

Track customer behavior by cohort (month they signed up):

```
Cohort  | Size | Mo1 | Mo2 | Mo3 | Mo4 | Mo5 | Mo6
Jan 2024| 100  | 100 | 85  | 72  | 65  | 60  | 58
Feb 2024| 120  | 120 | 102 | 88  | 78  | 72  |
Mar 2024| 110  | 110 | 94  | 80  | 72  |     |
```

This shows whether retention is improving (newer cohorts retain better) or degrading.

## Financial Modeling Best Practices

### Assumption Documentation

Every assumption needs:
1. **The number** — What you're assuming
2. **The rationale** — Why this number, not another
3. **The source** — Where it came from (historical data, industry benchmark, expert opinion)
4. **The range** — Best case / base case / worst case

**Good example:**
```
Revenue growth, Year 1: 150%
Rationale: Pre-seed SaaS startups with product-market fit
typically grow 100-200% in year 1 from a small base.
Source: SaaS Capital 2024 benchmarks for <$1M ARR companies.
Range: 100% (conservative) to 200% (optimistic)
```

### Common Mistakes

| Mistake | Why it's wrong | Fix |
|---------|---------------|-----|
| Linear growth forever | No business grows linearly | Use S-curve: slow start → rapid growth → plateau |
| 100% of market | Impossibly optimistic | Use SOM, not TAM, for projections |
| No working capital | Growing companies need cash for inventory/ receivables | Include working capital changes in cash flow |
| Ignoring churn | Even great companies lose customers | Include churn rate (5-10% monthly for early-stage) |
| Manual calculation errors | Easy to make, hard to spot | Use the Python scripts, not manual spreadsheet |
| Optimistic bias | Everything goes right | Use Monte Carlo to show the range, not just the mean |

## Sensitivity Analysis

### How to Interpret

The sensitivity analysis shows which variables matter most. If 90% of the valuation variance comes from one variable (e.g., revenue growth), the business is highly sensitive to that assumption. This is a risk factor to flag.

### Presentation

Present as a tornado chart (text-based):

```
Variable              Downside (-30%) | Base | Upside (+30%)
Revenue growth       ─────────────────●─────●──────────────
Gross margin         ────────●────────●────●───────────────
Churn rate           ────●────────────●─────●──────────────
CAC                  ──────●──────────●─────●──────────────
```

The longer the bar, the more sensitive the valuation is to that variable.

## Monte Carlo Simulation Interpretation

### How to Explain to Investors

"The Monte Carlo simulation ran 10,000 scenarios, each with randomly sampled assumptions based on our estimated ranges. The results show:

- **Mean outcome:** $X revenue in year 5 (the average across all scenarios)
- **P10-P90 range:** $X to $Y (80% of scenarios fall within this range)
- **VaR (95%):** $X (only 5% of scenarios are worse than this)

This means there's a realistic chance of outcomes between $X and $Y, with the most likely outcome around $Z. The wide range reflects the uncertainty inherent in early-stage projections."

### Common Pitfalls

- **Overconfidence:** Reporting only the mean without the range
- **Wrong distribution:** Using normal distribution for bounded variables (revenue can't be negative)
- **Too few iterations:** Less than 1,000 iterations gives unreliable results. 10,000 is standard.
- **Correlated variables:** Growth and margins are often correlated (high growth companies may have lower margins early on)