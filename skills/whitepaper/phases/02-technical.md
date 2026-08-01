# Technical Analysis Methodology

## Purpose

Produce a deep-dive technical analysis that convinces an investor the solution is:
1. **Real** — it can be built (feasibility)
2. **Hard** — it's defensible (moat)
3. **Right** — it solves the actual problem (fit)

## Process

### Step 1: Read the idea brief

Read `work/whitepaper/idea-brief.md`. Understand the problem, solution, industry, and constraints.

### Step 2: System architecture

Draw a component diagram in ASCII text showing:
- The user/client facing components
- The core processing/backend components
- External integrations/dependencies
- Data flow between components

Example:
```
┌──────────┐     ┌──────────┐     ┌──────────────┐
│  Client   │────▶│  API     │────▶│  Core Engine  │
│  (Web/App)│     │  Gateway │     │  (Processing) │
└──────────┘     └──────────┘     └──────┬───────┘
                                         │
                                  ┌──────▼───────┐
                                  │  Database     │
                                  │  (Postgres)   │
                                  └──────────────┘
```

### Step 3: Core technical innovation

What makes this technically novel or defensible? Be specific:
- **Novel algorithm** — what does it do that others can't?
- **Architecture pattern** — why is this approach better?
- **Data advantage** — does the system get better with more data?
- **Hardware/software co-design** — custom hardware, optimized stack
- **Integration moat** — deep integration with customer workflows

For each claim, explain WHY it's hard to replicate. Not "it uses AI" but "the model is trained on a proprietary dataset that takes 3 years to collect and requires domain expertise to label."

### Step 4: Why existing solutions fail

For each major competitor/alternative, identify a specific technical limitation:
- "Solution X uses rule-based approach, which fails on edge cases Y and Z"
- "Solution Y requires manual data entry, creating a bottleneck at scale"
- "Solution Z has a monolithic architecture, making it impossible to customize for enterprise clients"

Map each limitation to a specific design decision in your proposed solution.

### Step 5: Problem-to-solution trace

For each aspect of the problem, trace through to the architecture:

```
User pain: "Takes 40 hours/week to manually reconcile invoices"
  → Requirement: "Automated reconciliation with >99% accuracy"
    → Design decision: "ML pipeline with transformer-based matching"
      → Why this approach: "Outperforms regex-based approaches on ambiguous matches"
```

This trace is the most important part of the technical section. It shows the investor that every design decision is grounded in a real problem.

### Step 6: Technology stack

For each major technology choice, provide:
- **What** (name of technology)
- **Why** (rationale — why this one over alternatives)
- **Trade-off** (what you gave up by choosing it)

| Component | Choice | Rationale | Trade-off |
|-----------|--------|-----------|-----------|
| Database | PostgreSQL | Strong consistency, complex queries, ecosystem | Higher ops overhead than SQLite |
| ML framework | PyTorch | Research flexibility, community, deployment tools | Steeper learning curve than TensorFlow |
| Cloud | AWS | Lambda, SageMaker, market share | Higher cost than GCP for same compute |

### Step 7: Technical risks

For each risk, provide:
- **Risk** — what could go wrong
- **Probability** — Low/Medium/High
- **Impact** — what happens if it materializes
- **Mitigation** — what you're doing to prevent or recover from it

| Risk | Probability | Impact | Mitigation |
|------|-----------|--------|------------|
| Model accuracy below threshold | Medium | Delayed launch | Iterative validation with customers from month 1 |
| Scaling bottleneck at 10x load | Low | Performance degradation | Load testing from MVP, horizontal scaling architecture |

### Step 8: Development roadmap

Phases with milestones:

| Phase | Timeline | Milestone | Key technical bet |
|-------|----------|-----------|-------------------|
| Phase 1 | Months 1-3 | Prototype with core feature | Prove model accuracy >90% |
| Phase 2 | Months 4-6 | MVP with 3 customers | Validate scaling with real data |
| Phase 3 | Months 7-12 | Production launch | Automate deployment pipeline |

### Step 9: IP and defensibility

How does the technology get more valuable over time?
- **Data network effects** — more users → more data → better product
- **Switching costs** — deep integration with customer workflows
- **Patents** — what's patentable, what's filed
- **Trade secrets** — what's kept proprietary
- **Brand/trust** — regulatory approvals, certifications

## Output Format

Write to `work/whitepaper/technical.md`:

```markdown
# Technical Analysis: [Business Name]

## Architecture Overview
[ASCII diagram + description]

## Core Innovation
[What's novel and why it's defensible]

## Why Existing Solutions Fail
[Competitor → limitation → our design decision]

## Problem-to-Solution Trace
[Pain → requirement → design → why]

## Technology Stack
[Table with choices, rationales, trade-offs]

## Technical Risks
[Table with risks, probabilities, mitigations]

## Development Roadmap
[Phased timeline with milestones]

## IP & Defensibility
[Data moats, switching costs, patents, trade secrets]
```

## Quality Checks

- [ ] Architecture diagram is clear to a non-technical reader
- [ ] Every technical claim has a "why" and a "trade-off"
- [ ] Existing solutions are analyzed, not dismissed
- [ ] Risks are specific and have mitigations (not "we'll figure it out")
- [ ] Roadmap is realistic for the team size and stage
- [ ] Defensibility claims are specific (not "we have a moat")