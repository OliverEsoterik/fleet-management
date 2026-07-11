# Fleet Management

Multi-agent orchestration system using specialist agents in `agents/` and skills in `skills/`. Each agent is defined by a `brain.md` file, and you can invoke any agent on the fly via the `run-as-agent` skill.

## How to use

### Run a specific agent directly

```
run as financial-analyst and value NVDA
run as reviewer and audit this PR
```

This invokes the `run-as-agent` skill, which reads the agent's `brain.md`, loads any referenced skills, and launches a dedicated sub-agent with the full context.

### Use the fleet orchestration workflow

```
/skill:invoke-fleet <your task description>
```

The fleet skill guides through:
1. **Analyze & match** — pick a primary agent from `agents/` for your task
2. **Delegate** — launch the primary agent in a tmux session via `tools/delegate.sh`
3. **Orchestrate** — poll for consultation requests and route them to specialist agents via `tools/orchestrate.sh`
4. **Collect** — capture results with `tools/collect.sh`
5. **Cleanup** — remove work artifacts with `tools/cleanup.sh`

A pi extension is planned (`docs/plans/2026-07-10-fleet-extension.md`) to wrap these scripts into a `fleet_delegate` custom tool and `/fleet` slash command for structured input/output.

## Structure

### Agents

| Path | Purpose |
|---|---|
| `agents/financial-analyst/brain.md` | Financial analyst for DCF valuation, balance sheet analysis, cashflow analysis, and investment assessment (uses Lyn Alden methodology) |
| `agents/reviewer/brain.md` | Orchestrator for code review — invokes Security Auditor, Test Engineer, and DevOps Engineer agents and consolidates their reports |
| `agents/shared/WORKFLOW.md` | Cross-agent collaboration rules (read by all agents) |

### Skills

| Path | Purpose |
|---|---|
| `skills/invoke-fleet/` | Fleet orchestration — launch primary agent, route consultations, collect results |
| `skills/invoke-fleet/SKILL.md` | Skill instructions (invoke via `/skill:invoke-fleet`) |
| `skills/invoke-fleet/tools/delegate.sh` | Launch a primary agent in a new tmux session |
| `skills/invoke-fleet/tools/orchestrate.sh` | Poll `work/` directory and route consultation requests |
| `skills/invoke-fleet/tools/collect.sh` | Capture pane output from a tmux session and kill it |
| `skills/invoke-fleet/tools/cleanup.sh` | Remove all `work/` artifacts |
| `skills/lynn-alden-dcf/` | Discounted Cash Flow analysis (Lyn Alden's tutorial methodology) |
| `skills/run-as-agent/` | On-the-fly agent invocation — reads `agents/<name>/brain.md` and launches a sub-agent with the full definition |
| `skills/update-readme/` | Audit and update README.md to reflect current project structure |
| `skills/architect/` | Architect / implementation lead mode (built-in skill) |
| `skills/sre/` | Site Reliability Engineer / security review mode (built-in skill) |

### Other

| Path | Purpose |
|---|---|
| `.pi/extensions/` | Pi extension source (planned — see `docs/plans/`) |
| `docs/plans/` | Implementation plans |
| `work/todo/` | Consultation inbox (primary → consultant) |
| `work/response/` | Consultation responses (consultant → primary) |
| `work/done/` | Completion signals |

## Adding an agent

Create `agents/<name>/brain.md` with YAML frontmatter and agent instructions. The agent will then be discoverable by the `run-as-agent` skill and the fleet workflow.

```
---
name: <agent-name>
description: <one-line description of expertise>
---

<full agent instructions>
```

Agents that need to consult other agents should reference the `shared/WORKFLOW.md` collaboration rules.

## Adding a skill

Create `skills/<name>/SKILL.md` following the standard skill format (YAML frontmatter with `name` and `description`, then markdown body). Optionally include a `tools/` subdirectory with shell scripts that the skill references. Skills are auto-discovered by pi and available via `/skill:<name>`.

## Updating this README

```
/skill:update-readme
```

This skill scans the project structure (agents, skills, tools, docs, extensions) and reconciles README.md against what's actually on disk.