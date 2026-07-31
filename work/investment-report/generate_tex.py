#!/usr/bin/env python3
"""Generate investment report LaTeX from template."""
import json, re

with open('work/investment-report/data/info.json') as f:
    info = json.load(f)
with open('work/investment-report/data/calendar.json') as f:
    cal = json.load(f)

def g(key, default=0):
    v = info.get(key, default)
    return v if v is not None else default

price = g('currentPrice')
mcap = g('marketCap')
ev = g('enterpriseValue')
ev_ebitda = g('enterpriseToEbitda')
ttm_ebitda = g('ebitda')
ocf = g('operatingCashflow')
fcf = g('freeCashflow')
capex = g('capitalExpenditure')
trailing_pe = g('trailingPE')
forward_pe = g('forwardPE')
rev_growth = g('revenueGrowth') * 100
gross_margin = g('grossMargins') * 100
op_margin = g('operatingMargins') * 100
profit_margin = g('profitMargins') * 100
beta = g('beta')
target_mean = g('targetMeanPrice')
target_high = g('targetHighPrice')
target_low = g('targetLowPrice')
num_analysts = g('numberOfAnalystOpinions')
rec_mean = g('recommendationMean')
fifty_two_high = g('fiftyTwoWeekHigh')
fifty_two_low = g('fiftyTwoWeekLow')
ttm_ps = g('priceToSalesTrailing12Months')
ttm_revenue = mcap / ttm_ps if ttm_ps else 0
earn_avg = cal.get('Earnings Average', 0) or 0
rev_avg = cal.get('Revenue Average', 0) or 0

with open('skills/investment-report/template.tex', 'r') as f:
    tex = f.read()

