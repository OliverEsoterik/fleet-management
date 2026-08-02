---
name: whitepaper
description: When you have a business idea and need to create a professional whitepaper with technical deep-dive, business case, and go-to-market strategy — produces a polished PDF and companion pitch deck
skills: []
tools: Read, Write, Bash, Agent
---

# Whitepaper Creation — Graph

## Overview

This skill produces a complete investor-ready whitepaper PDF and companion pitch deck PDF from a raw business idea description.

The whitepaper is built for a specific investment thesis:
- **Exit strategy:** The primary exit path is acquisition by a strategic corporate buyer. The company is built to be sold, not to be run indefinitely.
- **Investor audience:** The whitepaper targets corporates (strategic investors), business angels, and VCs. Investors with corporate connections are particularly valuable — they are offered stakes and a clear path to a corporate exit.
- **Stage focus:** Idea to Pre-Seed. If there is working code, it is at most an MVP. The whitepaper validates the idea before significant capital is raised.
- **Scaling mandate:** Every startup must go to market within 12 months or scale within 36 months, or it is failed. Speed and talent are the two critical success factors.
- **Long-term view:** We look for things that can scale long-term and have the opportunity to make markets, not just enter them.

The pipeline has 10 phases:
1. **idea-decomposer** — Parses the raw idea into a structured brief
2. **technical-researcher** — arXiv and GitHub research to support the technical analysis
3. **technical-analyst** — Deep-dive technical architecture and solution
4. **market-researcher** — Market size, competitors, GTM strategy
5. **business-modeler** — Financial projections, Monte Carlo simulation
6. **coherence-checker** — Flags contradictions across sections
7. **whitepaper-writer** — Produces LaTeX whitepaper
8. **pitch-deck-writer** — Produces Beamer pitch deck
9. **quality-checker** — Applies 10-dimension quality framework
10. **pdf-compiler** — Compiles both documents to PDF

**Outputs:**
- `work/whitepaper/whitepaper.pdf` — final whitepaper
- `work/whitepaper/pitch-deck.pdf` — companion pitch deck
- `work/whitepaper/idea-brief.md` — structured idea brief
- `work/whitepaper/technical.md` — technical analysis
- `work/whitepaper/market.md` — market research
- `work/whitepaper/business.md` — business model
- `work/whitepaper/coherence-report.md` — coherence check
- `work/whitepaper/whitepaper.tex` — LaTeX source
- `work/whitepaper/pitch-deck.tex` — Beamer source
- `work/whitepaper/research.md` — arXiv and GitHub research findings
- `work/whitepaper/market-research.md` — market data, competitor intelligence, and industry reports
- `work/whitepaper/quality-report.md` — quality check

**Announce at start:** "I'm using the whitepaper skill to produce a professional whitepaper for [business idea]."

---

## Graph

