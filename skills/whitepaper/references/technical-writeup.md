# Technical Write-up Best Practices

## How to Structure a Technical Deep-Dive for Investors

Investors reading a technical section are looking for three things:
1. **Feasibility** — Can this be built?
2. **Defensibility** — Can it be protected from competitors?
3. **Fit** — Does it actually solve the problem?

### Architecture Diagrams

Use ASCII diagrams for component architecture. Keep them simple — 3-7 boxes max.

**Good example:**
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

**Bad example (too complex):**
```
[LOAD BALANCER] → [API GATEWAY] → [AUTH SERVICE] → [MESSAGE QUEUE]
  → [WORKER POOL] → [CACHE LAYER] → [DB CLUSTER] → [DATA WAREHOUSE]
  → [ML PIPELINE] → [FEATURE STORE] → [MODEL SERVING] → [MONITORING]
```

### Explaining Technical Defensibility

**Weak:** "We have a moat because of our technology."
**Better:** "Our model is trained on a proprietary dataset of 10,000 annotated samples that took 3 years to collect."
**Best:** "Our model is trained on a proprietary dataset of 10,000 annotated samples that took 3 years to collect. Each sample requires a domain expert with 5+ years of experience to label. This gives us a 3-year head start, and anyone replicating it would need to invest $2M+ in data collection."

**Types of defensibility (ranked by durability):**

1. **Data network effects** — More users → more data → better product → more users. Hardest to replicate.
2. **Switching costs** — Deep integration into customer workflows. Takes effort to leave.
3. **Regulatory moats** — FDA approval, banking licenses, compliance certifications.
4. **Technical complexity** — Hard to build, but once built, can be copied.
5. **Brand** — Takes time to build, but not technical.

### Common Pitfalls

| Pitfall | Example | Fix |
|---------|---------|-----|
| Over-explaining | 3 pages on database indexing | One paragraph on why you chose PostgreSQL |
| Under-explaining | "We use AI" | Specify the model architecture, training data, accuracy metrics |
| Jargon without definition | "We use a transformer-based encoder with attention" | "We use a transformer model (like GPT but specialized for our data) that..." |
| No trade-offs | "We chose React" | "We chose React over Vue because of the larger ecosystem and hiring pool, at the cost of a heavier bundle size" |
| Unrealistic timelines | "6 months to full launch" | Show the phased roadmap with dependencies |

### The Problem-to-Solution Trace

The most powerful technique in technical writing for investors. For each aspect of the problem, trace through:

```
[User pain] → [Requirement] → [Design decision] → [Why this approach]
```

Example:
```
Pain: "Takes 40 hrs/week to manually reconcile invoices"
  → Requirement: "Automated matching with >99% accuracy"
    → Decision: "Transformer-based matching pipeline"
      → Why: "Outperforms regex on ambiguous matches (92% vs 67%)"
```

This shows the investor that every design decision is grounded in a real problem, not just technology for its own sake.

### Technical Risks

**Weak:** "We might have scaling issues."
**Better:** "At 10x current load, the database will become the bottleneck. We'll mitigate this by sharding before we reach 5x load."

Every risk should have:
- **Specific scenario** — what happens, at what threshold
- **Mitigation** — what you're doing to prevent it
- **Trigger** — what event will tell you it's time to act
- **Cost** — what the mitigation costs (time, money, complexity)