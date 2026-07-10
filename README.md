# Agent Helpers

Multi-agent orchestration system using specialist agents in `agents/` and a fleet workflow skill in `skills/invoke-fleet/`.

## How to use

Start a session by invoking the fleet skill:

```
/skill:invoke-fleet <your task description>
```

The fleet skill will guide the agent through:
1. **Analyze & match** — pick a primary agent from `agents/` for your task
2. **Delegate** — launch the primary agent in a tmux session via `tools/delegate.sh`
3. **Orchestrate** — poll for consultation requests and route them to specialist agents (code review, security, python expert) via `tools/orchestrate.sh`
4. **Collect** — capture results with `tools/collect.sh`
5. **Cleanup** — remove work artifacts with `tools/cleanup.sh`

A pi extension is planned (`docs/plans/2026-07-10-fleet-extension.md`) to wrap these scripts into a `fleet_delegate` custom tool and `/fleet` slash command for structured input/output.

## Structure

### Agents

| Path | Purpose |
|---|---|
| `agents/code-reviewer/brain.md` | Expert code reviewer for quality, security, performance, and maintainability |
| `agents/python-expert/brain.md` | Python language expert for idiomatic Python, optimization, debugging |
| `agents/security-auditor/brain.md` | Security expert for vulnerability assessment, penetration testing, secure coding |
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
| `skills/update-readme/` | Audit and update README.md to reflect current project structure |
| `skills/architect/` | Architect / implementation lead mode (built-in) |
| `skills/sre/` | Site Reliability Engineer / security review mode (built-in) |

### Other

| Path | Purpose |
|---|---|
| `.pi/extensions/` | Pi extension source (planned — see `docs/plans/`) |
| `docs/plans/` | Implementation plans |
| `work/todo/` | Consultation inbox (primary → consultant) |
| `work/response/` | Consultation responses (consultant → primary) |
| `work/done/` | Completion signals |
| `work/recap.md` | Missing agent reports |

## Adding an agent

Create `agents/<name>/brain.md` with YAML frontmatter and agent instructions. It must reference `agents/shared/WORKFLOW.md` for collaboration rules. The agent will then be discoverable by the fleet workflow.

```
---
name: <agent-name>
description: <one-line description of expertise>
---

<full agent instructions, referencing shared/WORKFLOW.md for consultation rules>
```

## Adding a skill

Create `skills/<name>/SKILL.md` following the standard skill format (YAML frontmatter with `name` and `description`, then markdown body). Optionally include a `tools/` subdirectory with shell scripts that the skill references. Skills are auto-discovered by pi and available via `/skill:<name>`.

## Updating this README

```
/skill:update-readme
```

This skill scans the project structure (agents, skills, tools, docs, extensions) and reconciles README.md against what's actually on disk.