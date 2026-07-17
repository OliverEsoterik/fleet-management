---
name: architect
description: >
  Architectural design workflow for complex codebase changes. Deeply
  understands the codebase and user requirements, researches solution
  options, documents decisions as ADRs, and produces implementation
  plans. Human-in-the-loop at every stage.
---

# Architect — Architectural Design Workflow

## Overview

This skill guides architectural decision-making for complex codebase changes. It follows a sequential workflow with human review checkpoints at every stage.

**Execution model:** This is a **methodology skill**. The orchestrator launches a single sub-agent with this SKILL.md as its instructions. That sub-agent runs all phases sequentially in its own context, launching sub-sub-agents for specific tasks (research, plan writing) and reading their file outputs for handover.

**File-based handover between sub-sub-agents:** When you launch a sub-sub-agent (e.g. for research), it runs in its own context with no access to your conversation or files. You must include all relevant context in its prompt. When it completes, read the files it wrote. This is how information flows between phases.

**Core principle:** You cannot design a good architecture without deep understanding of both the problem (user request) and the current system (codebase). The workflow enforces this before any solution work begins.

**Announce at start:** "I'm using the architect skill to design the architecture for [task]."

**Outputs produced:**
- `work/architect/analysis.md` — codebase + user request analysis (phase 1)
- `work/architect/research.md` — solution research findings (phase 2)
- `docs/decisions/ADR-NNN-title.md` — architecture decision record (phase 4)
- `docs/superpowers/plans/YYYY-MM-DD-feature.md` — implementation plan (phase 6)

---

## Workflow Handover Contract

Every phase produces a file. Every subsequent phase that needs that data reads it from the file. Sub-sub-agents get context via their prompt (you include the relevant analysis), not via shared memory.

| Phase | Produces | Read by |
|-------|----------|---------|
| 1. Deep Understanding | `work/architect/analysis.md` | Phases 2, 3, 4, 6 |
| 2. Solution Research | `work/architect/research.md` | Phases 3, 4 |
| 3. Present Options | *(user decision — no file)* | Phase 4 |
| 4. Write ADR | `docs/decisions/ADR-NNN-*.md` | Phases 5, 6 |
| 5. Present ADR | *(user approval — no file)* | Phase 6 |
| 6. Implementation Plan | `docs/superpowers/plans/YYYY-MM-DD-*.md` | Phase 7 |
| 7. Execute | *(files modified in place)* | — |

---

## Workflow

### Phase 1 — Deep Understanding

**Goal:** Understand the codebase and user request well enough to propose sound architectural options.

**Do not skip this phase.** Most architectural failures come from insufficient understanding of existing code.

#### Step 1.1 — Understand the user request

Re-read the user's request carefully. Ask clarifying questions if anything is ambiguous:
- What problem are they trying to solve?
- What are the constraints (time, tech stack, team size, scalability requirements)?
- Are there non-functional requirements (performance, security, maintainability)?
- What does success look like — what would they consider "done"?

If the request has two plausible interpretations, **ask** before proceeding. Do not pick silently.

#### Step 1.2 — Understand the codebase

Explore the codebase systematically. For targeted lookups, use Explore sub-agents (`subagent_type: "Explore"`) to keep your context clean. Give each one specific questions, not generic "explore everything".

Questions to answer:
1. **Project structure:** What directories exist? What's the build system? Package manager?
2. **Existing patterns:** How are features organized? How is state managed? How are errors handled?
3. **Relevant files:** Read the files that will be touched, and the files that call them.
4. **Configuration:** What config files, environment variables, and deployment setup exists?
5. **Tests:** What testing patterns exist? What's the test coverage like?

#### Step 1.3 — Write the analysis document

Write everything you learned into `work/architect/analysis.md`.

**This file is the handover document for all subsequent phases.** Make it thorough. Include:

- **User request summary:** What they asked for, in your own words
- **Codebase context:** Key files, patterns, dependencies, and architecture relevant to the request
- **Constraints:** Any boundaries the solution must respect
- **Open questions:** Things you're still unsure about

**Format:**
```markdown
# Architectural Analysis: [request title]

## User Request
[summary of what the user asked for]

## Codebase Context
[relevant structure, patterns, and files]

## Constraints
- [constraint 1]
- [constraint 2]

## Open Questions
- [question 1]
- [question 2]
```

---

### Phase 2 — Solution Research

**Goal:** Research potential solutions — technical options, libraries, patterns, and approaches — grounded in the codebase context from Phase 1.

**Handover in:** Read `work/architect/analysis.md`
**Handover out:** Write `work/architect/research.md`

#### Step 2.1 — Delegate to the research skill

Launch a sub-agent using the `research` skill (`run_in_background: true`).

The research sub-agent runs in its own context — it cannot read your files or see our conversation. You must include all relevant context in its prompt: the user request summary, constraints, and codebase context from `work/architect/analysis.md`.

Example sub-agent prompt:

> Use the research skill to research architectural approaches for [problem].
> Sources: arxiv, github, web
> Context:
> - User request: [one paragraph]
> - Constraints: [list]
> - Relevant codebase info: [key files, tech stack, patterns]
> Specific questions to answer:
> 1. [question 1]
> 2. [question 2]

#### Step 2.2 — Read the research report

