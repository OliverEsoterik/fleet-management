# Coherence Checker Methodology

## Purpose

Act as a devil's advocate. Read all three analysis files (technical, market, business) and the idea brief. Identify contradictions, gaps, and weak arguments before they reach the final document. An investor who spots a contradiction in the whitepaper will lose trust in the entire document.

## Process

### Step 1: Read all inputs

Read these files:
- `work/whitepaper/idea-brief.md` — the shared contract
- `work/whitepaper/technical.md` — technical analysis
- `work/whitepaper/market.md` — market research
- `work/whitepaper/business.md` — business model
- `work/whitepaper/research.md` — arXiv and GitHub research (source data for citations)
- `work/whitepaper/market-research.md` — market data research (source data for citations)

### Step 2: Check for contradictions

Contradictions are the most damaging issue. Look for these patterns:

**Timeline contradictions:**
- Technical says "6 months to MVP" but business projects revenue starting in month 3
- Market says "enterprise sales cycle is 6 months" but marketing plan assumes 10,000 customers in year 1

**Number contradictions:**
- Technical says "costs $10/mo to serve each user" but business has 90% gross margin at $50/mo price
- Market says "TAM is $1B" but business projects $500M revenue in year 5 (50% market share — unlikely)

**Assumption contradictions:**
- Technical says "this requires a PhD-level team" but idea brief shows no PhDs on the team
- Market says "customers are price-sensitive" but pricing is premium

**Narrative contradictions:**
- Technical says "we're the only ones doing X" but competitor analysis shows 3 competitors doing X
- Business says "we'll be profitable in year 2" but Monte Carlo shows 30% chance of negative cash flow in year 3

### Step 3: Check for gaps

What's missing that an investor would notice?

- **Missing sections:** Does the template require a section that no analysis covers?
- **Missing evidence:** Claims without supporting data or rationale
- **Missing risks:** Obvious risks that aren't mentioned anywhere
- **Missing team:** No team section in any analysis
- **Missing market evidence:** TAM/SAM/SOM without sources

### Step 4: Check for weak arguments

- **Optimistic assumptions:** "We'll capture 10% market share in year 2" without evidence
- **Circular reasoning:** "We'll be successful because we'll grow fast"
- **Unsupported claims:** "We have a moat" without explaining what creates it
- **Vague language:** "We'll leverage AI" without specifying how
- **Missing trade-offs:** Every design choice has trade-offs — if they're not mentioned, the analysis is incomplete

### Check for uncited claims

Every factual claim in the analysis must have a source reference. Claims without sources are not credible and will be removed from the corrected files in the correction loop.

What counts as a claim that needs a source:
- **Dollar figures:** Any market size, revenue projection, cost estimate, price point
- **Percentages:** Growth rates, margins, churn, market share, conversion rates
- **Projections:** "Will reach X by 2030", "expected to grow at Y%"
- **Comparative statements:** "Faster than X", "cheaper than Y", "better than Z"
- **External facts:** Number of competitors, customer counts, industry statistics

What does NOT need a source:
- **Architecture descriptions:** "The system uses PostgreSQL"
- **Design decisions:** "We chose AWS over GCP because..."
- **Feature lists:** "The product includes X, Y, and Z"
- **Team descriptions:** "The founder has 10 years of experience"
- **Problem statements:** "Companies struggle to manage X"

Verification process:
1. Scan each analysis file for claims (look for $, %, numbers, comparative language)
2. For each claim found, check if it has a `[Source: ...]` reference nearby
3. If the claim has a source, verify the source exists in `research.md` or `market-research.md`
4. If the claim has no source, flag it as "Uncited Claim"
5. If the claim's source cannot be verified against the research files, flag it as "Unverifiable Source"
6. **If the source exists in the research files but does not have a publicly accessible URL (e.g., it is behind a paywall or the URL returns 404/403), flag it as "Unverifiable Source" and do NOT allow it to be added to `references.bib`.**
   A source behind a paywall is not verifiable. Remove the claim from the corrected files.
7. **If a source is added to `references.bib`, verify that the BibTeX entry has a `howpublished = {\url{...}}` field.**
   Any entry without a URL field is invalid and must be removed.

### Step 5: Premortem analysis

Imagine it's 6 months from now and the whitepaper failed to convince investors. What went wrong?

Common failure modes:
- "The technical section was too vague — investors didn't understand why it's hard to build"
- "The market size seemed inflated — they didn't trust the numbers"
- "The financial projections were too optimistic — they assumed 100% of the market"
- "The team section was weak — no domain expertise"
- "The whitepaper contradicted itself — lost credibility"

Work backwards from each failure mode. What would need to be true for that failure to occur? Is that currently the case?

### Step 6: Write recommendations

For each issue found, write a specific fix:
- **Not:** "Improve the financial projections"
- **But:** "Revenue projection assumes 50% market share in year 2. Reduce to 10% (aligned with competitor analysis showing 5 competitors) and adjust the timeline to year 4."

### Step 7: Iterative correction loop — fix until coherent