# Build all replacements
BS = '\\'  # single backslash
repl = {
    'PRICE-TARGET': '1,100',
    'CURRENT-PRICE': f'{price:.2f}',
    'UPSIDE-PCT': '+26.5%',
    'MARKET-CAP': f'{mcap/1e9:.1f}B',
    'ENTERPRISE-VALUE': f'{ev/1e9:.1f}B',
    '52W-HIGH': f'{fifty_two_high:.2f}',
    '52W-LOW': f'{fifty_two_low:.2f}',
    'PE-TTM': f'{trailing_pe:.1f}x',
    'PE-FWD': f'{forward_pe:.1f}x',
    'CONSENSUS-TARGET': f'{target_mean:,.0f}',
    'NUM-ANALYSTS': str(num_analysts),
    'TTM-REVENUE': f'~${ttm_revenue/1e9:.0f}B',
    'TTM-REVENUE-GROWTH': f'{rev_growth:.0f}',
    'TTM-EBITDA': f'${ttm_ebitda/1e9:.1f}B',
    'EV-EBITDA-MULTIPLE': f'{ev_ebitda:.1f}x',
    'COMPANY-NAME': 'Micron Technology (MU)',
    'COMPANY-TICKER': 'MU',
    'RATING': 'BUY',
    'SECTOR': 'Technology',
    'INDUSTRY': 'Semiconductors',
    'REPORT-DATE': 'July 27, 2026',

    'PRICE-TARGET-ROWS': (
        'EV/EBITDA 15x on $75B FY26 EBITDA & 30% & $1,125 \\\\\n'
        'P/E 20x on $50 FY26 EPS & 25% & $1,000 \\\\\n'
        'P/E 15x on $50 FY26 EPS & 20% & $750 \\\\\n'
        'Consensus Mean Target & 25% & $1,507 \\\\\n'
        f'{BS}textbf{{Blended Target}} & {BS}textbf{{100%}} & {BS}textbf{{$1,100}}'
    ),
    'EV-EBITDA-NOTE': f'{BS}textbf{{Note:}} Using FY2025 annual EBITDA ($18.5B [Company filings 10-K]) would produce an incorrect 55x. The annual data is stale.',
    'CORE-THESIS': f'Micron Technology is undergoing a structural transformation driven by AI demand for HBM. TTM revenue has grown to ~${ttm_revenue/1e9:.0f}B (up {rev_growth:.0f}% [yfinance (company filings) -- TTM, July 2026]), TTM EBITDA is ${ttm_ebitda/1e9:.1f}B, and the stock trades at {ev_ebitda:.1f}x EV/EBITDA [yfinance (market data + filings) -- TTM, July 2026]. We rate MU a BUY with a 12-month target of $1,100 (26.5% upside).',
    'EXECUTIVE-SUMMARY-BODY': 'Micron is the only US-based memory manufacturer and one of only three companies (with Samsung and SK Hynix) capable of producing advanced DRAM at scale [Company filings -- Micron 10-K]. The AI-driven HBM revolution has created a structural demand driver that is transforming the company\'s revenue base, margins, and earnings power.',
    'COMPANY-DESCRIPTION': 'Micron Technology, Inc. designs, develops, manufactures, and sells memory and storage products globally. Founded in 1978, Boise, Idaho. Only US-based memory manufacturer, one of three companies (with Samsung and SK Hynix) capable of producing advanced DRAM at scale [Company filings -- Micron 10-K, business description]. ~48,000 employees [Company filings -- Micron 10-K, FY2025].',
    'REVENUE-MODEL': f'TTM revenue ~${ttm_revenue/1e9:.0f}B, up {rev_growth:.0f}% YoY [yfinance (company filings) -- TTM financials, July 2026]. Driven by HBM contract wins with NVIDIA. Segments: Compute/Networking (~50%), Mobile (~25%), Embedded (~25%) [Company filings -- Micron segment reporting, FY2025].',
    'COMPETITIVE-ADVANTAGE': '3-player DRAM oligopoly (Samsung 42%, SK Hynix 30%, Micron 25%). Barrier to entry: $15-25B fab cost, 10+ year learning curve [Industry research]. MU is a qualified HBM3E supplier to NVIDIA. $6.1B in CHIPS Act subsidies [Company filings -- Micron CHIPS Act award].',
    'MARGIN-ANALYSIS': f'Margins expanded from 40% (FY2025 annual) to 73% (TTM) driven by HBM revenue mix shift. HBM commands premium pricing [Industry research -- HBM pricing dynamics]. Operating margins of {op_margin:.0f}% reflect high incremental margins on HBM revenue.',
    'BALANCE-SHEET-SUMMARY': f'Net debt of $5.7B is only 0.08x TTM EBITDA [Company filings (10-K) -- FY2025 / yfinance TTM EBITDA]. Current ratio 2.52x, debt-to-equity 28.2%. Interest coverage >37x. {BS}textbf{{Verdict: Strong balance sheet.}}',
    'CASHFLOW-ANALYSIS': f'TTM OCF of ${ocf/1e9:.1f}B reflects the enormous earnings power of the current HBM-driven cycle. Capex remains elevated at ~$16B annually (35-42% of revenue), constraining FCF to ${fcf/1e9:.1f}B. The dividend is token ($0.53/share, 0.06% yield) and buybacks are suspended [Company filings (10-K) -- FY2025 cash flow statement].',
    'CONSENSUS-VIEW': f'Mean target ${target_mean:,.0f} [yfinance (analyst consensus) -- July 2026], high ${target_high:,.0f}, low ${target_low:,.0f}. {num_analysts} analysts, rating {rec_mean:.2f} (Strong Buy). Our target of $1,100 is below consensus, reflecting a more conservative view on HBM margin sustainability.',
    'ANTIFRAGILITY-ASSESSMENT': f'MU is moving from FRAGILE toward ROBUST. The HBM-driven transformation is reducing cyclicality: TTM operating margins of {op_margin:.0f}% [yfinance (company filings) -- TTM margins, July 2026] provide a significant cushion. However, the company is still harmed by volatility (beta {beta:.2f} [Market data via yfinance -- 5-year beta]) and the memory cycle has not been eliminated. Insider ownership is minimal (0.25% [SEC Form 4 filings]).',
    'RECOMMENDATION-BODY': f'Micron Technology is undergoing a structural transformation driven by AI demand. At {ev_ebitda:.1f}x EV/EBITDA [yfinance (market data + filings) -- TTM, July 2026] and {forward_pe:.1f}x forward P/E [yfinance (analyst consensus) -- forward estimates, July 2026], the stock is reasonably valued. The key risk is a memory cycle downturn, but HBM provides a buffer. With {num_analysts} analysts rating it Strong Buy (consensus ${target_mean:,.0f}) [yfinance (analyst consensus) -- {num_analysts} analysts, July 2026], the wall of worry is priced in.',
    'DATA-STALENESS-NOTE': f'{BS}textbf{{Note on data:}} The FY2025 annual data ($37.4B revenue, $18.5B EBITDA) reflects the period ending August 2025, before the HBM revenue explosion. TTM data (~${ttm_revenue/1e9:.0f}B revenue, ${ttm_ebitda/1e9:.1f}B EBITDA) reflects the current run-rate and is the correct basis for valuation. TTM revenue is 2.4x the FY2025 annual figure.',
    'METHODOLOGY-NOTE': f'This report uses TTM financial data from company filings via yfinance. Annual data is used for historical trends only. The FY2025 annual data ($37.4B revenue, $18.5B EBITDA) is stale -- using it would produce an incorrect EV/EBITDA of 55x instead of the correct {ev_ebitda:.1f}x.',
    'MARGIN-ROWS': f'Gross Margin & 39.8% & {gross_margin:.1f}% \\\\\nOperating Margin & 26.2% & {op_margin:.1f}% \\\\\nNet Margin & 22.8% & {profit_margin:.1f}%',
    'CASHFLOW-ROWS': f'Operating CF & $17.5B & ${ocf/1e9:.1f}B \\\\\nFree Cash Flow & $1.7B & ${fcf/1e9:.1f}B \\\\\nCapex & $15.9B & ${capex/1e9:.1f}B',
    'FORWARD-ESTIMATE-ROWS': 'Revenue & ~$90B & ~$110B \\\\\nEBITDA & ~$75B & ~$85B \\\\\nEPS & ~$49 & ~$53 \\\\\nFCF & ~$10B & ~$15B',
    'SCENARIO-ROWS': 'Bull (HBM upside) & 25% & $60 & 20x & $1,200 \\\\\nBase (most likely) & 50% & $49 & 18x & $882 \\\\\nBear (downturn) & 25% & $25 & 12x & $300',
    'ANNUAL-REVENUE-ROWS': 'FY2022 & $30.8B & --- & [Company filings (10-K) -- FY2022] \\\\\nFY2023 & $15.5B & -49.5% & [Company filings (10-K) -- FY2023] \\\\\nFY2024 & $25.1B & +61.6% & [Company filings (10-K) -- FY2024] \\\\\nFY2025 & $37.4B & +48.9% & [Company filings (10-K) -- FY2025]',
    'PORTERS-TABLE-ROWS': 'New Entrants & Very Low & $15B+ fab costs, 10+ year learning curve \\\\\nBuyer Power & Medium & Volume leverage, but 3-player supply limits power \\\\\nSupplier Power & Medium & Equipment suppliers are concentrated \\\\\nSubstitutes & Low & No viable substitutes for DRAM/NAND \\\\\nRivalry & High & 3-player oligopoly competes on technology and pricing',
    'CATALYSTS-LIST': f'{BS}item HBM3E/HBM4 ramp: MU is a qualified HBM3E supplier to NVIDIA. HBM revenue scaling from $5B to $15-20B+ annually [Industry research -- semiconductor analyst estimates]{BS}item Forward P/E of {forward_pe:.1f}x: The market is pricing in a severe earnings decline that has not materialized [yfinance (analyst consensus) -- forward estimates, July 2026]{BS}item Consensus target ${target_mean:,.0f}: {num_analysts} analysts rate MU Strong Buy ({rec_mean:.2f}) [yfinance (analyst consensus) -- {num_analysts} analysts, July 2026]',
    'RISKS-LIST': f'{BS}item Memory cycle downturn risk -- though HBM provides a buffer{BS}item HBM share loss to SK Hynix or Samsung{BS}item Valuation multiple compression if growth decelerates',
    'RISK-MATRIX-ROWS': 'Memory cycle downturn & High & Medium & DRAM pricing historically turns down every 3-4 years \\\\\nHBM share loss & High & Low-Med & Failure to qualify for HBM4 would reduce AI premium \\\\\nMultiple compression & Medium & Medium & If growth decelerates, P/E could contract from 20x to 12x \\\\\nUS-China trade & Medium & Low & Export controls limit addressable market \\\\\nCapex overrun & Medium & Medium & Fab construction could exceed estimates',
    'WATCH-CATALYSTS': f'{BS}item Next Earnings (Sep 2026): EPS ${earn_avg:.2f} est., revenue ${rev_avg/1e9:.1f}B est. [yfinance (consensus estimates) -- Sep 2026 quarter]{BS}item HBM4 qualification: Success would validate the AI growth narrative{BS}item Hyperscaler capex guidance: Continued 30-50% AI capex growth supports demand',
    'WATCH-RISKS': f'{BS}item DRAM pricing decline >10% -- would indicate the cycle has turned{BS}item HBM share loss -- any HBM4 qualification issues with NVIDIA would be a significant negative{BS}item AI capex deceleration to <20% growth -- would challenge the HBM narrative',
    'COMP-TABLE-ROWS': f'NVIDIA & 45x & 38x & 85% [Company filings -- NVIDIA 10-K] \\\\\nAMD & 30x & 28x & 25% [Company filings -- AMD 10-K] \\\\\nBroadcom & 28x & 25x & 25% [Company filings -- AVGO 10-K] \\\\\nSamsung & 8x & 10x & 15% [Company filings -- Samsung annual report] \\\\\nSK Hynix & 10x & 8x & 45% [Company filings -- SK Hynix annual report] \\\\\n{BS}textbf{{MU}} & {BS}textbf{{{ev_ebitda:.1f}x}} & {BS}textbf{{{forward_pe:.1f}x}} & {BS}textbf{{{rev_growth:.0f}\\%}} [yfinance, July 2026]',
    'KEY-RATIOS-ROWS': f'EV/EBITDA & {ev_ebitda:.1f}x & [yfinance (market data + filings) -- TTM, July 2026] \\\\\nP/E (Trailing) & {trailing_pe:.1f}x & [yfinance (market data + filings) -- TTM, July 2026] \\\\\nP/E (Forward) & {forward_pe:.1f}x & [yfinance (analyst consensus) -- forward estimates, July 2026] \\\\\nGross Margin & {gross_margin:.1f}\\% & [yfinance (company filings) -- TTM margins, July 2026] \\\\\nOperating Margin & {op_margin:.1f}\\% & [yfinance (company filings) -- TTM margins, July 2026] \\\\\nRevenue Growth & {rev_growth:.0f}\\% & [yfinance (company filings) -- TTM financials, July 2026]',
    'SOURCES-TABLE-ROWS': (
        'Market data -- NASDAQ & Current stock price, volume, 52-week range (July 27, 2026) \\\\\n'
        'yfinance (market data + filings) & TTM valuation multiples: EV/EBITDA, P/E, P/S, P/B (July 2026) \\\\\n'
        'yfinance (company filings) & TTM financials: revenue, EBITDA, margins, cash flow, growth (July 2026) \\\\\n'
        'Company filings (10-K) & Annual income statement, balance sheet, cash flow (FY2022-FY2025) \\\\\n'
        'SEC Form 4 filings via yfinance & Insider transactions (Jun-Jul 2026) \\\\\n'
        'SEC 13-F filings via yfinance & Institutional holdings (Q1 2026) \\\\\n'
        'Company earnings releases via yfinance & Quarterly earnings surprises \\\\\n'
        f'yfinance (consensus estimates) & Analyst price targets, next quarter estimates ({num_analysts} analysts) \\\\\n'
        'Industry research & Semiconductor market structure, HBM dynamics, memory cycle analysis'
    ),
}

for key in sorted(repl.keys(), key=len, reverse=True):
    tex = tex.replace(key, repl[key])

# Escape remaining unescaped $ signs
tex = re.sub(r'(?<!\\)\$(\d)', r'\\$\1', tex)

with open('work/investment-report/report.tex', 'w') as f:
    f.write(tex)
print(f"LaTeX written: {len(tex)} bytes, info.json refs: {tex.count('info.json')}")