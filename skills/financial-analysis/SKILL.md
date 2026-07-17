---
name: financial-analysis
description: >
  Multi-methodology financial analysis pipeline — data collection, then
  parallel analysis across DCF (Lyn Alden), value/GARP (Peter Lynch), and
  antifragility critique (Taleb), followed by a consolidated recommendation.
  Each methodology is delegated to a dedicated sub-agent.
---

# Financial Analysis

## Delegation

Phase 1 — Data Collection (parallel):
  - Agent: stock-researcher
    Role: >
      You are a financial researcher. Fetch comprehensive financial data
      for the specified stock ticker and write it to work/research/data.md.
      Use the stock-info skill to gather all data.
    Skills: [stock-info]
    Output: work/research/data.md

Phase 2 — Multi-Methodology Analysis (parallel, after Phase 1):
  - Agent: dcf-analyst
    Role: >
      You are a DCF valuation specialist following Lyn Alden's methodology.
      Read work/research/data.md for all financial data. Do not fetch any
      additional data from the internet. Perform a full DCF valuation:
      project cash flows, compute present values, calculate terminal value,
      determine fair value per share, compare to current price, and
      document margin of safety. Run sensitivity analysis on discount rate
      and growth rate. Write your full analysis to work/analysis/dcf.md.
    Skills: [lyn-alden-dcf]
    Output: work/analysis/dcf.md

  - Agent: value-analyst
    Role: >
      You are a value investing analyst following Peter Lynch's GARP
      (Growth at a Reasonable Price) methodology. Read
      work/research/data.md for all financial data. Do not fetch any
      additional data from the internet. Perform a complete Lynch analysis:
      classify the stock (Slow Grower / Stalwart / Fast Grower / Cyclical /
      Turnaround / Asset Play), compute PEG ratio, check balance sheet
      health, analyze insider activity, assess growth quality, and check
      sell signals. Write your full analysis to work/analysis/lynch.md.
    Skills: [peter-lynch]
    Output: work/analysis/lynch.md

  - Agent: antifragility-analyst
    Role: >
      You are a risk analyst applying Nassim Nicholas Taleb's antifragility
      framework. Read work/research/data.md for all financial data. Do not
      fetch any additional data from the internet. Critique the investment
      thesis: identify hidden fragilities, black swan exposures, asymmetric
      risk/reward, optionality, and Lindy effects. Assess whether the
      company benefits from volatility (antifragile) or is harmed by it
      (fragile). Write your analysis to work/analysis/taleb.md.
    Skills: [nassim-nicholas-taleb]
    Output: work/analysis/taleb.md

Phase 3 — Synthesis (after Phase 2):
  - Agent: synthesis-analyst
    Role: >
      You are a senior portfolio analyst. Read all three analysis files
      (work/analysis/dcf.md, work/analysis/lynch.md,
      work/analysis/taleb.md) and produce a consolidated investment
      recommendation. Compare the methodologies: where do they agree?
      Where do they conflict? Weigh each methodology's findings into a
      final BUY / HOLD / SELL verdict with a specific price target and
      risk assessment. Write the consolidated recommendation to
      work/recommendation.md.
    Skills: []
    Output: work/recommendation.md