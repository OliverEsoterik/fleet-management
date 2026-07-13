---
name: peter-lynch
description: >
  Applies Peter Lynch's GARP (Growth at a Reasonable Price) methodology to
  analyze and classify stocks, determine fair valuation, assess balance sheet
  health, evaluate insider activity, and generate a buy/hold/sell recommendation.
---

# Peter Lynch Investment Strategy

## Overview

Use this skill when you need to analyze a stock using Peter Lynch's investment methodology. Lynch managed the Fidelity Magellan Fund from 1977 to 1990, achieving a 29.2% annualized return (2,700% cumulative) and outperforming the S&P 500 in 11 of 13 years.

**Core philosophy:** Invest in what you know. Stock prices follow earnings over the long term. Ignore macro forecasts and focus on individual companies. A stock must have both a **story** (qualitative thesis you can explain in 2 minutes) and a **number** (valuation supported by fundamentals).

**Announce at start:** "I'm using the peter-lynch skill to analyze [ticker]."

---

## The Process

The analysis follows 7 sequential steps. Each step writes an output file under `work/peter-lynch/`. The final step synthesizes everything into a recommendation.

---

### Step 1: Stock Classification

Classify the stock into one of Peter Lynch's six categories. **Each category has different valuation rules, expected returns, and sell criteria.** Getting this wrong means applying the wrong framework.

| Category | Growth Rate | Examples | Key Metric | Expected Return |
|----------|------------|----------|------------|-----------------|
| **Slow Grower** | 2-4% | Utilities, P&G, Coca-Cola | Dividend yield consistency | 3-6% annually |
| **Stalwart** | 10-12% | McDonald's, PepsiCo | PEG ~1.0 | 10-15% annually |
| **Fast Grower** | 20-25%+ | Dunkin' Donuts (early), Walmart (early) | PEG < 1.0, low debt | 20-30%+ annually |
| **Cyclical** | Variable | Ford, Caterpillar, airlines | Inventory-to-sales, capacity | 50-100% in upswing |
| **Turnaround** | N/A | Chrysler (1982), Apple (1997) | Debt structure, cash burn | 100-500% if successful |
| **Asset Play** | N/A | Real estate / holding cos | Net asset value vs market cap | Variable |

**How to classify:**
1. Fetch earnings growth rate using `get_stock_info` — look at 1yr, 3yr, 5yr EPS CAGR
2. Check revenue growth consistency — is growth steady or volatile?
3. Check industry context — is the company tied to economic cycles?
4. Check for distress signals — is the company losing money but has assets/cash?