Wait for the sub-agent to complete. Then read `work/research/report/report.md` to get the consolidated findings.

#### Step 2.3 — Write the architect's research document

Write research findings specific to the architectural decision to `work/architect/research.md`. This is not a dump of the research report — it's a focused summary that relates the findings back to the codebase and the specific decision at hand. Organize by architectural option, not by source.

```markdown
# Solution Research: [request title]

## Option A: [approach name]
- **Description:** [what it is]
- **Fit with codebase:** [how well it integrates]
- **Sources:** [citations from research report]
- **Pros:** [list]
- **Cons:** [list]

## Option B: [approach name]
...
```

---

### Phase 3 — Present Options to User

**Goal:** Present the research findings and options to the user, then let them choose.

**Handover in:** Read `work/architect/analysis.md` and `work/architect/research.md`

#### Step 3.1 — Present

Show the user the options clearly:

1. Summarize each viable approach (2-3 sentences each)
2. For each, list pros and cons
3. If you have a recommendation, state it — but be clear about trade-offs
4. Present the trade-offs neutrally. Do not hide the downsides of your preferred option

#### Step 3.2 — Wait for decision

**Ask the user which option they prefer.** Do not proceed without their explicit choice.

---

### Phase 4 — Write ADR

**Goal:** Document the architectural decision as an Architecture Decision Record (ADR).

**Handover in:** Read `work/architect/analysis.md`, `work/architect/research.md`, and incorporate the user's decision from Phase 3.

#### Step 4.1 — Write the ADR

Create an ADR at `docs/decisions/ADR-NNN-title.md`. Use sequential numbering — check `docs/decisions/` for the next available number.

ADR template:

```markdown
# ADR-NNN: [Decision Title]

## Status
Accepted

## Date
YYYY-MM-DD

## Context
[The problem that prompted this decision. Include relevant constraints,
codebase context, and requirements from the user request.]

## Decision
[What was decided. Be specific — include technology names, patterns,
concrete architectural choices.]

## Alternatives Considered
[For each alternative, briefly describe it, list pros and cons, and
state why it was rejected. This is the most valuable section for
future readers.]

## Consequences
[What this decision means for the codebase, team, and future work.
Both positive and negative.]
```

---

### Phase 5 — Present ADR to User

**Goal:** Let the user review the ADR before implementation begins.

#### Step 5.1 — Present

Show the user the ADR. Ask them to review it. If they want changes, make them.

#### Step 5.2 — Wait for approval

**Do not proceed to implementation without user approval.** Ask explicitly: "Do you want to proceed with implementation?"

---

### Phase 6 — Implementation Plan

**Goal:** Produce a detailed, testable implementation plan.

**Handover in:** Read `work/architect/analysis.md` for codebase context. Read the ADR at `docs/decisions/ADR-NNN-*.md` for the architectural decision.

#### Step 6.1 — Delegate to the writing-plans skill

Launch a sub-agent using the `writing-plans` skill (`run_in_background: true`).

The writing-plans sub-agent runs in its own context — include all relevant context in its prompt: the user request, the ADR content, and key codebase context.

Example sub-agent prompt:

> Use the writing-plans skill to create an implementation plan for [feature].
>
> Context:
> - User request: [one paragraph]
> - Architectural decision (ADR): [key points from the ADR]
> - Relevant codebase: [files to touch, patterns to follow]
> - Constraints: [list]

**Do not write the plan yourself** — delegate to the writing-plans skill. It has better structure for this.

#### Step 6.2 — Read the plan

Wait for the sub-agent to complete. Read the plan file (the writing-plans skill saves to `docs/superpowers/plans/YYYY-MM-DD-*.md`).

#### Step 6.3 — Present plan

Show the user the completed plan. Ask if they want to proceed with execution.

---

### Phase 7 — Execute (optional)

**Goal:** Execute the plan — but only with explicit user permission.

**Handover in:** The plan file at `docs/superpowers/plans/YYYY-MM-DD-*.md`.

#### Step 7.1 — Ask before executing

**Do not execute without user approval.** Ask: "Do you want me to execute this plan?"

#### Step 7.2 — Delegate to the execute skill

If the user approves, launch a sub-agent using the `execute` skill. Include the plan path and any relevant context in the prompt.

---

## Self-Review Checklist

Before presenting any output to the user, check:

1. **Did I deeply understand the codebase?** Can I point to specific files and patterns I read?
2. **Did I surface assumptions?** Did I state "I'm assuming X" anywhere I was uncertain?
3. **Did I present options neutrally?** Are the trade-offs of each option clear?
4. **Did I wait for user input at each checkpoint?** Phases 3, 5, and 7 require explicit user decisions.
5. **Is the ADR complete?** Does it have context, decision, alternatives, and consequences?
6. **Did I delegate to the right skill?** research for research, writing-plans for plans, execute for execution — not ad-hoc.
7. **Did I include context in sub-sub-agent prompts?** They cannot read your files. If they needed info from a previous phase, you put it in their prompt.

## References

- ADR format based on Michael Nygard's ADR pattern and the fleet-management conventions
- Research skill: `skills/research/SKILL.md`
- Writing plans skill: `skills/writing-plans/SKILL.md`
- Execute skill: `skills/execute/SKILL.md`