---
name: run-as-agent
description: Use when the user asks you to run or invoke a specific agent defined in the agents/ directory — e.g. "run as financial-analyst", "invoke the reviewer agent", "act as agent X"
---

# Run As Agent

## Overview

Fleet agents are defined in `agents/<name>/brain.md` files. Each brain.md is a self-contained agent specification — it defines the agent's role, tools, workflow, and domain knowledge. When the user asks you to "run as agent X", you load the brain and launch it as a sub-agent.

## Workflow

```
User: "run as financial-analyst and value NVDA"
                    │
                    ▼
          Read agents/<name>/brain.md
                    │
                    ▼
          Identify referenced skills in brain.md
          (e.g. "MUST use the lyn-alden-dcf skill")
                    │
                    ▼
          Read those skill files
                    │
                    ▼
          Read agents/<name>/../shared/WORKFLOW.md
          (cross-agent collaboration contract)
                    │
                    ▼
          Launch general-purpose agent with:
            - brain.md content as system prompt
            - referenced skills appended
            - WORKFLOW.md appended
            - user's task as the goal
```

## Step-by-Step

### 1. Resolve the agent

```
agents/<agent-name>/brain.md
```

The agent name comes from the directory name under `agents/`. If the user says "run as financial-analyst", the path is `agents/financial-analyst/brain.md`. Resolve relative to the project root (`/home/oliver/fleet-management/`).

### 2. Read the brain.md

Read the full file. Extract:

- **Required tools** from the frontmatter `tools:` field (if any) — these tell you what the agent needs
- **Required skills** — look for phrases like "MUST use the X skill" or "Use the X skill"
- **Instructions** — the full body is the agent's system prompt

### 3. Read referenced skills

For each skill referenced in the brain (e.g. `lynn-alden-dcf`), read its `SKILL.md` from `skills/<skill-name>/SKILL.md`. You will include the skill content as supporting context in the sub-agent.

### 4. Read the shared WORKFLOW.md if the brain references it

Always read `agents/shared/WORKFLOW.md` and include it in the sub-agent's context. The collaboration contract applies to all agents.

### 5. Launch the sub-agent

Use a **general-purpose** sub-agent. The prompt must include:

```
You are acting as the [AGENT NAME] agent.

The following is your full agent definition:

[full content of brain.md]

--- Referenced Skills ---

[content of each referenced SKILL.md]

--- Shared Workflow ---

[content of agents/shared/WORKFLOW.md]

--- User Task ---

[the user's specific request]
```

Set the `model` parameter to a capable model (e.g. sonnet). Use `inherit_context: false` to give the sub-agent a clean context with just its brain definition.

### 6. Route the result

When the sub-agent finishes, report back to the user with a summary and the output location. The sub-agent's output files go wherever the brain.md specifies (each brain defines its own output convention). Check the brain for paths like `work/output/`, `work/result/`, etc.

## Agent Directory Layout

```
agents/
├── financial-analyst/
│   ├── brain.md                 # Agent definition
│   ├── work/                    # Runtime working directory (created as needed)
│   │   ├── output/              # Generated reports
│   │   ├── scripts/             # Generated scripts
│   │   └── todo/                # Consultation requests
│   └── research/                # Research data
├── reviewer/
│   ├── brain.md                 # Agent definition
│   └── work/                    # Runtime working directory (created as needed)
├── shared/
│   └── WORKFLOW.md              # Cross-agent collaboration rules
└── <any future agent>/
    ├── brain.md
    └── work/                    # Runtime working directory (created as needed)
```

> **Note:** The `work/` directories are created on demand by the agent during execution. Not all of them exist on disk until the agent has been run at least once.

## Tools Access

The brain.md frontmatter declares required tools. The sub-agent inherits the general-purpose agent's tools, which include:
- Read, Write, Edit, Bash, Grep
- WebSearch, WebFetch
- get_stock_info (stock data via yfinance)
- academic_search (research papers)
- Agent (launch further sub-agents)

If the brain declares custom tool needs beyond these, note the gap to the user.

## Example

User: "run as financial-analyst and value NVDA"

Your actions:
1. Read `agents/financial-analyst/brain.md`
2. Read `skills/lynn-alden-dcf/SKILL.md` (referenced in the brain)
3. Read `agents/shared/WORKFLOW.md`
4. Launch sub-agent with full context (brain + skill + workflow)
5. Report: "Launched financial-analyst for NVDA valuation. Report will appear in agents/financial-analyst/work/output/ when complete."
