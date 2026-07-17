# Fleet Management

Multi-agent orchestration system using specialist agents (flat `.md` files in `agents/`) and skills in `plugins/skills/` and `plugins/workflows/`. The orchestrator skill is the primary entry point — it analyzes requests, discovers available skills, and delegates work to specialized sub-agents.

## How to use

### Use the orchestrator skill

```
/skill:orchestrator <your task description>
```

The orchestrator skill:
1. **Discovers** all available skills in `plugins/`
2. **Matches** your request against skill names and descriptions
3. **Executes** the matched skill's delegation plan, or decomposes from scratch if no direct match
4. **Consolidates** sub-agent results into a coherent response

### Use a skill directly

```
/skill:<skill-name> <task description>
```

Skills are auto-discovered by pi and available via `/skill:<name>`.

### Use an agent directly

```
run as financial-analyst and value NVDA
run as reviewer and audit this PR
```

This invokes the agent's `<name>.md` file from the `agents/` directory and launches a dedicated sub-agent with the full context.

## Structure

### Agents

| Path | Purpose |
|---|---|
| `agents/financial-analyst.md` | Financial analyst for DCF valuation, balance sheet analysis, cashflow analysis, and investment assessment (uses Lyn Alden methodology) |
| `agents/reviewer.md` | Orchestrator for code review — invokes Security Auditor, Test Engineer, and DevOps Engineer agents and consolidates their reports |
| `agents/gitops-expert.md` | GitOps audit specialist — reviews ArgoCD/Flux configurations against security hardening, deployment safety, and operational maturity checklists |
| `agents/shared-workflow.md` | Cross-agent collaboration rules (read by all agents) |

### Skills

| Path | Purpose |
|---|---|
| `plugins/workflows/orchestrator/` | Master orchestrator — analyzes requests, discovers skills, decomposes work, and delegates to specialized sub-agents |
| `plugins/skills/lynn-alden-dcf/` | Discounted Cash Flow analysis (Lyn Alden's tutorial methodology) |
| `plugins/skills/update-readme/` | Audit and update README.md to reflect current project structure |
| `plugins/workflows/review-and-fix/` | Full pipeline — review the repository, plan fixes, and implement them |
| `plugins/workflows/review-my-work/` | Review the repository for security vulnerabilities, test quality, and infrastructure issues |
| `plugins/workflows/fix-my-work/` | Diagnose and fix issues in the repository |
| `plugins/workflows/financial-analysis/` | Diagnose and fix issues in the repository (shared with `fix-my-work`) |
| `plugins/workflows/create-skill/` | Create a new skill in the project with research, synthesis, planning, and writing phases |

### Other

| Path | Purpose |
|---|---|
| `docs/plans/` | Implementation plans |
| `work/` | Consultation artifacts (todo, response, done, recap directories) |

## Adding an agent

Create `agents/<name>.md` with YAML frontmatter and agent instructions. The agent will then be discoverable by the orchestrator skill and available for direct invocation.

```
---
name: <agent-name>
description: <one-line description of expertise>
---

<full agent instructions>
```

Agents that need to consult other agents should reference the `agents/shared-workflow.md` collaboration rules.

## Adding a skill

Create `plugins/workflows/<name>/SKILL.md` or `plugins/skills/<name>/SKILL.md` following the standard skill format (YAML frontmatter with `name` and `description`, then markdown body). Skills are auto-discovered by pi and available via `/skill:<name>`. For the full skill creation workflow, use:

```
/skill:create-skill <description of the skill you want to create>
```

## Updating this README

```
/skill:update-readme
```

This skill scans the project structure (agents, plugins, docs) and reconciles README.md against what's actually on disk.