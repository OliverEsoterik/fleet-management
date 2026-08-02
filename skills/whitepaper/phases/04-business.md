# Business Modeling Methodology

## Purpose

Build financial projections and risk analysis that demonstrate:
1. **The business makes economic sense** (unit economics work)
2. **The projections are grounded** (assumptions are justified)
3. **The risks are understood** (Monte Carlo, sensitivity analysis)

## Process

### Step 1: Read the idea brief and research data

Read `work/whitepaper/idea-brief.md` to understand the industry, stage, funding needs, and constraints.

Read `work/whitepaper/market-research.md` for industry benchmarks (margins, CAC, churn, etc.) that ground your financial projections.

### Cite every claim

Every financial assumption in your analysis must include a source reference. Use the format `[Source: Name, URL]`.

**Examples:**
- "Gross margin for SaaS is 75% [Source: OpenView Benchmarks 2024, https://...]"
- "Median CAC for enterprise SaaS is $50K [Source: KeyBanc SaaS Survey 2024, https://...]"
- "Annual churn for mid-market SaaS is 10% [Source: Pacific Crest SaaS Survey, https://...]"

If you cannot find a source in the market research file, do not make the claim. The coherence checker will remove any uncited claims from the corrected files.

### Step 2: Revenue model

Define how the business makes money:

- **Revenue streams:** List all sources (subscription, usage-based, one-time, services, etc.)
- **Unit economics per stream:** Price per unit, units per customer, frequency
- **Revenue drivers:** What needs to happen for revenue to grow? (more customers, higher prices, more usage)
- **Cohort behavior:** How does revenue per customer evolve over time? (expansion, contraction, churn)

### Step 3: Cost structure

- **Fixed costs:** Rent, salaries, software, insurance, etc.
- **Variable costs:** Cloud hosting, payment processing, COGS, customer support per user
- **Marginal cost per unit:** What does it cost to serve one more customer?
- **Scaling behavior:** Which costs are fixed, which scale linearly, which have economies of scale?

### Step 4: 5-year financial projections

Use the `financial_model.py` script:

```bash
echo '{
  "starting_revenue": <current or projected year-1 revenue>,
  "revenue_growth_rates": [0.XX, 0.XX, 0.XX, 0.XX, 0.XX],
  "cogs_percent": [0.XX, 0.XX, 0.XX, 0.XX, 0.XX],
  "op_ex_pct": [0.XX, 0.XX, 0.XX, 0.XX, 0.XX],
  "tax_rate": 0.25,
  "capex_percent": 0.05,
  "dnb_percent": 0.03,
  "working_capital_pct": 0.10,
  "debt": 0,
  "interest_rate": 0.05,
  "shares_outstanding": 10000000
}' | python3 skills/whitepaper/scripts/financial_model.py > work/whitepaper/financial-projections.json
```

**IMPORTANT: Every assumption must have a written rationale.** Do not just input numbers — explain why 50% growth in year 1, why 30% OPEX, why 70% gross margin. Investors will challenge every assumption.

### Step 5: Break-even analysis

Calculate:
- **Break-even revenue:** Fixed costs / contribution margin
- **Break-even customers:** Break-even revenue / ARPU
- **Break-even month:** When cumulative FCF turns positive
- **Cash runway:** How long existing funds last at current burn rate

### Step 6: Monte Carlo simulation

Use the `monte_carlo.py` script:

```bash
echo '{
  "revenue_growth": {"mean": 0.XX, "std": 0.XX},
  "gross_margin": {"mean": 0.XX, "std": 0.XX},
  "operating_margin": {"mean": 0.XX, "std": 0.XX},
  "churn_rate": {"mean": 0.XX, "std": 0.XX},
  "cac": {"mean": XXX, "std": XXX},
  "initial_revenue": <current revenue>,
  "projection_years": 5,
  "cost_structure": {"fixed": XXX, "variable_pct": 0.XX}
}' | python3 skills/whitepaper/scripts/monte_carlo.py > work/whitepaper/monte-carlo-results.json
```

Read the results and explain:
- **Mean:** The expected outcome
- **P10–P90 range:** The range of likely outcomes (80% confidence)
- **VaR at 95%:** The worst-case scenario (only 5% of outcomes are worse)
- **What drives the variance:** Which assumptions have the biggest impact on the spread?

### Step 7: Sensitivity analysis

Identify the 3-5 variables that have the most impact on valuation/profitability:

| Variable | Base case | Downside | Upside | Impact on valuation |
|----------|-----------|----------|--------|---------------------|
| Revenue growth | 30% | 15% | 50% | ±40% |
| Gross margin | 70% | 55% | 80% | ±25% |
| Churn rate | 5%/mo | 8%/mo | 3%/mo | ±30% |

### Step 8: Risk register

Top 10 risks, each with:

| # | Risk | Category | Probability | Impact | Mitigation | Owner |
|---|------|----------|------------|--------|------------|-------|
| 1 | Competitor launches similar product | Competitive | Medium | High | Patent filing, first-mover advantage, customer lock-in | CEO |
| 2 | Key engineer leaves | Team | Low | High | Equity vesting, documentation, hiring pipeline | CTO |
| ... | ... | ... | ... | ... | ... | ... |

## Output Format

Write to `work/whitepaper/business.md`:

```markdown
# Business Model & Financial Projections: [Business Name]

## Revenue Model
[Revenue streams, unit economics, drivers]

## Cost Structure
[Fixed, variable, marginal cost, scaling behavior]

## 5-Year Financial Projections
[Summary table from financial_model.py + assumption rationales]

## Break-Even Analysis
[Revenue, customers, timeline]

## Monte Carlo Simulation
[Results from monte_carlo.py + interpretation]

## Sensitivity Analysis
[Key drivers and their impact]

## Risk Register
[Top 10 risks with mitigations]
```

## Quality Checks

- [ ] Every financial assumption has a written rationale
- [ ] Monte Carlo results are interpreted (not just printed)
- [ ] Sensitivity analysis identifies the 3-5 key drivers
- [ ] Break-even analysis is realistic for the stage
- [ ] Risk register has specific mitigations, not "we'll manage it"
- [ ] Projections are internally consistent (revenue growth → headcount → costs)
- [ ] The projections tell a story that matches the technical and market sections