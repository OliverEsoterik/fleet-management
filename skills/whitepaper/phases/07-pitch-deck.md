# Pitch Deck Writing Methodology

## Purpose

Produce a Beamer presentation that tells the same story as the whitepaper in 10-15 slides. The pitch deck is a summary — every number must match the whitepaper, and every claim must be supported by the analysis.

## Process

### Step 1: Read all inputs

Read these files:
- `work/whitepaper/idea-brief.md`
- `work/whitepaper/technical.md`
- `work/whitepaper/market.md`
- `work/whitepaper/business.md`
- `work/whitepaper/coherence-report.md`

### Step 2: Apply coherence fixes

Same as the whitepaper — apply fixes from the coherence report before writing.

### Step 3: Design the slide structure

**10-15 slides max.** Investors have short attention spans. Every slide must earn its place.

**Slide structure:**

1. **Title slide** — Company name, tagline, presenter name, date. One sentence that makes the investor want to know more.

2. **Problem** (1 slide) — The pain. Make it visceral. Use a specific example or quantify the cost. "Companies spend $X/year on Y, and it's still broken."

3. **Solution** (1 slide) — What you do, in one clear sentence. A screenshot or mockup if possible. The "aha" moment.

4. **How it works** (1-2 slides) — The technical magic. Not a deep dive — just enough to show it's real and hard to copy. Architecture diagram (simplified).

5. **Market size** (1 slide) — TAM → SAM → SOM. Show the math. Cite the source.

6. **Business model** (1 slide) — How you make money. Unit economics (ARPU, gross margin, LTV/CAC). One simple chart.

7. **Traction / roadmap** (1 slide) — Where you are now and where you're going. Milestones, not activities. "Launched MVP, 3 paying customers, $X revenue."

8. **Competitive landscape** (1 slide) — 2x2 matrix or table. Show you understand the competition and have a clear advantage.

9. **Team** (1 slide) — Key people, their relevant experience, why they're the right team for this. Include advisors.

10. **Financial projections** (1 slide) — Revenue chart (5-year). Key metrics. Monte Carlo range (show the confidence interval).

11. **Ask** (1 slide) — How much, what you'll use it for, what milestones it funds. Be specific.

12. **Thank you** (1 slide) — Contact info, QR code to whitepaper if available.

### Step 4: Write the Beamer source

Create `work/whitepaper/pitch-deck.tex`:

```latex
\documentclass[10pt,aspectratio=169]{beamer}

\usetheme{metropolis}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{amsmath}

\title{[Company Name]}
\subtitle{[Tagline]}
\date{\today}
\author{[Presenter Name]}

\begin{document}

\begin{frame}
\titlepage
\end{frame}

\begin{frame}{The Problem}
\begin{itemize}
    \item Pain point 1
    \item Pain point 2
    \item \$X cost per year
\end{itemize}
\end{frame}

% ... more frames ...

\end{document}
```

**Design rules:**
- Minimal text, maximum signal. One idea per slide.
- Use the `metropolis` Beamer theme (clean, modern, investor-appropriate)
- If `metropolis` is not available, use `default` with minimal customization
- Include speaker notes with `\note{...}` after each frame
- Charts should be simple tables or text-based — no external images
- Every number on every slide must match the whitepaper exactly

### Step 5: Consistency check

Before finishing:
- Every number in the pitch deck: check against the whitepaper analysis files
- Every claim: check against the analysis
- No new information that wasn't in the whitepaper (the pitch deck is a summary, not a separate document)

## Output Format

Write to `work/whitepaper/pitch-deck.tex`.

## Quality Checks

- [ ] 10-15 slides max
- [ ] One idea per slide (if a slide has 3+ bullet points, it needs to be split)
- [ ] Every number matches the whitepaper analysis
- [ ] No new claims not supported by the analysis
- [ ] Speaker notes are included for each slide
- [ ] The `metropolis` theme is used (or a clean alternative)
- [ ] The ask slide is specific (amount, use, milestones)
- [ ] The deck tells a complete story even without the presenter