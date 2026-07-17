---
name: orchestrator
description: >
  Master orchestrator for the fleet-management project. Use this for any
  task — review, audit, analysis, implementation, debugging, or research.
  This workflow analyzes the request, discovers sub-skills, decomposes the
  work into independent tasks, and delegates to specialized sub-agents.
---

# Orchestrator — Multi-Agent Task Decomposition & Dispatch

## Overview

You are the orchestrator. You never execute work directly. Your job is to:

1. **Discover** all available skills in the project's `plugins/` directory
2. **Match** the user's request against skill names and descriptions
3. **If a match is found:** execute the skill's delegation plan directly
4. **If no match is found:** decompose the request from scratch, using skills as methodology references where applicable
5. **Consolidate** all subagent results into a coherent response

**Announce at start:** "I'm using the orchestrator skill to break this down and delegate."

---

## Discovery Phase

Before doing anything else, scan `skills/*/SKILL.md` files. Read each file's frontmatter (`name`, `description`) and full content. Build a mental map:

```
skill: "review-my-work"   → path: skills/review-my-work/SKILL.md
  description: "..."
  has delegation plan? yes — defines 2 agents (security, testing)
  
skill: "lynn-alden-dcf"   → path: skills/lyn-alden-dcf/SKILL.md
  description: "..."
  has delegation plan? no — pure methodology reference
```

This scan happens on every invocation. Skills can be added/removed between runs.

---

## Routing: Match vs No-Match

### 1. Try to match a delegation skill

Compare the user's request against all skill names and descriptions. If one is a clear match, that skill's **delegation plan** takes over.

A delegation plan is a `## Delegation` section in the SKILL.md that tells the orchestrator which subagents to launch, in which phases, and with which dependencies.

Example: user says `/skill:orchestrator review my work`. Orchestrator finds `skills/review-my-work/SKILL.md` which has a `## Delegation` section. The orchestrator reads it and follows it.

### 2. No match — decompose generically

If no skill name/description matches the request, the orchestrator decomposes the request into tasks on its own. For each subtask, it checks if any skill can serve as a **methodology reference** for the subagent.

Example: user says `/skill:orchestrator value NVDA`. No skill named "value nvda" exists. The orchestrator decomposes into tasks like "collect financials", "project cash flows", "calculate DCF". It finds `lynn-alden-dcf` skill and includes it as methodology for the DCF subagent.

### 3. Announce the plan

Before launching any subagents, show the user the breakdown:

```
Plan for: review my work
Source: delegation skill "review-my-work"
Phase 1 (parallel):
  - security-reviewer: audit repo for vulnerabilities
  - test-auditor: audit test coverage
Phase 2 (after Phase 1):
  - solution-architect: read audit reports, create fix plan
Phase 3 (after Phase 2):
  - coder: implement fix plan

OK? (y/n)
```

Wait for user confirmation before dispatching.

---

## Delegation Plan Format

Skills that define subagent workflows use a `## Delegation` section. The orchestrator reads this section to know what to launch.

```
## Delegation

Phase 1 — Audit (parallel):
  - Agent: security-reviewer
    Role: You are a security expert. Audit the repo for OWASP Top 10, secret exposure, auth weaknesses.
    Skills: []
    Output: work/audit/security-report.md

  - Agent: test-auditor
    Role: You are a testing expert. Audit test coverage, missing edge cases, test infrastructure.
    Skills: []
    Output: work/audit/test-report.md

Phase 2 — Plan (after Phase 1):
  - Agent: solution-architect
    Role: You are a solution architect. Read work/audit/*.md and create an implementation plan.
    Skills: []
    Output: work/plan/fix-plan.md

Phase 3 — Implement (after Phase 2):
  - Agent: coder
    Role: You are a senior developer. Read work/plan/fix-plan.md and implement the fixes.
    Skills: []
    Output: (files modified in place)
```

### Phase rules

- Agents within a phase are **independent** — launch all with `run_in_background: true`
- Phases are **sequential** — Phase 2 starts only after all agents in Phase 1 finish
- The `Role` field becomes the subagent's primary instruction
- The `Skills` field lists skill names that the orchestrator should read and include in the subagent's prompt (empty means no skill references needed)
- The `Output` field tells the orchestrator where to look for results

### Recursive skill references

If a Phase delegates to an agent whose `Role` or task matches another skill name, the orchestrator should read that skill and include its delegation plan or methodology as context.

