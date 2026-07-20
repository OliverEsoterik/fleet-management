---
name: design-doc
description: >
  Generate structured design documents following a proven template. Captures
  context, goals/non-goals, proposed design, alternatives, trade-offs, and
  implementation plans in the style of industry-standard technical design
  documents.
---

# Design Doc — Structured Technical Design Documents

## Overview

A design document captures the high-level implementation strategy and key design decisions for a software system or feature, with emphasis on the trade-offs considered. Its primary audience is other engineers — the doc exists to get consensus, identify issues early, and preserve organizational memory.

Use this skill when you need to:
- Propose a significant feature or system change
- Document architecture decisions for a new component
- Get alignment before writing code on a non-trivial effort
- Create a record of reasoning that future maintainers can trace

If the solution is trivially obvious, you don't need a design doc — just write the code. If you're unsure about the right design, that's exactly when to write one.

**Announce at start:** "I'm using the design-doc skill to write a design document for [feature]."

**Output path:** `docs/design/<feature-name>.md`

**Reference example:** Read `docs/evals-design.md` for the canonical example of this skill's output style.

---

## Core Principles

These five principles govern every design doc produced by this skill. They are not suggestions.

### 1. Non-goals are the most powerful clarifying device

Explicitly stating what the system does NOT aim to do prevents scope creep and unstated expectations. A goal like "scalable" is meaningless until paired with a non-goal like "does not need multi-region replication." The non-goal is what makes the goal concrete.

Include at least as many non-goals as goals. For each non-goal, explain *why* it was excluded. The reader's first reaction to a non-goal is "why not?" — answer it before they ask.

### 2. Design docs are about decisions, not about code

The value of a design doc is in the trade-offs and reasoning, not in the implementation details. A doc that only describes the chosen approach is a tutorial, not a design doc. If you find yourself writing more about how something works than *why* it was chosen, you've lost the plot.

### 3. The "Why" must precede the "What"

Every section should explain why a choice was made before describing what was chosen. "We chose PostgreSQL because we need strong consistency guarantees and complex joins" is better than "We're using PostgreSQL." The what is obvious from the why.

### 4. Trade-offs over implementation detail

Spend more space on rejected alternatives and their trade-offs than on the implementation details of the chosen approach. The chosen approach is what the code will show. The rejected alternatives are what the design doc preserves.

### 5. Prose narrative over bullet points

Use paragraphs and arguments, not lists. Bullet points compress reasoning; prose forces you to justify connections. Use bullet points only for enumerations (goals, non-goals, lists of options). For argumentation — why this matters, why this choice, why not that one — write paragraphs.

---

## Required Sections

Follow these sections in order. Each section follows the same pattern: explain why it matters first, then provide concrete guidance.

### 1. Title and Metadata

Every design doc starts with a header block that tells the reader what they're looking at, how current it is, and what research went into it.

```
# Feature Name — Design Document

> **Status:** Draft | In Review | Accepted
> **Date:** YYYY-MM-DD
> **Research basis:** [Author (year) — key finding; Author (year) — key finding]
> **Practical basis:** [existing systems, prior art, codebase references]
```

- **Status** tracks lifecycle. Start at "Draft." Move to "In Review" when circulating. Move to "Accepted" when implemented or accepted as the plan.
- **Research basis** cites specific sources that informed the design. One line per source. This grounds the doc in reality and shows the work was done.
- **Practical basis** references existing systems, prior implementations, or codebase conventions that the design builds on.

### 2. Context and Motivation

Why this doc exists. What problem is being solved. Who the stakeholders are. Why now, not later.

Start with the problem, not the solution. The reader needs to understand the pain before they can evaluate the fix.

Include:
- What is the current state? (facts, not opinions)
- What is the specific problem or opportunity?
- Who is affected? (users, operators, other systems)
- Links to related issues, docs, or prior work
- Why this timing? What changed to make this necessary now?

**Example opening (from the reference doc):**

> Skills in this project are Markdown files that instruct an LLM agent what to do. Unlike traditional code, there is no compiler, no type checker, no test runner. A skill "works" if the agent interprets it correctly and produces the expected output. This is fragile.

