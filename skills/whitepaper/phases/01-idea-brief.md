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

### Step 3: Determine exit strategy and investor targeting

**Exit strategy:** The primary exit path is acquisition by a strategic corporate buyer. The company is built to be sold, not to be run indefinitely. Document the founder's intent and the types of corporate buyers that would be natural acquirers.

**Investor target group:** The whitepaper targets three groups:
- Corporates (strategic investors who may become acquirers)
- Business angels (especially those with corporate connections)
- Venture capital firms

Investors with corporate connections are particularly valuable — they are offered stakes and a clear path to a corporate exit.

### Step 4: Assess the team

- Founders: who, what background, what domain expertise
- Key hires needed: which roles must be filled to execute
- Gaps: what expertise is missing (critical for investor evaluation)

### Step 5: Determine stage

Default stage is **Idea to Pre-Seed**. If there is working code, it is at most an MVP. The whitepaper validates the idea before significant capital is raised.

| Stage | Characteristics | Whitepaper implications |
|-------|----------------|------------------------|
| Idea | No product, no customers | Focus on problem, solution, market size, team |
| Pre-Seed | Idea validated, some research, no/few users | Problem depth, solution design, team, roadmap, market opportunity |
| MVP | Working product, early users, no/minimal revenue | Traction metrics, early feedback, iteration plan |

### Step 6: Define corporate alignment

How will the company align with corporate partners? This is critical to prove the company is on the right track. Types of alignment:
- **Co-development:** Building the product together with a corporate partner
- **Distribution:** Using a corporate partner's distribution channels
- **Strategic investment:** Corporate partner takes a stake
- **Pilot programs:** Corporate partner runs a pilot before full adoption

Document any existing corporate conversations, letters of intent, or partnership interest.

### Step 7: Define the ecosystem

What ecosystem surrounds the business?
- Platforms the company plugs into or depends on
- Partners, suppliers, and complementary technologies
- Network effects that strengthen as the ecosystem grows
- How the company creates value within or creates an ecosystem

### Step 8: Identify constraints

- Regulatory: FDA, SEC, GDPR, HIPAA, etc.
- Technical: hard technical problems, R&D risk, patent dependency
- Competitive: well-funded competitors, switching costs, network effects
- Timeline: funding runway, regulatory deadlines, market windows
- **Scaling:** Every startup must go to market within 12 months or scale within 36 months, or it is failed. Speed and talent are critical.

### Step 9: Define success criteria

What does "done" mean for this whitepaper? Common criteria:
- Convince an investor to take a meeting
- Serve as a technical reference for due diligence
- Position the company as a thought leader
- Attract strategic partners
- Demonstrate a clear path to corporate acquisition

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

**Key hires needed:** [roles — be specific about what the company needs to hire]
**Critical gaps:** [missing expertise]

## Stage
**Stage:** [Idea / Pre-Seed / MVP]
**Default:** Idea to Pre-Seed. If there is code, at most MVP.
**Evidence:** [what supports this stage classification]

## Exit Strategy
**Primary path:** Corporate acquisition
**Rationale:** [why a corporate buyer would want to acquire this company]
**Founder intent:** [founder's goal — exit into corporate, not indefinite operation]
**Natural acquirers:** [types of corporate buyers]

## Investor Target Group
**Targets:** Corporates, Business Angels, VCs
**Corporate connection value:** Investors with corporate connections are offered stakes and a clear path to corporate exit.

## Corporate Alignment
**Type:** [Co-development / Distribution / Strategic investment / Pilot]
**Existing interest:** [any existing corporate conversations, LOIs, partnership interest]
**Plan:** [how corporate alignment will be built and proven]

## Ecosystem
**Description:** [surrounding ecosystem, platforms, partners, technologies]
**Network effects:** [how the ecosystem strengthens the company's position]

## Scaling Requirements
**Go-to-market timeline:** Within 12 months
**Scale timeline:** Within 36 months or fail
**Critical factors:** Speed, Talent

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
| Scaling | ... | ... |

## Success Criteria
- [ ] [criterion 1]
- [ ] [criterion 2]
```

## Quality Checks

Before submitting, verify:
- [ ] Every section is filled (no blanks)
- [ ] Industry classification is precise and justified
- [ ] Problem statement is quantified where possible
- [ ] Team section includes gaps and key hires needed (honesty builds credibility)
- [ ] Exit strategy is specific (types of corporate buyers, not just "corporate acquisition")
- [ ] Investor target group is clear and justified
- [ ] Corporate alignment has a concrete plan (not just "we'll talk to companies")
- [ ] Ecosystem is defined (platforms, partners, network effects)
- [ ] Scaling requirements are stated (12mo GTM, 36mo scale)
- [ ] Constraints are real and specific (not generic)
- [ ] Success criteria are concrete and verifiable