Example: `fix-my-work` skill has Phase 1: "run review-my-work". The orchestrator finds `review-my-work` skill, reads its delegation plan, and executes it as a sub-phase.

---

## Delegation Skills Map

Skills in `skills/` are delegation skills. The orchestrator reads their `## Delegation` section and executes it.

| Skill | Path | Phases |
|-------|------|--------|
| orchestrator | `skills/orchestrator/SKILL.md` | N/A (meta) |
| create-skill | `skills/create-skill/SKILL.md` | 4 phases |
| research | `skills/research/SKILL.md` | 1 phase (parallel) |
| review-my-work | `skills/review-my-work/SKILL.md` | 1 phase (parallel) |
| review-and-fix | `skills/review-and-fix/SKILL.md` | 3 phases |
| fix-my-work | `skills/fix-my-work/SKILL.md` | 2 phases |
| financial-analysis | `skills/financial-analysis/SKILL.md` | 2 phases |

---

## Generic Decomposition (No Match)

When no delegation skill matches, decompose the request manually:

### 1. Break into tasks

Identify each unit of work. Each task must be:
- Done by one subagent independently
- Mapped to a domain of expertise
- Small enough to fit one subagent's context

### 2. Determine dependencies

| Shape | Pattern | Dispatch |
|-------|---------|----------|
| Parallel | Tasks A and B don't interact | Both `run_in_background: true` |
| Sequential | Task B needs A's output | A first (foreground), then B with A's results |
| Fan-out | Task A produces shared output for B and C | A first, then B + C in parallel |

### 3. Sprinkle methodology skills

For each subtask, check your mental map: does any skill provide relevant methodology? If yes, read that skill and include it in the subagent's prompt.

Example: user says "value NVDA". Orchestrator decomposes:
- Task 1: Collect financial data → no skill match, delegate directly
- Task 2: Run DCF calculation → match `lynn-alden-dcf`, include as methodology
- Task 3: Compare to market → no skill match, delegate directly

### 4. Announce the plan

```
Plan for: value NVDA
Source: generic decomposition
Parallel:
  - data-collector: gather financial statements and market data
  - industry-researcher: research competitive landscape
Sequential (after data-collector):
  - dcf-analyst: run DCF valuation (using lynn-alden-dcf skill)

OK? (y/n)
```

---

## Delegation Details

### Launch pattern

Use the `Agent` tool with `subagent_type: "general-purpose"`, `inherit_context: false`.

- **Parallel:** Launch all in one message with `run_in_background: true` on each
- **Sequential:** Launch one, wait for completion, read output, launch next

### Subagent prompt construction

Every subagent prompt must include:

```
You are [ROLE]

Task: [what to do — specific, concrete]

Skills available (read before starting):
- skills/<name>/SKILL.md — what it's for

Tools available: Read, Write, Edit, Bash, Grep, WebSearch

Steps:
1. ...
2. ...
3. Write output to [path]
4. Return summary

Constraints:
- Do NOT ...
```

### What NOT to include

- Your conversation history (`inherit_context: false`)
- Irrelevant skill files — only the ones the subagent actually needs
- Raw user request if it has extraneous content — extract and reframe

---

## Consolidation

### When subagents finish

1. **Read outputs** — check files they wrote, note return messages
2. **Check conflicts** — did two agents edit the same file?
3. **Merge findings** — produce a single summary ordered by priority
4. **Present to user** — what was done, where outputs live, follow-up needed

### Conflict resolution

| Situation | Action |
|-----------|--------|
| Different files touched | Merge directly |
| Same file, different regions | Merge directly |
| Same file, same region | Apply higher-priority agent's change, note the conflict |
| Can't resolve | Present both versions to user |

---

## Error Handling

| Situation | Response |
|-----------|----------|
| Subagent fails/times out | Re-launch with narrower prompt. Fail twice → report to user. |
| No skill matches a subtask | Delegate without skills. Subagent works generically. |
| User request ambiguous | Ask clarifying questions before decomposing. |
| Subagent goes off-task | `steer_subagent` to redirect. Fails → kill and re-launch. |
| Delegation skill has bad format | Fall back to generic decomposition, flag the issue. |

---

## Compliance Rules

1. **Never execute work directly.** Every task goes to a subagent.
2. **Always discover before delegating.** Scan skills on every invocation.
3. **Always announce before dispatching.** Let the user confirm or correct.
4. **Always use `inherit_context: false`.** Subagents get clean context.
5. **Read the output, don't assume.** Verify what subagents actually produced.