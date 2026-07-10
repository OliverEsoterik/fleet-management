## Cross-Agent Collaboration (Mandatory)

Before finishing your task, you must consult any other agents whose expertise could improve your output.

### Consultation model

You are the **primary agent** — you own the task. Other agents are **consultants**. You ask them for advice, they respond, you decide what to incorporate.

```
┌─────────────┐     consults      ┌──────────────┐
│             │ ────────────────→ │ Test Agent   │
│  Primary    │ ← ──────────────  │              │
│  Agent      │     reports back  └──────────────┘
│  (you)      │
│             │     consults      ┌──────────────┐
│             │ ────────────────→ │ DevOps Agent │
│             │ ← ──────────────  │              │
│             │     reports back  └──────────────┘
└─────────────┘
```

### When to consult

Ask yourself:
- Does my output need **code review**?
- Does it need a **security audit**?
- Does it need **deployment / DevOps** review?
- Does it need **testing**?
- Does it touch **infrastructure** (Docker, K8s, cloud)?
- Is there anything I'm **not an expert in** that affects this task?

If the answer to *any* of these is yes, you must consult.

### How to consult

Write a consultation request to `work/todo/<agent-name>.md`:

```markdown
# Consultation for <agent-name>

requested_by: <your-agent-name>
already_consulted:
  - <your-agent-name>

## What I produced

<brief summary of what you built/wrote>

## What I need from you

<specific question or task for this agent>

## Where to find my output

<file paths>
```

Replace `<agent-name>` with the directory name of the target agent (e.g. `test-automator`, `devops-engineer`, `security-auditor`).

### How to receive consultation results

When a consultant finishes, it writes its response to `work/response/<your-agent-name>/<agent-name>.md`.

Read that file, apply the feedback, and if needed, ask for another round.

### Iteration limits

- You have at most **3 rounds** of consultation per consultant.
- Track rounds in `work/response/<your-agent-name>/round.txt`:

```
consultant: test-automator
round: 1
max_rounds: 3
```

After 3 rounds without resolution, write a summary to `work/escalation.md` explaining what couldn't be resolved, and let the orchestrator handle it.

### Important rules

- Add **your own name** to `already_consulted` so the orchestrator doesn't start you again.
- Do **not** write a todo if the agent directory doesn't exist.
- If you think an agent *should* exist but doesn't, write the gap to `work/recap.md`.
- Be specific in "What I need from you" — vague requests produce vague results.
- When you're done (all consultations resolved or escalated), signal completion by writing `work/done/<your-agent-name>.md`.