This is a good opening: it states the current state, identifies the problem in one sentence, and gives the reader an immediate understanding of why the doc exists.

### 3. Goals and Non-Goals

This is the most important section. It defines what success looks like and — crucially — what it doesn't.

**Goals:** What the system/feature WILL achieve. 3-5 concrete goals. Each should be measurable or at least verifiable. Not "make it fast" but "support 1000 concurrent users with p99 latency under 200ms."

**Non-goals:** What it will NOT do. At least as many non-goals as goals. Each non-goal gets a "Why not" explanation that addresses the obvious objection.

Format:

```markdown
## 3. Goals and Non-Goals

### Goals
- **Goal 1:** [concrete, verifiable statement]
- **Goal 2:** [concrete, verifiable statement]

### Non-Goals
- **Non-goal 1:** [what we're explicitly not doing]
  _Why not:_ [explanation — what trade-off or constraint made this a non-goal]
- **Non-goal 2:** ...
```

**Example from the reference doc:**
The reference doc doesn't have a formal Goals section (it's a methodology doc, not a feature design), but its section structure serves the same purpose. Every section starts with a clear claim about what it covers and what it doesn't.

### 4. Proposed Design

The chosen approach. This section should explain, not just describe. By the time a reader finishes this section, they should understand what the design is, how it works at a high level, and *why* this approach works for the stated goals.

#### 4.1. Architecture Overview

High-level structure, components, data flow. A diagram in ASCII or text is appropriate here if it clarifies the architecture:

```
[Client]  -->  [API Gateway]  -->  [Service A]  -->  [Database]
                        \               \
                         --> [Auth]      --> [Queue]  --> [Worker]
```

Describe the components and their responsibilities. Show the data flow: what enters, what gets transformed, what exits.

#### 4.2. Detailed Design

Deeper look at key components. Use code blocks for concrete formats — JSON schemas, directory trees, API signatures, config structures. Do not copy-paste full interface definitions; only include what's relevant to the design trade-offs.

```json
{
  "api_version": "v1",
  "endpoints": {
    "POST /evaluate": "Run a single eval on a skill",
    "GET /results/{id}": "Retrieve eval results by ID"
  }
}
```

#### 4.3. User-Facing Changes

If the design changes what users see or do, describe it here. What stays the same? What changes? What must users learn or unlearn?

### 5. Alternatives Considered

This is the most valuable section for future readers. A future engineer debugging a problem needs to know what else was tried and why it didn't work. Without this section, they'll repeat the same failed explorations.

For each alternative:
- **Brief description:** What was the alternative approach?
- **Pros:** What made it attractive?
- **Cons:** Why was it ultimately not the right choice?
- **Why rejected:** Explicit statement of why it was not selected. This is the most important part.

Include alternatives that an informed reader would think of. "Why not just use X?" should be answered here before the reader has to ask.

Minimum 2 alternatives. 3-4 is better. If you cannot think of alternatives, you haven't thought deeply enough about the problem.

### 6. Cross-Cutting Concerns

Each concern gets its own subsection. Cover only what's relevant — skip concerns that don't apply to this design.

#### 6.1. Security
Threat model, authentication, authorization, data protection, secrets management. What attack vectors does this design introduce or mitigate?

#### 6.2. Performance
Latency expectations, throughput, scaling behavior, bottlenecks. How does this design perform under load? What's the scaling ceiling?

#### 6.3. Observability
Logging, metrics, monitoring, alerting, tracing. How will operators know the system is healthy? How will they debug it when it's not?

#### 6.4. Testability
How does the design enable or hinder testing? Unit tests, integration tests, end-to-end tests. Can critical paths be tested without a full deployment?

#### 6.5. Operational Impact
Deployment strategy, rollback plan, migration path, data migration. What happens when this ships? What happens when it needs to be rolled back?

### 7. Trade-offs and Consequences

A structured discussion of what this design gains and what it sacrifices. This is distinct from Section 5 (alternatives) — this section is about the *chosen* design's own trade-offs, not comparisons with rejected alternatives.

