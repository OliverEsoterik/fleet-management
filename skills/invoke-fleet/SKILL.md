---
name: invoke-fleet
description: Use this skill to activate the multi-agent fleet — launch a primary agent in tmux and orchestrate a hub-and-spoke consultation workflow with specialist agents
---

# Invoke Fleet — Multi-Agent Orchestration

## Overview

This skill activates a **hub-and-spoke** multi-agent system. A primary agent (you) owns the task and consults specialist agents from the `agents/` directory for their expertise. Consultants report back, you revise and iterate.

**Announce at start:** "I'm using the invoke-fleet skill to orchestrate a multi-agent workflow."

**Prerequisites:** The project must have an `agents/` directory with `brain.md` files per agent and `agents/shared/WORKFLOW.md`.

---

## Tooling

This skill ships with shell scripts in the `tools/` directory (relative to this skill file):

| Script | Purpose |
|--------|---------|
| `tools/delegate.sh` | Launch a primary agent in a new tmux session |
| `tools/orchestrate.sh` | Poll `work/` directory and route consultation requests to consultants |
| `tools/collect.sh` | Capture pane output from a tmux session and kill it |
| `tools/cleanup.sh` | Remove all `work/` artifacts |

**All scripts accept `--help` or wrong args to show usage.** They are invoked as `bash tools/<script>.sh <args>`. The skill directory is `<skilldir>` — substitute the actual path when running.

---

## Agents Directory Structure

```
agents/
├── <agent-name>/        # Each specialist agent is a directory
│   └── brain.md         # Agent instructions (YAML frontmatter + body)
├── shared/
│   └── WORKFLOW.md      # Cross-agent collaboration rules (mandatory reading for all agents)
```

---

## Workflow

### Step 1: Analyze & Match

1. Analyze the user's request and break it into tasks.
2. Match each task to a primary agent in `agents/`.
3. If no agent matches a task, report the gap into `work/recap.md`.

### Step 2: Delegate Primary Agent

Run the delegate script with the project directory, agent name, and task description:

```bash
bash <skilldir>/tools/delegate.sh /path/to/project <agent-name> "<task description>"
```

This creates a tmux session named `pi-agent-<timestamp>-<agent-name>`, runs `cat brain.md WORKFLOW.md | pi -p "<task>"` inside the agent's directory, and prints `--- PRIMARY DONE ---` on completion. The session stays alive for 1 hour for manual inspection.

**Example:**
```bash
bash /home/oliver/agent-helpers/skills/invoke-fleet/tools/delegate.sh /home/oliver/my-project code-reviewer \
  "Review the auth module in src/auth/ for vulnerabilities and suggest fixes"
```

### Step 3: Orchestrator Loop

After launching the primary agent, run the orchestrate script:

```bash
bash <skilldir>/tools/orchestrate.sh /path/to/project <primary-agent-name> [max-depth]
```

This loops up to `max-depth` times (default 5), polling for:
- `work/escalation.md` → breaks (unresolvable issue)
- `work/done/<primary>.md` → breaks (completion)
- `work/todo/*.md` → routes each to the appropriate consultant in a new tmux session, waits 30 seconds, captures output, kills the session

**Example:**
```bash
bash /home/oliver/agent-helpers/skills/invoke-fleet/tools/orchestrate.sh /home/oliver/my-project code-reviewer 5
```

### Step 4: Collect Results

If you need to manually inspect a running or completed session:

```bash
bash <skilldir>/tools/collect.sh <session-name>
```

Captures pane output to stdout and kills the session.

### Step 5: Cleanup

```bash
bash <skilldir>/tools/cleanup.sh /path/to/project
```

Removes `work/todo/`, `work/response/`, `work/done/`, and `work/escalation.md`.

---

## Cross-Agent Collaboration Rules (from WORKFLOW.md)

This section is what each agent sees in its context — you (the primary agent) must follow it too.

### When to Consult

Ask yourself:
- Does my output need **code review**?
- Does it need a **security audit**?
- Does it need **deployment / DevOps** review?
- Does it need **testing**?
- Does it touch **infrastructure** (Docker, K8s, cloud)?
- Is there anything I'm **not an expert in** that affects this task?

If yes to any, you must consult.

### How to Consult

Write a consultation request to `work/todo/<agent-name>.md`:

```markdown
# Consultation for <agent-name>

requested_by: <your-agent-name>
already_consulted:
  - <your-agent-name>

## What I produced

<brief summary>

## What I need from you

<specific question or task>

## Where to find my output

<file paths>
```

### How to Receive Results

When a consultant finishes, it writes its response to `work/response/<your-agent-name>/<agent-name>.md`. Read it, apply the feedback, iterate if needed.

### Iteration Limits

- Max **3 rounds** per consultant.
- Track rounds in `work/response/<your-agent-name>/round.txt`.
- After 3 rounds without resolution → write `work/escalation.md`.

### Signaling Completion

When all consultations are resolved (or escalated), write:

```markdown
work/done/<your-agent-name>.md
```

---

## File Contract

| Path | Purpose |
|------|---------|
| `work/todo/<agent>.md` | Consultation request (primary → consultant) |
| `work/response/<primary>/<agent>.md` | Consultation response (consultant → primary) |
| `work/response/<primary>/round.txt` | Round tracking per consultant |
| `work/done/<primary>.md` | Primary signals completion |
| `work/escalation.md` | Primary signals unresolvable issue |
| `work/recap.md` | Gaps (agent directory missing for needed expertise) |

---

## Execution Checklist

When you invoke this skill, follow these steps in order:

1. **Read** `agents/<agent-name>/brain.md` for the agent you'll delegate to
2. **Read** `agents/shared/WORKFLOW.md`
3. **Launch** the primary agent: `bash <skilldir>/tools/delegate.sh <project> <agent> "<task>"`
4. **Orchestrate**: `bash <skilldir>/tools/orchestrate.sh <project> <agent> [max-depth]`
5. **Collect** (if needed): `bash <skilldir>/tools/collect.sh <session>`
6. **Present** the result to the user
7. **Clean up**: `bash <skilldir>/tools/cleanup.sh <project>`

Replace `<skilldir>` with the actual path to this skill's directory (detected at runtime — available as `$(dirname "$(readlink -f "$0")")` in scripts, or hardcode as the path shown in the agent's available skills list).