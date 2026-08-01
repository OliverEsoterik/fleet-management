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

## Output Format

Write to `work/whitepaper/coherence-report.md`:

```markdown
# Coherence Report: [Business Name]

## Summary
- **Contradictions found:** X
- **Gaps found:** X
- **Weak arguments found:** X
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

## Premortem Analysis
[Failure scenario → root cause → what needs to change]

## Priority Fixes
[Top 3 things that must be fixed before writing the whitepaper]
```

## Quality Checks

- [ ] Every contradiction is specific (section:line references)
- [ ] Every fix is actionable (not "make it better")
- [ ] Premortem analysis identifies concrete failure modes
- [ ] Issues are prioritized (not everything is equally important)
- [ ] The tone is constructive — the goal is to improve the document, not to criticize the analysis