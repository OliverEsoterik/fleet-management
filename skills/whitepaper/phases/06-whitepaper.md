# Whitepaper Writing Methodology

## Purpose

Take all analysis files and the coherence report, apply the fixes, and produce a polished LaTeX whitepaper that tells a compelling, consistent story to investors.

## Process

### Step 1: Read all inputs

Read these files:
- `work/whitepaper/corrected/idea-brief.md`
- `work/whitepaper/corrected/technical.md`
- `work/whitepaper/corrected/market.md`
- `work/whitepaper/corrected/business.md`
- `work/whitepaper/research.md` (for bibliography references)
- `work/whitepaper/market-research.md` (for market data sources)
- `work/whitepaper/coherence-report.md` (for awareness — the fixes are already applied)
- `skills/whitepaper/template.tex`

### Step 2: Trust the loop — the corrected files are coherent

The coherence checker ran an iterative correction loop (Step 7 in the methodology) until the corrected files contained zero contradictions, gaps, or weak arguments. The files in `work/whitepaper/corrected/` are verified coherent. Do not re-check or second-guess them — write the whitepaper directly from the corrected files.

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
    - Top risks and mitigations (drawn from the corrected analysis, not from the coherence report's diagnostic language)
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

### Step 6: Create the bibliography from research data

Read `work/whitepaper/research.md` and `work/whitepaper/market-research.md` — they contain citation data for every paper, repository, and market source found during research.

Create `work/whitepaper/references.bib` with BibTeX entries for each source that is actually cited in the whitepaper text.

For arXiv papers (from `research.md`), use the `@misc` entry type with the arXiv ID as the key:
```bibtex
@misc{author2023key,
  author = {Last, First and Last, First},
  title = {Paper Title},
  year = {2023},
  eprint = {2301.12345},
  archivePrefix = {arXiv},
}
```

For GitHub repositories (from `research.md`), use the `@misc` entry type:
```bibtex
@misc{owner-repo,
  author = {Owner or Organization},
  title = {Repository Name},
  year = {2023},
  howpublished = {\url{https://github.com/owner/repo}},
}
```

For market data sources (from `market-research.md`), convert URLs and report names to BibTeX:
```bibtex
@misc{source-key,
  author = {Organization},
  title = {Report Title or Page Title},
  year = {2024},
  howpublished = {\url{https://...}},
}
```

**Citation rules:**
- Every `[Source: ...]` reference in the analysis files must be converted to a `\cite{key}` in the LaTeX
- Every `\cite{key}` must have a corresponding entry in `references.bib`
- Use `\cite{key}` immediately after the claim it supports, e.g.: "The market is projected to reach $30B by 2030\cite{gartner2024}."
- If a `[Source: ...]` reference cannot be matched to a BibTeX entry, flag it in the quality report
- **Every BibTeX entry must have a `howpublished = {\url{...}}` field pointing to the URL where the source was actually found during the research phase.**
  Do NOT add entries for sources that are behind paywalls, that you have not personally verified are publicly accessible, or that you only know about from memory.
  A source is only valid if it has a URL that was fetched and confirmed during the research phase.
- **If a claim in the analysis files references a source that cannot be found with a verifiable public URL, do NOT add it to `references.bib`.**
  Instead, remove the claim from the whitepaper text and flag it in the quality report.
  It is better to remove an unsupported claim than to include a fake or unverifiable citation.

## Output Format

Write to `work/whitepaper/whitepaper.tex` and `work/whitepaper/sections/*.tex`.

## Quality Checks

- [ ] Corrected analysis files are used (not the originals)
- [ ] No diagnostic language, failure-mode labels, or coherence-report jargon appears in the `.tex` output
- [ ] Every section that is included is complete (no empty sections)
- [ ] Cross-references between sections are consistent
- [ ] Numbers match across sections (revenue in financials matches market size in market section)
- [ ] LaTeX compiles without errors (run pdflatex to verify)
- [ ] One sentence per line in `.tex` source
- [ ] All special characters are escaped for LaTeX
- [ ] **Every BibTeX entry has a `howpublished = {\url{...}}` field with a publicly accessible URL**
  If a source does not have a URL that was fetched and verified during research, it must be removed from `references.bib` and the claim removed from the text.