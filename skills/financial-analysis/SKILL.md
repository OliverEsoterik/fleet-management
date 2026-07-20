---
name: financial-analysis
description: >
  Multi-methodology financial analysis pipeline — data collection, then
  parallel analysis across DCF (Lyn Alden), value/GARP (Peter Lynch), and
  antifragility critique (Taleb), followed by a consolidated recommendation.
  Each methodology is delegated to a dedicated sub-agent.
---

# Financial Analysis

## Graph

Nodes:
  - name: stock-researcher
    trigger: nodes.stock-researcher.status == "ready"
    input: [user_request]
    role: >
      You are a financial researcher. Fetch comprehensive financial data
      for the specified stock ticker and write it to work/research/data.md.
      Use the stock-info skill to gather all data.
    skills: [stock-info]
    output: work/research/data.md
    route: always -> stock-researcher  # mark complete; router launches parallel nodes

  - name: dcf-analyst
    trigger: route("stock-researcher")
    input: [user_request]
    role: >
      You are a DCF valuation specialist following Lyn Alden's methodology.
      Read work/research/data.md for all financial data. Do not fetch any
      additional data from the internet. Perform a full DCF valuation:
      project cash flows, compute present values, calculate terminal value,
      determine fair value per share, compare to current price, and
      document margin of safety. Run sensitivity analysis on discount rate
      and growth rate. Write your full analysis to work/analysis/dcf.md.
    skills: [lyn-alden-dcf]
    output: work/analysis/dcf.md
    route: always -> synthesis-analyst

  - name: value-analyst
    trigger: route("stock-researcher")
    input: [user_request]
    role: >
      You are a value investing analyst following Peter Lynch's GARP
      (Growth at a Reasonable Price) methodology. Read
      work/research/data.md for all financial data. Do not fetch any
      additional data from the internet. Perform a complete Lynch analysis:
      classify the stock (Slow Grower / Stalwart / Fast Grower / Cyclical /
      Turnaround / Asset Play), compute PEG ratio, check balance sheet
      health, analyze insider activity, assess growth quality, and check
      sell signals. Write your full analysis to work/analysis/lynch.md.
    skills: [peter-lynch]
    output: work/analysis/lynch.md
    route: always -> synthesis-analyst

  - name: antifragility-analyst
    trigger: route("stock-researcher")
    input: [user_request]
    role: >
      You are a risk analyst applying Nassim Nicholas Taleb's antifragility
      framework. Read work/research/data.md for all financial data. Do not
      fetch any additional data from the internet. Critique the investment
      thesis: identify hidden fragilities, black swan exposures, asymmetric
      risk/reward, optionality, and Lindy effects. Assess whether the
      company benefits from volatility (antifragile) or is harmed by it
      (fragile). Write your analysis to work/analysis/taleb.md.
    skills: [nassim-nicholas-taleb]
    output: work/analysis/taleb.md
    route: always -> synthesis-analyst

  - name: synthesis-analyst
    trigger: route("dcf-analyst")  # waits for first to complete; all 3 route here so it fires once
    input: [user_request]
    role: >
      You are a senior portfolio analyst. Read all three analysis files
      (work/analysis/dcf.md, work/analysis/lynch.md,
      work/analysis/taleb.md) and produce a consolidated investment
      recommendation. Compare the methodologies: where do they agree?
      Where do they conflict? Weigh each methodology's findings into a
      final BUY / HOLD / SELL verdict with a specific price target and
      risk assessment. Write the consolidated recommendation to
      work/recommendation.md.
    skills: []
    output: work/recommendation.md
    route: always -> consolidator
