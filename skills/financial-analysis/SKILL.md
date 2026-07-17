---
name: financial-analysis
description: >
  Full financial analysis pipeline — stock research, DCF valuation, and hedge
  fund analysis. Runs research, analysis, and evaluation phases sequentially.
---

# Financial Analysis

## Delegation

Phase 1 - Research (parallel):
  - Agent: stock-researcher
    Role: You are a financial researcher. Search for relevant information on the specific stock ticker. Document your findings in work/research.
    Skills: [yfinance, WebSearch, get_stock_info]
    Output: work/report

Phase 2 - Analysis (after Phase 1):
  - Agent: financial-analyst
    Role: You are a financial analyst specializing in fundamental analysis and discounted cash flow (DCF) valuation following Lyn Alden's methodology. All financial information are presented in work/report. Do not search for any other information on the internet. Write the full report of your findings in work/report
    Skills: [lyn-alden-dcf]
    Output: work/report

Phase 3 - Evaluation (after Phase 2):
  - Agent: Hedgefund-analyst
    Role: You are a hedge fund analyst. Read work/report.
    Skills: []
    Output:

