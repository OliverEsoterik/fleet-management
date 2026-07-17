# Fleet Management

Multi-agent orchestration system using skills (`skills/<name>/SKILL.md`) for
pi (the coding agent harness). The orchestrator skill is the primary entry
point — it analyzes requests, discovers available skills, and delegates work
to specialized sub-agents.

## How to use

### Use the orchestrator (recommended)

```
/skill:orchestrator <task description>
```

The orchestrator:
1. Scans all skills in `skills/`
2. Matches your request against skill names and descriptions
3. Executes the matched skill's delegation plan, or decomposes from scratch
4. Consolidates sub-agent results

### Use a skill directly

```
/skill:<skill-name> <task>
```

For the full list of skills, see [`skills/README.md`](skills/README.md).
Most skills are designed to work through the orchestrator; direct invocation
is for targeted tasks (e.g., `/skill:setup-testing-workflows .`,
`/skill:update-readme`, `/skill:research best practices for Redis caching`).

### Use an agent directly

```
run as financial-analyst and value NVDA
```

This invokes the agent's `.md` file from `agents/`. Less common — most
functionality is exposed through skills.

## Structure

### Skills

All skills live in `skills/<name>/SKILL.md`. Each has YAML frontmatter with
`name` and `description`. Skills are auto-discovered by pi and available via
`/skill:<name>`.

| Skill | Type | Purpose |
|-------|------|---------|
| orchestrator | Delegation (meta) | Master entry point — discovers skills, routes requests |
| architect | Methodology | Architectural design with ADR + plans |
| better-products-habits | Methodology | Hiten Shah's 5 habits for product building |
| create-skill | Delegation | Create new skills with research + writing phases |
| execute | Delegation | Execute implementation plans with sub-agents |
| financial-analysis | Delegation | Multi-methodology analysis (DCF, Lynch, Taleb) |
| fix-my-work | Delegation | Diagnose and fix repo issues |
| git-workflow | Methodology | Branching, versioning, changelogs |
| lyn-alden-dcf | Methodology | DCF valuation reference |
| nassim-nicholas-taleb | Methodology | Antifragility/black swan critique |
| peter-lynch | Methodology | GARP/value analysis reference |
| research | Delegation | Multi-source parallel research |
| review-and-fix | Delegation | Full audit → plan → fix pipeline |
| review-my-work | Delegation | Security, test, and infrastructure audit |
| setup-testing-workflows | Methodology | GitHub Actions test workflow generator |
| stock-info | Methodology (data) | yfinance data provider for all analysis skills |
| update-readme | Methodology | Scan and reconcile README.md |
| writing-plans | Methodology | Implementation plan writer |

### Agents

Agent definitions in `agents/*.md` are invoked via `run as <name>`.

| Path | Purpose |
|------|---------|
| `agents/financial-analyst.md` | Financial analyst (DCF, balance sheet, cash flow) |
| `agents/reviewer.md` | Orchestrator for code review — invokes multiple auditors |
| `agents/gitops-expert.md` | GitOps audit (ArgoCD/Flux configurations) |
| `agents/shared-workflow.md` | Cross-agent collaboration rules |

### Other

| Path | Purpose |
|------|---------|
| `docs/plans/` | Implementation plans (read-only) |
| `docs/decisions/` | Architecture Decision Records (ADRs) |
| `work/` | Ephemeral consultation artifacts (todo, response, done, recap) |
| `skills/README.md` | Quick reference for all skills and how to invoke them |

## Adding a skill

Create `skills/<name>/SKILL.md` following the standard format:

```yaml
---
name: <skill-name>
description: > <one-line summary>
---

# Title

Contents...
```

Skills are auto-discovered by pi. For the full creation workflow, use:

```
/skill:create-skill <description>
```

## Adding an agent

Create `agents/<name>.md` with YAML frontmatter and agent instructions.
Agents referenced by the financial-analysis skill should follow the
cross-agent workflow in `agents/shared-workflow.md`.

## Updating this README

```
/skill:update-readme
```
