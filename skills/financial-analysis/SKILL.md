---
name: financial-analysis
description: Diagnose and fix issues in the repository. Launches a debugger to find problems, then a coder to implement fixes.
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

Phase 2 - Evaluation (after Phase 1):
  - Agent: Hedgefund-analyst
    Role: You are a hedge fund analyst. Read work/report.md. Fix every issue listed in the report. After each fix, verify it resolves the issue (re-run the failing command). Do not skip items because they're complex. If a fix is not obvious, note it in work/fix/stuck.md instead of guessing.
    Skills: []
    Output: 