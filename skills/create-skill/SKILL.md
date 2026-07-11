---
name: create-skill
description: Methodology for creating new skills in the project. Follow this format when asked to create or write a new skill.
---

# Create Skill — Methodology

## Overview

This is a **methodology skill** — it does not define a delegation plan. It provides instructions that the orchestrator passes to a subagent tasked with creating a new skill file.

The orchestrator reads this file and includes it in the subagent's prompt so the subagent knows exactly what format to produce.

---

## Skill Types

There are two kinds of skill files in this project:

### 1. Delegation Skill

Defines a `## Delegation` section with phases, agents, roles, and dependencies. The orchestrator reads this section and executes it directly.

Use when: the skill defines a multi-agent workflow (review → plan → implement).

```
## Delegation

Phase 1 — Audit (parallel):
  - Agent: security-reviewer
    Role: You are a security expert. ...
    Skills: []
    Output: work/audit/security-report.md

  - Agent: test-auditor
    Role: You are a testing expert. ...
    Skills: []
    Output: work/audit/test-report.md

Phase 2 — Plan (after Phase 1):
  - Agent: solution-architect
    Role: You are a solution architect. ...
    Skills: []
    Output: work/plan/fix-plan.md
```

### 2. Methodology Skill

Provides step-by-step instructions, formulas, or methodology. No `## Delegation` section. The orchestrator reads it and includes it as reference material in a subagent's prompt.

Use when: the skill provides domain knowledge (DCF formulas, code review checklists, deployment procedures).

---

## Frontmatter Rules

The `name` field in frontmatter is what the orchestrator tries to match against the user's request. Choose it carefully:

```yaml
---
name: review-terraform
description: Review Terraform code for security, best practices, and style issues.
---
```

The name should be something the user might say: "review terraform", "create skill", "dcf analysis".

---

## File Location

All skills live at `skills/<name>/SKILL.md` relative to the project root. The directory name should match the frontmatter `name`.

---

## Output Convention

Subagents launched by the orchestrator should write their outputs to `work/<topic>/<file>.md` relative to the project root, unless the delegation plan specifies otherwise.

---

## What to Do When Creating a Skill

1. **Understand the request** — what should the skill do? Is it a workflow (launch multiple agents) or a reference (provide methodology)?
2. **Choose the type** — delegation or methodology
3. **Name it carefully** — the name is what the orchestrator matches against
4. **Write the file** at `skills/<name>/SKILL.md`
5. **If delegation:** write `## Delegation` with phases, agents, roles, skills, outputs
6. **If methodology:** write clear step-by-step instructions the subagent can follow