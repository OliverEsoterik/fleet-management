# Idea Brief Methodology

## Purpose

Take the user's raw business idea description and produce a structured "idea brief" that serves as the shared contract for all downstream nodes. Every downstream node reads this brief — its quality determines the quality of the entire whitepaper.

## Process

### Step 1: Parse the user request

Read the user's description carefully. Extract:

1. **Problem statement** — What is the problem? Who has it? Why now? How bad is the pain? Quantify if possible (e.g., "$X billion lost annually", "Y hours wasted per week").

2. **Proposed solution** — One-paragraph summary of what the business does. Clear enough that someone unfamiliar with the domain understands it.

3. **Target customers** — Who pays? B2B, B2C, marketplace? What's the decision-maker profile?

### Step 2: Classify the industry

This is critical — downstream nodes adjust their methodology based on industry. Be specific and accurate.

| Industry | Characteristics | Whitepaper emphasis |
|----------|----------------|---------------------|
| SaaS | Recurring revenue, cloud, subscription | Unit economics, churn, CAC, LTV, growth metrics |
| Deep tech | Hardware, AI, robotics, novel science | Technical architecture, IP, regulatory pathway, R&D timeline |
| Biotech | Therapeutics, diagnostics, medical devices | Clinical trial pathway, regulatory (FDA), patent landscape, reimbursement |
| Finance | Fintech, payments, lending, insurance | Regulatory compliance, risk modeling, network effects, partnership strategy |
| Hardware | Physical product, manufacturing, supply chain | BOM, supply chain, manufacturing timeline, unit economics at scale |
| Marketplace | Two-sided platform, network effects | Liquidity strategy, chicken-and-egg problem, take rate, network effects |
| Consumer | B2C app, direct-to-consumer | CAC, viral loops, retention, unit economics, brand strategy |
| Enterprise | B2B software, professional services | Sales cycle, deal size, channel strategy, implementation complexity |

If the idea spans multiple industries, choose the primary one based on where the most technical complexity lies.

### Step 3: Assess the team

- Founders: who, what background, what domain expertise
- Key hires needed: which roles must be filled to execute
- Gaps: what expertise is missing (critical for investor evaluation)

### Step 4: Determine stage

| Stage | Characteristics | Whitepaper implications |
|-------|----------------|------------------------|
| Idea | No product, no customers | Focus on problem, solution, market size, team |
| Prototype | Working prototype, no revenue | Technical validation, early user feedback |
| MVP | Live product, early users | Traction metrics, early revenue, iteration plan |
| Revenue | Paying customers, growing | Financials, growth metrics, scaling plan |
| Growth | Scale-stage, significant revenue | Expansion strategy, competitive defense, moat |

### Step 5: Identify constraints

- Regulatory: FDA, SEC, GDPR, HIPAA, etc.
- Technical: hard technical problems, R&D risk, patent dependency
- Competitive: well-funded competitors, switching costs, network effects
- Timeline: funding runway, regulatory deadlines, market windows

### Step 6: Define success criteria

What does "done" mean for this whitepaper? Common criteria:
- Convince an investor to take a meeting
- Serve as a technical reference for due diligence
- Position the company as a thought leader
- Attract strategic partners

## Output Format

Write the idea brief to `work/whitepaper/idea-brief.md` using this template:

```markdown
# Idea Brief: [Business Name]

## Problem
[Problem statement — who, what, why now, how bad]

## Solution
[One-paragraph summary]

## Target Customers
[Who pays, who decides, how many]

## Industry Classification
**Primary:** [SaaS / Deep Tech / Biotech / Finance / Hardware / Marketplace / Consumer / Enterprise]
**Secondary:** [if applicable]
**Rationale:** [why this classification]

## Team
| Role | Name | Background |
|------|------|------------|
| Founder | ... | ... |
| ... | ... | ... |

**Key hires needed:** [roles]
**Critical gaps:** [missing expertise]

## Stage
**Stage:** [Idea / Prototype / MVP / Revenue / Growth]
**Evidence:** [what supports this stage classification]

## Funding
**Amount seeking:** $X
**Use of funds:** [bullet list]
**Valuation expectations:** [if known]

## Constraints
| Type | Constraint | Impact |
|------|-----------|--------|
| Regulatory | ... | ... |
| Technical | ... | ... |
| Competitive | ... | ... |
| Timeline | ... | ... |

## Success Criteria
- [ ] [criterion 1]
- [ ] [criterion 2]
```

## Quality Checks

Before submitting, verify:
- [ ] Every section is filled (no blanks)
- [ ] Industry classification is precise and justified
- [ ] Problem statement is quantified where possible
- [ ] Team section includes gaps (honesty builds credibility)
- [ ] Constraints are real and specific (not generic)
- [ ] Success criteria are concrete and verifiable