The coherence report identifies what's wrong. This step fixes it — and verifies the fix — in a loop. The goal is to produce corrected files that contain zero contradictions, gaps, or weak arguments, so the whitepaper writer can write from a clean foundation.

**Setup:**
```bash
mkdir -p work/whitepaper/corrected
cp work/whitepaper/idea-brief.md work/whitepaper/corrected/idea-brief.md
```

**The loop (max 5 iterations to prevent infinite loops):**

For each iteration N (starting at 1):

1. **Read the current files:**
   - Iteration 1: read the originals (`work/whitepaper/technical.md`, `work/whitepaper/market.md`, `work/whitepaper/business.md`)
   - Iterations 2+: read the previously corrected files (`work/whitepaper/corrected/technical.md`, etc.)

2. **Check for issues** — apply the same coherence checking methodology from Steps 2-5 to the current files:
   - Are there contradictions between sections?
   - Are there gaps?
   - Are there weak arguments or unsupported claims?
   - Did the previous iteration's fixes introduce new problems?

3. **If no issues found:** exit the loop. The files are coherent.

4. **If issues found:**
   - Fix every issue directly in the analysis content
   - Write corrected files to `work/whitepaper/corrected/technical.md`, `work/whitepaper/corrected/market.md`, `work/whitepaper/corrected/business.md`
   - Go to iteration N+1

**Writing the convergence summary:**

After the loop ends (either converged or hit max iterations), append a Correction Loop section to the coherence report. Record every iteration and what changed.

**Rules for correcting:**
- Fix the root cause, not the symptom. If revenue projections are optimistic, adjust the numbers and rationale — don't just add a note.
- Preserve the structure and format of the original files. Only change the content that needs fixing.
- If a contradiction exists between two sections, pick the more defensible position and align both sections to it.
- Do NOT include failure-mode labels, diagnostic language, or "this is a risk" commentary in the corrected files.
- Maintain the same level of detail as the original files.
- **Remove uncited claims entirely.** If a claim lacks a `[Source: ...]` reference, delete it from the corrected file. Do not replace it with "we assume" or "we estimate" — remove it. The whitepaper should only contain claims that are supported by verifiable sources.
- **Remove claims whose source cannot be verified against a public URL.** If a source exists in the research files but is behind a paywall or has no publicly accessible URL, the claim must be removed. A source is only valid if it can be fetched and verified by anyone reading the whitepaper.

**Convergence criteria:**
The loop converges when ALL of the following are true:
- Zero contradictions exist between any two corrected files
- Zero gaps remain (all required sections from the idea brief are addressed)
- Zero weak arguments remain (every claim has supporting evidence or rationale)
- Zero uncited claims remain (every factual claim has a `[Source: ...]` reference that can be verified against the research files)
- The corrected files tell one coherent, consistent story

## Output Format

Write to `work/whitepaper/coherence-report.md`:

```markdown
# Coherence Report: [Business Name]

## Summary
- **Contradictions found:** X
- **Gaps found:** X
- **Weak arguments found:** X
- **Uncited claims found:** X
- **Premortem verdict:** [what's most likely to cause failure]

## Contradictions
| # | Issue | Sections involved | Fix |
|---|-------|-------------------|-----|
| 1 | ... | technical.md:12, business.md:45 | ... |

## Gaps
| # | Gap | Why it matters | Fix |
|---|-----|----------------|-----|
| 1 | ... | ... | ... |

## Weak Arguments
| # | Argument | Why it's weak | Fix |
|---|----------|---------------|-----|
| 1 | ... | ... | ... |

## Uncited Claims
| # | Claim | File | Fix |
|---|-------|------|-----|
| 1 | "$30B by 2030" | market.md:15 | Removed — no source found |
| 2 | "40% CAGR" | market.md:22 | Removed — no source found |

## Premortem Analysis
[Failure scenario → root cause → what needs to change]

## Priority Fixes
[Top 3 things that must be fixed before writing the whitepaper]

## Correction Loop
- **Iterations:** N
- **Converged:** Yes / No
- **If No, remaining issues:** [what still needs fixing]
- **Changes per iteration:**
  - Iteration 1: [list of specific fixes applied]
  - Iteration 2: [list of specific fixes applied]
  - ...
```

## Quality Checks

- [ ] Every contradiction is specific (section:line references)
- [ ] Every fix is actionable (not "make it better")
- [ ] Premortem analysis identifies concrete failure modes
- [ ] Issues are prioritized (not everything is equally important)
- [ ] The tone is constructive — the goal is to improve the document, not to criticize the analysis
- [ ] Corrected analysis files are written to `work/whitepaper/corrected/` after the loop converges
- [ ] Corrected files contain no diagnostic language, failure-mode labels, or "this is a risk" commentary
- [ ] The idea brief is copied to `work/whitepaper/corrected/idea-brief.md`
- [ ] The loop converged (or max iterations reached with remaining issues documented)
- [ ] Each iteration's changes are recorded in the convergence summary
- [ ] Uncited claims identified and removed from corrected files
- [ ] Every remaining claim has a `[Source: ...]` reference verifiable against research files