**Critical rules:**
- "A high-growth company in a high-growth industry is the most dangerous type of stock." Fast Growers in boring industries (Dunkin' Donuts in food, Walmart in retail) are safer because competition is less intense.
- Cyclicals look like bargains at the wrong time: P/E is highest at the cycle bottom (earnings depressed) and lowest at the peak (earnings bloated). Do not buy cyclicals based on low P/E alone.
- Turnarounds are "the most predictable of all stock categories" — a company with $2/share cash and zero debt has limited downside.

**Output:** `work/peter-lynch/classification.md`

---

### Step 2: PEG Ratio Analysis and Valuation

The PEG ratio is Lynch's signature metric. It relates price to both earnings and growth.

**Formula:**
```
PEG = (Current P/E Ratio) / (Earnings Growth Rate %)
```

**Interpretation:**

| PEG Range | Signal |
|-----------|--------|
| < 0.5 | Strong buy — "screaming bargain" |
| 0.5 - 1.0 | Undervalued — good buying opportunity |
| 1.0 - 1.5 | Fairly valued |
| 1.5 - 2.0 | Overvalued — caution |
| > 2.0 | Overvalued — avoid or sell |

**Refinements:**
- **Slow Growers and Stalwarts:** Use adjusted PEG = P/E / (Growth Rate + Dividend Yield). Dividends are part of the total return.
- **Cyclicals and Turnarounds:** PEG is not useful. Use other metrics.
- **Forward vs Trailing:** Lynch used both. Prefer forward PEG for valuation, trailing PEG for checking consistency.
- **Industry context:** Compare PEG to industry median, not just absolute threshold.

**Lynch's rule of thumb:** A stock's P/E ratio should equal its growth rate + dividend yield. If P/E < growth rate, the stock is a bargain.

**How to compute:**
1. Use `get_stock_info` to get current P/E ratio
2. Calculate earnings growth rate (1yr, 3yr, 5yr CAGR from EPS data)
3. Compute PEG = P/E / growth rate
4. For dividend-paying stocks, compute adjusted PEG = P/E / (growth rate + dividend yield)
5. Compare to industry median PEG
6. Determine if the stock is undervalued, fairly valued, or overvalued

**Output:** `work/peter-lynch/valuation.md`

---

### Step 3: Balance Sheet Health Check

Lynch cared deeply about financial strength. A great growth story means nothing if the company is drowning in debt.

**Key metrics to check:**

| Metric | Lynch's Rule | What It Means |
|--------|-------------|---------------|
| **Net Cash per Share** | Cash - Long-term debt > 0 | Downside protection; net cash adds to intrinsic value |
| **Debt-to-Equity** | < 0.3 (ideally 0) | Low debt = flexibility. **Exclude financials** (banks/S&Ls) from this rule |
| **Current Ratio** | > 1.5 | Can pay short-term obligations |
| **Inventory-to-Sales Trend** | Inventory growth <= Sales growth | Rising inventory faster than sales = trouble brewing |
| **Free Cash Flow** | Positive and growing | Real earnings quality check — earnings should convert to cash |
| **Dividend Payout Ratio** | 25-50% for dividend payers | Sustainable dividend; > 80% is risky (may be cut) |

**How to analyze:**
1. Use `get_stock_info` to fetch balance sheet and cash flow data
2. Calculate each metric above
3. Flag any metric that violates Lynch's rule
4. For inventory: compare trend over 3+ years, not just current quarter
5. Determine overall balance sheet health: **Strong** (all green), **Adequate** (1-2 flags), **Weak** (3+ flags)

**Output:** `work/peter-lynch/balance-sheet.md`

---

### Step 4: Insider Activity Analysis

Lynch saw insider buying as one of the strongest signals available to individual investors.

**Rules:**
- **Bullish signal:** 3+ executives/directors buying shares on the open market within 90 days
- **Neutral:** Insider selling is normal (diversification, tax planning). Not a sell signal by itself.
- **Bearish signal:** Heavy, sustained insider selling by multiple executives without explanation
- **Strongest signal:** Insiders buying after a significant price drop

**How to analyze:**
1. Use `academic_search` or web search to find recent insider transactions
2. Count distinct insiders who bought/sold in the last 90 days
3. Note the dollar amounts — $1M+ insider buying is significant
4. Distinguish between open-market purchases (signal) and option exercises (not a signal)
5. Assess: strong buying, moderate buying, neutral, or selling pressure

**Output:** `work/peter-lynch/insider-activity.md`

---

### Step 5: Growth Rate Analysis

Lynch looked at growth from multiple angles to assess quality and sustainability.

**Metrics to analyze:**

1. **Historical EPS Growth (3yr and 5yr CAGR):** Consistent growth is better than erratic growth
2. **Revenue Growth:** Must support EPS growth — if EPS grows but revenue doesn't, the growth may come from cost-cutting or financial engineering
3. **Earnings Quality:** Did growth come from operations or one-time items? Exclude non-recurring gains
4. **Sustainable Growth Rate:** ROE × (1 - Dividend Payout Ratio). Shows how fast the company can grow without issuing new equity or taking on debt
5. **Growth vs Industry:** Is the company gaining or losing market share?

**How to analyze:**
1. Use `get_stock_info` to get EPS history, revenue history, ROE, payout ratio
2. Calculate the metrics above
3. Determine growth quality: **Strong** (consistent 15%+ EPS growth, revenue-supported), **Moderate** (10-15%, some one-time items), **Weak** (erratic or declining)

**Output:** `work/peter-lynch/growth-rate.md`

---

### Step 6: Sell Signal Framework

Lynch had specific sell rules for each category. Checking these helps decide whether to hold or exit.

| Category | Key Sell Signals |
|----------|------------------|
| **Slow Grower** | Stock up 30-50% past fair value; dividend cut; market share lost for 2+ years |
| **Stalwart** | P/E exceeds growth rate by 2x; new products failing; stock 30-50% ahead of fundamentals |
| **Fast Grower** | Growth deceleration (EPS growth < 15-20%); same-store sales decline 2 quarters; debt increasing; heavy insider selling |
| **Cyclical** | Inventory buildup; capacity expansion announcements; weakening end-market demand; P/E compressing while earnings rise (paradoxical sell signal) |
| **Turnaround** | Debt restructuring fails; turnaround completes (time to exit and find the next one) |
| **Asset Play** | Spin-off completed; institutional ownership rising (catalyst triggered) |

**General sell signals that apply across categories:**
- The "story" changes — you can no longer explain the thesis in 2 minutes
- P/E has expanded far beyond the growth rate (multiple expansion without fundamental justification)
- Insiders are selling heavily and consistently
- The company acquires unrelated businesses (Lynch called this "di-worse-ification")
- Inventory growing faster than sales for 2+ quarters

**How to analyze:**
1. Re-read the classification from Step 1
2. Check current valuation against the signals for that category
3. Check general sell signals
4. Count how many signals are triggered: 0-1 = Hold, 2-3 = Caution, 4+ = Sell

**Output:** `work/peter-lynch/sell-signals.md`

---

### Step 7: Final Recommendation

Synthesize all previous analyses into a clear recommendation.

**Weight the factors:**
- PEG valuation is the most important quantitative factor
- Balance sheet health is the risk gate — weak balance sheet overrides good valuation
- Insider activity is the confirmation signal
- Sell signals determine whether existing positions should be held

**Recommendation template:**

```markdown
## Recommendation for [TICKER]

**Classification:** [Category]
**Verdict:** [BUY / HOLD / SELL]

### Supporting Evidence
- **Valuation (PEG):** [PEG value] — [undervalued/fair/overvalued]
- **Balance Sheet:** [Strong/Adequate/Weak] — [key strength/concern]
- **Insider Activity:** [Strong buying / Neutral / Selling]
- **Growth Quality:** [Strong/Moderate/Weak] — [growth rate and sustainability]
- **Sell Signals:** [X of Y triggered] — [key signals]

### Price Target
- **Fair value based on PEG:** [price]
- **Current price:** [price]
- **Margin of safety:** [%]

### Risk Factors
- [Key risk 1]
- [Key risk 2]

### Catalysts
- [Catalyst 1 — what could drive the stock higher]
```

**Output:** `work/peter-lynch/recommendation.md`

---

## Application Checklist

When the user asks to analyze a stock using Peter Lynch methodology:

1. **Confirm the ticker** and optionally the specific task
2. **Announce** the skill being used
3. **Execute sequentially** through Steps 1-7
4. **Use tools** — `get_stock_info` for financial data, `academic_search` for supplementary research (industry context, insider activity)
5. **Write outputs** to `work/peter-lynch/` for each step
6. **Present the final recommendation** with supporting evidence from all prior steps

---

## Key References

- Lynch, P. & Rothchild, J. (1989). *One Up On Wall Street*. Simon & Schuster.
- Lynch, P. & Rothchild, J. (1993). *Beating the Street*. Simon & Schuster.
- Lynch, P. & Rothchild, J. (1995). *Learn to Earn*. Simon & Schuster.
- Lakonishok, Shleifer & Vishny (1994). "Contrarian Investment, Extrapolation, and Risk." *Journal of Finance*.
- Piotroski, J.D. (2000). "Value Investing: The Use of Historical Financial Statement Information." *Journal of Accounting Research*.

---

## Limitations

1. **PEG is backward-looking** — historical growth may not predict future growth. Use forward estimates when available.
2. **"Buy what you know" can cause overconfidence** — familiarity with a product is not the same as understanding the business.
3. **The strategy was developed in a unique market environment** (falling rates, 1982-1990 bull market). Modern conditions differ.
4. **High turnover** — Lynch's strategy requires active monitoring. It is not a "set and forget" approach.
5. **Scale dependent** — Lynch's approach works best for individual investors; large funds cannot replicate his flexibility.