Format: paired statements. Each trade-off has a clear upside and downside.

| Decision | Upside | Downside |
|----------|--------|----------|
| Using PostgreSQL over SQLite | Strong consistency, complex queries | Operational overhead of a server |
| Async processing via queue | Resilience under load | Eventual consistency, complexity |

Don't hide the downsides. A design doc that only presents positives is a sales pitch, not a design document. The downsides are what the team needs to plan for.

### 8. Implementation Plan

The design doc should be actionable. A phased implementation plan with concrete deliverables tells the reader what happens next and in what order.

Each phase:
- **What gets built**
- **Estimated effort** (developer-sessions or weeks, not hours)
- **Dependencies** (on other phases, external teams, infrastructure)
- **Shipping criteria** (how do you know this phase is done?)

Phases should be independent where possible — one phase should not block another unless there's a real dependency.

```
### Phase 1 — Infrastructure (2-3 sessions)

1. Create directory structure and core data model
2. Implement configuration parsing
3. Write unit tests for data model

### Phase 2 — Core logic (2-3 sessions)

4. ...
```

---

## Style Guide

The output style of this skill is modeled on `docs/evals-design.md`. Follow these rules:

### Voice

- **Direct, opinionated openings.** Every section starts with a strong claim or explanation, not a definition. "A design doc is about decisions" not "Design documents are documents that describe design decisions."
- **No fluff.** Every sentence carries weight. No padding, no filler, no "In today's fast-paced world," no "It is important to note that."
- **Assume an intelligent reader.** Don't explain fundamentals. Link to references instead.
- **Technical and objective.** State facts about the system, environment, and constraints. Avoid marketing language.

### Formatting

- **Bold for key concepts.** Core terms, principles, and emphasis get **bold**.
- **Code blocks for concrete formats.** JSON schemas, directory trees, API signatures, config files. Not abstract descriptions.
- **Numbered sections with subsections (1.1, 2.1 format).** Clear hierarchy. Use the format `## 1. Section Name` and `#### 1.1. Subsection Name`.
- **Blockquotes for metadata headers.** The status/date/research block is a single blockquote.
- **Tables for structured comparisons.** Trade-offs and alternatives work well in tables.

### Content Rules

- **Every section must explain "why" before "what".** If you can't explain why the section exists, it doesn't belong.
- **Address obvious objections.** Include "Why not" subsections, "What about X?" discussions, and direct counters to the most likely criticisms.
- **Examples are not optional.** Every abstract rule should be followed by a concrete example. The reference doc uses examples extensively — do the same.
- **Implementation plan is not optional.** A design doc without an implementation plan is unfinished.

---

## Self-Review Checklist

Before finishing, check every item. If any fails, fix it.

1. Does the doc have a status, date, and research/practical basis in the header?
2. Are non-goals explicitly stated with at least as many non-goals as goals?
3. Are at least 2 alternatives considered and rejected with reasoning?
4. Does each section explain the "why" before the "what"?
5. Are trade-offs of the chosen design discussed, not just implementation details?
6. Is the implementation plan phased with concrete deliverables?
7. Is the doc concise? (10-20 pages for major, 1-3 pages for mini)
8. Does the doc avoid placeholder text (TBD, TODO, FIXME)?
9. Does the doc use prose narrative, not just bullet points, for the main argumentation?
10. Are obvious objections addressed directly (not assumed to be understood)?

---

## References

- **Canonical example:** `docs/evals-design.md` — the reference design document that this skill's output style is based on
- **Research synthesis:** `work/design-doc-research/synthesis.md` — the research that informed this skill's structure
- **Google design doc culture:** Malte Ubl, "Design Docs at Google" (industrialempathy.com) — the most widely referenced design doc framework
- **ARC42:** arc42.org — comprehensive architecture documentation template
- **ADR pattern:** Michael Nygard, "Documenting Architecture Decisions" (thinkrelevance.com, 2011) — lightweight architecture decision records
- **Amazon 6-pager:** Internal Amazon narrative format for design decisions