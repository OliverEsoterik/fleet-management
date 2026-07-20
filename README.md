# Fleet Management

Multi-agent orchestration system using the **graph engine** — a data-driven
state machine that routes work through autonomous nodes, the **chain-planner**
(which builds skill chains from your description), micro-loops, and local
human-in-the-loop interaction.

Skills (`skills/<name>/SKILL.md`) define workflows as node graphs or
methodology references. Agents (`agents/<name>.md`) wrap skills with
preferred models and domain expertise. The orchestrator skill scans both
and routes through the appropriate chain.

## How to use

### Use the orchestrator (recommended)

```
/skill:orchestrator <task description>
```

The orchestrator chains skills and agents together based on your request. Each step in the chain is a separate dispatch with its own model.

**Describe your own chain:** Say "research transformer architectures, then architect a solution, then review the plan." The chain-planner builds:
```
research [haiku] → architect [sonnet] → code-review [haiku] → consolidator
```
Three separate dispatches, each with a different model. No collapsing, no dedup.

**Or use a standard chain:** Say "implement feature X" and pick Fast (direct), Safe (implement + review), or Thorough (plan + implement + audit + review).

**The full flow:**
1. Scans all skills and agents
2. Chain-planner builds a chain from your description or shows a menu
3. Each step gets a model (agent model or default)
4. Confirm gate shows the chain, you approve
5. Router launches steps in sequence with their assigned models
6. Micro-loops handle coder -> audit -> fix cycles when needed

### Use a skill directly

```
/skill:<skill-name> <task>
```

Examples:
- `/skill:architect design the user authentication system`
- `/skill:research "transformer architectures" --sources=arxiv,github`
- `/skill:create-skill a skill for reviewing SQL queries`

Direct invocation runs with pi's default model. For model-pinned execution,
use the orchestrator or create an agent.

### Use an agent directly

```
run as <agent-name> <task>
```

Examples:
- `run as gitops-expert and audit our Kubernetes cluster`

Agents can declare a preferred model in their frontmatter. When invoked via
`run as`, that model is used. When the orchestrator selects an agent for a
chain step, it uses the agent's model.

---

## Structure

### Skills

All skills live in `skills/<name>/SKILL.md`. Each has YAML frontmatter with
`name` and `description`. Skills are auto-discovered by pi and available via
`/skill:<name>`.

Skill types:
- **Graph** — defines a multi-node workflow with triggers, routes, and
  sub-agent roles. The orchestrator registers its nodes dynamically.
- **Methodology** — provides step-by-step instructions passed to a single
  sub-agent. No multi-agent orchestration.
- **Data provider** — provides bash scripts (e.g., `stock-info`) used by other
  skills as dependencies.

| Skill | Type | Purpose |
|-------|------|---------|
| orchestrator | Graph (meta) | Master state machine — discovers skills + agents, chain-planner, routes through graphs |
| architect | Methodology | Architectural design with codebase analysis, ADRs, and plans |
| better-products-habits | Methodology | Hiten Shah's 5 habits for product building |
| code-review | Methodology | Rigorous code review (security, performance, maintainability) |
| create-skill | Graph | Create new skills with research, synthesis, planning, and writing |
| financial-analysis | Graph | Multi-methodology analysis (DCF via Lyn Alden, GARP via Lynch, antifragility via Taleb) |
| git-workflow-and-versioning | Methodology | Branching, versioning, changelogs, and release conventions |
| lyn-alden-dcf | Methodology | DCF valuation reference (Lyn Alden methodology) |
| nassim-nicholas-taleb | Methodology | Antifragility / black swan / via negativa critique |
| peter-lynch | Methodology | GARP/value analysis reference (Peter Lynch methodology) |
| research | Methodology | Multi-source parallel search across arxiv, github, pubmed, archive, web |
| setup-testing-workflows | Methodology | GitHub Actions test workflow generator |
| sre | Methodology | Security & reliability audit (4-phase pipeline) |
| stock-info | Data provider | yfinance data provider for all analysis skills |
| update-readme | Methodology | Scan and reconcile README.md |
| writing-plans | Methodology | Implementation plan writer |

### Agents

Agent definitions in `agents/<name>.md`. The orchestrator scans these and
prefers agents over raw skills when a match is found. An agent can declare
`skills` (which skills it wraps), `model` (preferred model), and `tools`
(what tools the agent needs).

| Agent | Wraps skills | Model | Tools | Purpose |
|-------|-------------|-------|-------|---------|
| `gitops-expert` | sre, code-review | haiku | Read, Write, Bash, Grep, WebSearch | GitOps audit (ArgoCD/Flux) |
| `reviewer.md` | — | — | — | Code review orchestrator (invokes multiple auditors) |
| `shared-workflow.md` | — | — | — | Cross-agent collaboration rules |

### Other

| Path | Purpose |
|------|---------|
| `docs/plans/` | Implementation plans (read-only) |
| `docs/decisions/` | Architecture Decision Records (ADRs) |
| `work/` | Ephemeral artifacts (graph state, outputs) |
| `work/graph/state.json` | Shared state — the single source of truth for the graph engine |

---

## Graph engine architecture

The orchestrator is a state router, not a puppeteer. It reads a shared state
object at `work/graph/state.json`, selects the next node to execute, launches
it, and writes the result back.

Key concepts:
- **Decomposer** — scans skills + agents, builds skill_index and agent_index
- **Chain-planner** — builds chains from your description or shows a menu.
  Each step gets a model assignment. Agent steps use the agent's frontmatter
  model.
- **Nodes** — autonomous units (chain-planner, confirm, coder, human_input,
  consolidator) that each handle one task
- **Router** — pure function that reads state and returns the next node
- **Micro-loop** — coder -> audit -> coder loop runs autonomously until
  the iteration counter hits max_iterations
- **Confirm gate** — shows the chain with model assignments, you approve/modify
- **Model routing** — the chain-planner assigns models per step, the
  orchestrator enforces them when launching sub-agents. Agent models take
  precedence over defaults.

## Adding a skill

Use the create-skill workflow:

```
/skill:create-skill <description>
```

Or manually create `skills/<name>/SKILL.md` with YAML frontmatter and a
`## Graph` or `## Overview` section. See `skills/orchestrator/SKILL.md`
for the complete node format.

## Adding an agent

Create `agents/<name>.md` with YAML frontmatter:

```yaml
---
name: my-agent
description: > What this agent does
skills: [skill1, skill2]  # skills this agent wraps
model: haiku              # preferred model when used via orchestrator
tools: Read, Write, Bash  # tools the agent needs
---
```

The orchestrator reads the `tools` field and maps it to the appropriate
subagent type at launch. If the agent needs web search or external APIs,
include `WebSearch` or `WebFetch` in `tools`.

The orchestrator's chain-planner prefers this agent over raw skills when
a request matches its description or its wrapped skills.

## Updating this README

```
/skill:update-readme
```