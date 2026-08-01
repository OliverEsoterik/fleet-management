# Whitepaper Writing Methodology

## Purpose

Take all analysis files and the coherence report, apply the fixes, and produce a polished LaTeX whitepaper that tells a compelling, consistent story to investors.

## Process

### Step 1: Read all inputs

Read these files:
- `work/whitepaper/idea-brief.md`
- `work/whitepaper/technical.md`
- `work/whitepaper/market.md`
- `work/whitepaper/business.md`
- `work/whitepaper/coherence-report.md`
- `skills/whitepaper/template.tex`

### Step 2: Apply coherence fixes

Before writing anything, go through the coherence report's fixes and apply them to the analysis. The whitepaper should reflect the corrected analysis, not the original errors.

### Step 3: Select relevant sections

Read the template.tex to see which sections are available. Choose only the sections relevant to the industry and idea brief:

| Industry | Include | Skip |
|----------|---------|------|
| SaaS | Executive summary, problem, solution, business model, market, competitive, GTM, financials, risk, team | Regulatory, manufacturing |
| Biotech | Executive summary, problem, solution, regulatory pathway, clinical trials, market, competitive, financials, risk, team | GTM (adapt), manufacturing |
| Deep tech | Executive summary, problem, solution, technical architecture, IP, market, competitive, financials, risk, team | — |
| Hardware | Executive summary, problem, solution, BOM, supply chain, manufacturing, market, competitive, financials, risk, team | GTM (adapt) |
| Finance | Executive summary, problem, solution, regulatory, risk modeling, market, competitive, financials, team | Manufacturing |

### Step 4: Write each section

Create `work/whitepaper/sections/` directory. Write one `.tex` file per section.

**LaTeX rules (follow these exactly):**
- One sentence per line in the `.tex` source (clean diffs, easier debugging)
- Use `\section{}`, `\subsection{}`, `\subsubsection{}` for headings
- Use `\label{sec:name}` and `\ref{sec:name}` for cross-references
- Use `\textbf{}` for emphasis, `\emph{}` for italic
- Use `\begin{itemize}` for bullet lists
- Use `\begin{tabularx}{\textwidth}{lXX}` for tables (with `\toprule`, `\midrule`, `\bottomrule` from booktabs)
- Escape special characters: `$` → `\$`, `%` → `\%`, `&` → `\&`, `_` → `\_`, `#` → `\#`
- Use `\textit{...}` for source citations
- Use `\cite{key}` for bibliography references
- Use `\href{url}{text}` for links

**Section structure (industry-standard whitepaper):**

1. **Executive Summary** (1-2 pages)
   - The problem in one sentence
   - The solution in one sentence
   - Why now (market timing)
   - Key metrics (TAM, revenue projection, team)
   - The ask (funding needed)
   - The reader should understand the entire opportunity from this section alone

2. **Problem Statement** (1-2 pages)
   - The pain: who, what, how bad, how much it costs
   - Why existing solutions don't work
   - Why now (technology maturity, market shifts, regulatory changes)

3. **Technical Solution** (3-6 pages)
   - Architecture overview
   - Core innovation
   - Why it's hard to replicate
   - Development roadmap
   - Technical risks and mitigations

4. **Business Model** (1-2 pages)
   - Revenue model and unit economics
   - Cost structure
   - Key metrics

5. **Market Analysis** (2-3 pages)
   - TAM/SAM/SOM
   - Customer persona
   - Market trends

6. **Competitive Landscape** (2-3 pages)
   - Competitor analysis
   - Positioning
   - Moat analysis

7. **Go-to-Market Strategy** (2-3 pages)
   - Channels and sales model
   - Customer acquisition
   - Pricing
   - Marketing plan

8. **Financial Projections** (2-3 pages)
   - 5-year P&L summary
   - Monte Carlo results (chart/table)
   - Sensitivity analysis
   - Break-even analysis
   - Funding plan and use of funds

9. **Risk Analysis** (1-2 pages)
   - Top risks and mitigations
   - Premortem findings

10. **Team** (1 page)
    - Founders and key team members
    - Advisors
    - Key hires needed

11. **Appendix** (optional)
    - Detailed financials
    - Technical specifications
    - Market research methodology

### Step 5: Create the main file

Write `work/whitepaper/whitepaper.tex` that sets the metadata and includes all sections:

```latex
\input{settings.tex}
\renewcommand{\whitepaperTitle}{[Your Title]}
\renewcommand{\companyName}{[Your Company]}
\renewcommand{\docDate}{\today}

\begin{document}
\input{sections/01-executive-summary.tex}
\input{sections/02-problem-statement.tex}
...
\end{document}
```

### Step 6: Add a bibliography

If the whitepaper cites external sources, create `work/whitepaper/references.bib`.

## Output Format

Write to `work/whitepaper/whitepaper.tex` and `work/whitepaper/sections/*.tex`.

## Quality Checks

- [ ] All coherence report fixes have been applied
- [ ] Every section that is included is complete (no empty sections)
- [ ] Cross-references between sections are consistent
- [ ] Numbers match across sections (revenue in financials matches market size in market section)
- [ ] LaTeX compiles without errors (run pdflatex to verify)
- [ ] One sentence per line in `.tex` source
- [ ] All special characters are escaped for LaTeX