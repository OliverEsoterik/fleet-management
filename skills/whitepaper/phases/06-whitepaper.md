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
| SaaS | Executive summary, problem, solution, business model, corporate alignment, market, competitive, GTM, financials, ecosystem, risk, team | Regulatory, manufacturing |
| Biotech | Executive summary, problem, solution, regulatory pathway, clinical trials, corporate alignment, market, competitive, financials, ecosystem, risk, team | GTM (adapt), manufacturing |
| Deep tech | Executive summary, problem, solution, technical architecture, IP, corporate alignment, market, competitive, financials, ecosystem, risk, team | — |
| Hardware | Executive summary, problem, solution, BOM, supply chain, manufacturing, corporate alignment, market, competitive, financials, ecosystem, risk, team | GTM (adapt) |
| Finance | Executive summary, problem, solution, regulatory, risk modeling, corporate alignment, market, competitive, financials, ecosystem, team | Manufacturing |

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
   - **Answers:** What is the purpose of the company? Why does it exist? What does it do?

2. **Problem Statement** (1-2 pages)
   - The pain: who, what, how bad, how much it costs
   - Why existing solutions don't work
   - Is this a real problem that really needs a solution? (validate the problem depth)
   - Why now (technology maturity, market shifts, regulatory changes)
   - **Answers:** What problem is it solving? Is it a real problem that really needs a solution? Why now?

3. **Technical Solution** (3-6 pages)
   - Architecture overview
   - Core innovation
   - Why it's hard to replicate
   - Development roadmap
   - Technical risks and mitigations
   - **MVP definition** (not prototype — a working product that delivers core value to early users)
   - **Answers:** What is the solution? What does the MVP look like?

4. **Business Model** (1-2 pages)
   - Revenue model and unit economics
   - Cost structure
   - Key metrics
   - **Answers:** What is the business model? How does it make money?

5. **Corporate Alignment & Partnership Strategy** (1-2 pages)
   - How corporate partnerships are structured (co-development, distribution, strategic investment)
   - Why corporate alignment proves the company is on the right track
   - Exit strategy: the company is built with a clear path to acquisition by a strategic corporate buyer
   - Existing corporate interest, LOIs, or pilot programs
   - **Answers:** How will corporate alignment look? Why is this the right track?

6. **Market Analysis** (2-3 pages)
   - TAM/SAM/SOM
   - Customer persona
   - Market trends
   - **Answers:** What is the addressable market?

7. **Competitive Landscape** (2-3 pages)
   - Competitor analysis
   - Positioning and differentiation
   - Moat analysis
   - **Answers:** What is the competition? Why is this solution significantly better?

8. **Go-to-Market Strategy** (2-3 pages)
   - Channels and sales model
   - Customer acquisition
   - Pricing
   - Marketing plan
   - Scaling timeline: go-to-market within 12 months
   - **Answers:** What is the go-to-market strategy?

9. **Financial Projections & Capital Roadmap** (2-3 pages)
   - 5-year P&L summary
   - Monte Carlo results (chart/table)
   - Sensitivity analysis
   - Break-even analysis
   - Funding plan and use of funds
   - Capital roadmap: what milestones each funding round unlocks, how capital maps to scaling
   - **Answers:** What should the roadmap in capital look like?

10. **Ecosystem** (1-2 pages)
    - Surrounding ecosystem: platforms, partners, complementary technologies
    - Network effects and ecosystem dynamics
    - How the company creates value within or creates an ecosystem
    - Long-term scalability: how the ecosystem grows with the company
    - **Answers:** What is the ecosystem?

11. **Risk Analysis** (1-2 pages)
    - Top risks and mitigations
    - Premortem findings
    - Talent risk: how the company will attract and retain the talent needed
    - Product-market fit risk: how PMF will be validated

12. **Team** (1 page)
    - Founders and key team members
    - Advisors
    - Key hires needed (specific roles the company requires to build this)
    - **Answers:** What is the team? What roles do we need to hire?

13. **Appendix** (optional)
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