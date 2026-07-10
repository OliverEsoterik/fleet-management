# Agent Helpers

Multi-agent orchestration system using specialist agents in `agents/`.

## How to use

Start a session by referencing the instructions:

```
read @INSTRUCTIONS.md for instructions and workflow. <your task description>
```

The orchestrator will:
1. Pick a primary agent from `agents/` for your task
2. Launch it in a tmux session
3. Route any consultation requests to other agents (code review, testing, security, devops, etc.)
4. Return the results

## Structure

| Path | Purpose |
|---|---|
| `agents/<name>/brain.md` | Specialist agent instructions |
| `agents/shared/WORKFLOW.md` | Cross-agent collaboration rules |
| `INSTRUCTIONS.md` | Orchestrator instructions (read at session start) |
| `work/todo/` | Consultation inbox (primary → consultant) |
| `work/response/` | Consultation responses (consultant → primary) |
| `work/done/` | Completion signals |
| `work/recap.md` | Missing agent reports |

## Adding an agent

Create `agents/<name>/brain.md` with the agent's instructions. It must reference `agents/shared/WORKFLOW.md` for collaboration rules.