### Nodes

  - name: idea-decomposer
    trigger: nodes.idea-decomposer.status == "ready"
    input: [user_request]
    role: >
      You are a business analyst and idea architect. Your job is to take the
      user's raw business idea description and produce a structured "idea
      brief" that every downstream node uses as its shared contract.

      Read the methodology at `skills/whitepaper/phases/01-idea-brief.md`
      and follow it exactly.

      Create the output directory:
      ```bash
      mkdir -p work/whitepaper
      ```

      **Output:** `work/whitepaper/idea-brief.md`

      The idea brief must include:
      - Problem statement (what, who, why now, how bad is the pain)
      - Proposed solution (one-paragraph summary)
      - Target customer segments
      - Industry/sector classification (SaaS, deep tech, biotech, finance, hardware, other)
      - Team overview (founders, key hires needed, gaps)
      - Stage (Idea to Pre-Seed — the default. If there is code, it is at most MVP)
      - Funding requirements (amount, use of funds, valuation expectations)
      - Key constraints (regulatory, technical, competitive, timeline)
      - **Exit strategy** — corporate acquisition plan. The company is built to be acquired by a strategic corporate buyer, not to be run indefinitely.
      - **Investor target group** — corporates, business angels, VCs. Investors with corporate connections are particularly valuable.
      - **Corporate alignment** — how partnerships with corporates will be structured (co-development, distribution, strategic investment).
      - **Ecosystem** — surrounding ecosystem, network effects, platforms the company plugs into or creates.
      - **Scaling requirements** — go-to-market within 12 months, scale within 36 months, or fail. Speed and talent are critical.
      - Success criteria (what "done" looks like for this whitepaper)

      The industry classification is critical — downstream nodes adjust their
      methodology based on it. Be specific and accurate.
    skills: []
    output: work/whitepaper/idea-brief.md
    route: always -> technical-researcher, market-data-researcher, business-modeler

  - name: technical-researcher
    trigger: route("idea-decomposer")
    input: [user_request]
    role: >
      You are a technical research specialist. Read the idea brief from
      `work/whitepaper/idea-brief.md` and search arXiv and GitHub for
      relevant academic papers and open-source implementations to
      support the technical analysis.

      Read the methodology at `skills/whitepaper/phases/02b-research.md`
      and follow it exactly.

      **Output:** `work/whitepaper/research.md`
    skills: []
    output: work/whitepaper/research.md
    route: always -> technical-analyst

  - name: technical-analyst
    trigger: route("technical-researcher")
    input: [user_request]
    role: >
      You are a technical architect. Read the idea brief from
      `work/whitepaper/idea-brief.md` and the research findings from
      `work/whitepaper/research.md`, then produce a deep-dive technical
      analysis that incorporates relevant papers and implementations.

      Read the methodology at `skills/whitepaper/phases/02-technical.md`
      and follow it exactly.

      Also read the reference at
      `skills/whitepaper/references/technical-writeup.md` for best
      practices on structuring technical deep-dives for investors.

      **Output:** `work/whitepaper/technical.md`

      Your analysis must include:
      - System architecture overview (component diagram in ASCII text)
      - Core technical innovation (what's novel, defensible, non-obvious)
      - Why existing solutions fail (specific technical limitations)
      - Problem-to-solution trace (pain → requirement → design decision)
      - Technology stack decisions (each choice with rationale and trade-offs)
      - Technical risks and mitigations
      - Development roadmap (phases, milestones, key technical bets)
      - IP / defensibility (patents, trade secrets, data moats, network effects)
    skills: []
    output: work/whitepaper/technical.md
    route: always -> coherence-checker

  - name: market-data-researcher
    trigger: route("idea-decomposer")
    input: [user_request]
    role: >
      You are a market research specialist. Read the idea brief from
      `work/whitepaper/idea-brief.md` and search the web for market data,
      competitor information, and industry reports to support the market
      analysis.

      Read the methodology at `skills/whitepaper/phases/03b-market-research.md`
      and follow it exactly.

      **Output:** `work/whitepaper/market-research.md`
    skills: []
    output: work/whitepaper/market-research.md
    route: always -> market-researcher

  - name: market-researcher
    trigger: route("market-data-researcher")
    input: [user_request]
    role: >
      You are a market analyst and GTM strategist. Read the idea brief and
      the market research findings, then produce market analysis and
      go-to-market strategy.

      Read the market research at `work/whitepaper/market-research.md` and
      incorporate real market data, competitor intelligence, and industry
      benchmarks into your analysis. Cite sources where possible.

      Read the idea brief from
      `work/whitepaper/idea-brief.md` and produce market research and
      go-to-market strategy.

      Read the methodology at `skills/whitepaper/phases/03-market.md`
      and follow it exactly.

      Also read the reference at
      `skills/whitepaper/references/go-to-market.md` for strategy
      frameworks.

      **Output:** `work/whitepaper/market.md`

      Your analysis must include:
      - TAM / SAM / SOM with calculation logic
      - Competitor landscape (direct, indirect, future)
      - Competitive positioning (moat, differentiation, switching costs)
      - Customer persona(s) and pain points
      - Go-to-market strategy (channels, partnerships, sales model)
      - Customer acquisition strategy (CAC, channels, viral loops)
      - Pricing strategy (model, tiers, benchmarks)
      - Sales strategy (direct, channel, self-serve, enterprise)
      - Marketing plan (content, PR, events, demand gen)
      - Key metrics (LTV, CAC, LTV/CAC, churn, NPS, conversion rates)
    skills: []
    output: work/whitepaper/market.md
    route: always -> coherence-checker

  - name: business-modeler
    trigger: route("idea-decomposer")
    input: [user_request]
    role: >
      You are a financial analyst. Read the idea brief from
      `work/whitepaper/idea-brief.md` and build financial projections and
      Monte Carlo simulations.

      Read the methodology at `skills/whitepaper/phases/04-business.md`
      and follow it exactly.

      Also read the reference at
      `skills/whitepaper/references/business-case.md` for financial
      modeling frameworks.

      Use the Python scripts in `skills/whitepaper/scripts/` for
      calculations:
      ```bash
      python3 skills/whitepaper/scripts/monte_carlo.py
      python3 skills/whitepaper/scripts/financial_model.py
      ```

      **Output:** `work/whitepaper/business.md`

      Your analysis must include:
      - Revenue model (unit economics, revenue streams, pricing)
      - Cost structure (fixed, variable, marginal cost)
      - 5-year financial projections (P&L, cash flow)
      - Key assumptions (each with a written rationale)
      - Break-even analysis
      - Monte Carlo simulation results (10K iterations, mean/median/p10/p90/VaR)
      - Sensitivity analysis (which variables drive value most)
      - Risk register (top 10 risks with impact, probability, mitigation)
    skills: []
    output: work/whitepaper/business.md
    route: always -> coherence-checker

  - name: coherence-checker
    trigger: route("technical-analyst") AND route("market-researcher")
      AND route("business-modeler")
    input: [user_request]
    role: >
      You are a devil's advocate and integration reviewer. Read all three
      analysis files and the idea brief, then produce a coherence report.

      Read the methodology at `skills/whitepaper/phases/05-coherence.md`
      and follow it exactly.

      **Read these files:**
      - `work/whitepaper/idea-brief.md`
      - `work/whitepaper/technical.md`
      - `work/whitepaper/market.md`
      - `work/whitepaper/business.md`
      - `work/whitepaper/research.md` (source data for citation verification)
      - `work/whitepaper/market-research.md` (source data for citation verification)

      **Output:** `work/whitepaper/coherence-report.md`

      After writing the report, enter the iterative correction loop
      (Step 7 in the methodology): fix the issues, write corrected
      files, re-read and check again, repeat until no issues remain.
      The loop converges when the corrected files
      (`work/whitepaper/corrected/technical.md`, etc.) contain zero
      contradictions, gaps, or weak arguments. Max 5 iterations.

      Your report must identify:
      - Contradictions between sections (e.g., tech says 6-month dev
        timeline, business says 3-month revenue)
      - Gaps (missing sections, unaddressed risks, unsupported claims)
      - Weak arguments (claims without evidence, optimistic assumptions)
      - Premortem analysis — if this whitepaper fails to convince
        investors, what went wrong?
      - Recommended fixes for each issue with specific corrections
      - Categorize each issue: Contradiction / Gap / Weak Argument /
        Unsupported Claim
    skills: []
    output: work/whitepaper/coherence-report.md, work/whitepaper/corrected/technical.md, work/whitepaper/corrected/market.md, work/whitepaper/corrected/business.md
    route: always -> whitepaper-writer, pitch-deck-writer

  - name: whitepaper-writer
    trigger: route("coherence-checker")
    input: [user_request]
    role: >
      You are a technical writer. Read all analysis files, the coherence
      report, and the LaTeX template, then produce the whitepaper.

      Read the methodology at `skills/whitepaper/phases/06-whitepaper.md`
      and follow it exactly.

      **Read these files:**
      - `work/whitepaper/corrected/idea-brief.md`
      - `work/whitepaper/corrected/technical.md`
      - `work/whitepaper/corrected/market.md`
      - `work/whitepaper/corrected/business.md`
      - `work/whitepaper/research.md` (for bibliography references)
      - `work/whitepaper/market-research.md` (for market data sources)
      - `work/whitepaper/coherence-report.md` (for awareness — fixes are already applied to the corrected files)
      - `skills/whitepaper/template.tex`

      The coherence report's fixes are already applied to the corrected
      files. Do NOT reproduce failure-mode labels, diagnostic language,
      or "contradiction" / "gap" / "weak argument" terminology from the
      coherence report in the final document. The whitepaper must read as
      a confident, coherent investment case — not as a self-critique.

      Create `work/whitepaper/sections/` with one `.tex` file per section.
      Only include sections relevant to the industry and idea brief.

      **Output:** `work/whitepaper/whitepaper.tex`
    skills: []
    output: work/whitepaper/whitepaper.tex
    route: always -> quality-checker

  - name: pitch-deck-writer
    trigger: route("coherence-checker")
    input: [user_request]
    role: >
      You are a presentation designer. Read all analysis files and the
      coherence report, then produce a Beamer pitch deck.

      Read the methodology at `skills/whitepaper/phases/07-pitch-deck.md`
      and follow it exactly.

      **Read these files:**
      - `work/whitepaper/corrected/idea-brief.md`
      - `work/whitepaper/corrected/technical.md`
      - `work/whitepaper/corrected/market.md`
      - `work/whitepaper/corrected/business.md`
      - `work/whitepaper/research.md` (for bibliography references)
      - `work/whitepaper/market-research.md` (for market data sources)
      - `work/whitepaper/coherence-report.md` (for awareness — fixes are already applied to the corrected files)

      Do NOT reproduce failure-mode labels, diagnostic language, or
      "contradiction" / "gap" / "weak argument" terminology from the
      coherence report in the pitch deck.

      Use the `metropolis` Beamer theme (or similar clean theme). 12-16
      slides max (14 is the sweet spot). One idea per slide. Include speaker notes.

      Every number in the pitch deck must match the whitepaper.

      **Output:** `work/whitepaper/pitch-deck.tex`
    skills: []
    output: work/whitepaper/pitch-deck.tex
    route: always -> quality-checker

  - name: quality-checker
    trigger: route("whitepaper-writer") AND route("pitch-deck-writer")
    input: [user_request]
    role: >
      You are a quality assurance auditor. Read both documents and apply
      the 10 documentation quality dimensions.

      Read the methodology at `skills/whitepaper/phases/08-quality.md`
      and follow it exactly.

      Also read the reference at
      `skills/whitepaper/references/quality-dimensions.md` for the
      full quality framework.

      **Read these files:**
      - `work/whitepaper/whitepaper.tex`
      - `work/whitepaper/pitch-deck.tex`

      **Output:** `work/whitepaper/quality-report.md`

      Score each document on 10 dimensions (Treude et al., 2020):
      Accuracy, Completeness, Consistency, Correctness, Currency,
      Readability, Relevance, Structure, Style, Timeliness.

      For each FAIL or FLAG, provide the specific location (section, line)
      and a concrete fix. Final verdict: PASS / FIX MINOR / BLOCKING ISSUES.
    skills: []
    output: work/whitepaper/quality-report.md
    route: always -> pdf-compiler

  - name: pdf-compiler
    trigger: route("quality-checker")
    input: [user_request]
    role: >
      You are a LaTeX compiler. Read the quality report — if it says
      BLOCKING ISSUES, report the issues and stop. Otherwise, compile
      both documents.

      **Read the quality report:** `work/whitepaper/quality-report.md`

      If verdict is BLOCKING ISSUES, report the issues and stop.

      If verdict is PASS or FIX MINOR, compile both documents:

      ```bash
      cd work/whitepaper
      # Compile whitepaper
      pdflatex -interaction=nonstopmode whitepaper.tex 2>&1 | tail -5
      pdflatex -interaction=nonstopmode whitepaper.tex 2>&1 | tail -5
      # Compile pitch deck
      pdflatex -interaction=nonstopmode pitch-deck.tex 2>&1 | tail -5
      pdflatex -interaction=nonstopmode pitch-deck.tex 2>&1 | tail -5
      ```

      Verify:
      ```bash
      ls -lh work/whitepaper/whitepaper.pdf
      ls -lh work/whitepaper/pitch-deck.pdf
      ```

      If compilation fails, check `report.log` for errors, fix the source
      file, and recompile. Use `grep "^! " report.log` to find errors.

      **Output files:**
      - `work/whitepaper/whitepaper.pdf`
      - `work/whitepaper/pitch-deck.pdf`
    skills: []
    output: work/whitepaper/whitepaper.pdf, work/whitepaper/pitch-deck.pdf
    route: always -> consolidator
