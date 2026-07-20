---
name: orchestrator
description: >
  Graph-engine orchestrator for the fleet-management project. Routes work
  through a data-driven state machine with autonomous nodes, micro-loops,
  and local human-in-the-loop interaction. No central manager — the
  shared state drives all transitions.
---

# Orchestrator — Graph Engine (State Machine Router)

## Overview

The orchestrator is a **state router**: it reads a shared state object, selects the next node to execute based on routing rules, launches that node, and writes the result back. The state machine runs autonomously — the orchestrator does not own the logic, it only follows transitions.

**Announce at start:** "I'm using the graph engine to route this through the state machine."

### Flow

```
User request → decomposer → chain-planner (user picks a chain)
  → confirm (user approves) → execute nodes → consolidate
```

The chain-planner is mandatory on every invocation. Even for a one-line fix, you see the available skill chains and pick one.

### Architecture

```
                    ┌──────────────────────────┐
                    │     SHARED STATE         │
                    │  work/graph/state.json   │
                    │  status, chains, nodes{} │
                    └──────────┬───────────────┘
                               │
                   ┌───────────┴───────────┐
                   │        ROUTER         │
                   │  f(state) -> next     │
                   └───────────┬───────────┘
                               │
          ┌──────────┬─────────┼─────────┬──────────┐
          ▼          ▼         ▼         ▼          ▼
   ┌──────────┐  ┌────────┐ ┌──────┐ ┌───────┐ ┌──────────┐
   │ chain-   │  │confirm │ │coder │ │audit  │ │human_    │
   │ planner  │  │(gate)  │ │      │ │nodes* │ │input     │
   └─────┬────┘  └───┬────┘ └──┬───┘ └───┬───┘ └────┬─────┘
         │           │         │         │          │
         └───────────┴─────────┴─────────┴──────────┘
                                     │
                                     ▼
                              ┌──────────────┐
                              │ consolidator │
                              └──────────────┘
```

*Audit nodes: security-reviewer, test-auditor (configurable, defined by chain)

### Key properties

- **State router, not puppeteer.** The orchestrator never copies text between agents. Nodes write to shared state; the next node reads from it. The state is the conduit.
- **Chain planner before confirm gate.** You pick a skill chain first. Then the confirm gate shows the detailed plan for that chain.
- **Token isolation.** Every sub-agent gets `inherit_context: false` and only the relevant slice of shared state — never the full state or other agents' history.
- **Autonomous micro-loops.** coder -> audit -> (fail -> coder) loops with an iteration counter. Max 5 iterations, then escalates to human.

---

## 1. Shared State

The shared state lives at `work/graph/state.json` and is the single source of truth. Every node reads from it, executes, writes back. The orchestrator creates it on first invocation.

**Schema:** See `skills/orchestrator/schema.json` for the full JSON structure.

### Status values

| Status | Meaning |
|--------|---------|
| `START` | Initial state. |
| `DECOMPOSING` | Breaking request into tasks. |
| `CHAINING` | Building chain proposals. |
| `CONFIRM` | Waiting for user approval. |
| `CODING` | Coder node active. |
| `REVIEWING` | Audit node active. |
| `HUMAN_REVIEW` | Waiting for user input (paused). |
| `ERROR` | Unrecoverable error. |
| `READY` | All nodes complete. |
| `COMPLETE` | Work finished. |

---

## 2. Nodes

Each node is an autonomous sub-agent. The orchestrator reads the relevant state slice, constructs a prompt, launches the sub-agent with `inherit_context: false`, reads its output, writes to state, and routes.

### Node: `decomposer`

**Trigger:** `state.status == "START"` OR `state.routing.next_node == "decomposer"`

**Input:** `state.user_request`

**Behavior:**
1. Scan `skills/*/SKILL.md` — read frontmatter (`name`, `description`). For graph skills, also read their `## Graph` nodes list.
2. Build a `skill_index`: each entry has `name`, `description`, `type` (graph|methodology), `nodes` (list of node names if graph), and `produces` (what outputs the skill generates, inferred from its graph output paths).
3. Scan `agents/*.md` — read frontmatter (`name`, `description`, `skills`, `model`, `tools`).
4. Build an `agent_index`: each entry has `name`, `description`, `skills`, `model`, and `tools`.
5. Match the user request against skill names/descriptions and agent names/descriptions.
6. Decompose the request into tasks, assign each task to a node.

**Output (writes to state):** See `skills/orchestrator/examples/decomposer-output.md` for the full format.

**Routing:** Always -> `chain-planner`

---

### Node: `chain-planner`

**Trigger:** `state.routing.next_node == "chain-planner"`

**Mandatory.** Runs on every invocation. You see chain options before any work starts.

**Input:** `state.user_request`, `state.decomposition.tasks`, `state.skill_index`, `state.agent_index`

**Behavior:**

1. Set `state.status = "CHAINING"`.
2. Build chain proposals.

### Step A: Check if the user already described a chain

Scan the user's request for chain language:
- Sequential connectors: "first... then", "next", "after that", "and then"
- Ordered lists: "1." "2." "3.", "step 1" "step 2"
- Explicit skill or agent names (matched against both indices)

**If chain language is detected:**
- Parse into individual steps. Each connector-separated clause is one step.
- For each step, match against `agent_index` first, then `skill_index`:
  - **Agent match (highest priority):** Exact name match. Use the agent's `skills` list and `model`. Step type becomes `"agent"`.
  - **Skill match:** Name match, description keyword match, or task verb match.
  - **Agent fallback by skill:** If no agent matched by name, check if any agent lists the matched skill in its `skills` field. If yes, prefer the agent.
  - If no match: treat as a generic `coder` task.
- Build **exactly as described**. No collapsing, dedup, or reordering. Add warnings as notes.
- Add a `consolidator` step at the end if not already present.
- Assign models per step — agent frontmatter model takes precedence.
- Show as a single resolved chain — **no menu.**

**See `skills/orchestrator/examples/chain-proposal-described.md` for output format.**

### Step B: No chain language detected — show menu

Show standard chains built dynamically from the indices:

- **Fast** — matched skill (or agent) -> consolidator
- **Safe** — matched skill -> code-review -> fix issues -> consolidator
- **Thorough** — architect -> matched skill -> sre -> code-review -> fix issues -> consolidator

If an agent matches the request, use it instead of the raw skill. If none fit, the user can rephrase with "first X then Y".

**See `skills/orchestrator/examples/chain-proposal-menu.md` for output format.**

### Model assignment per step

| Step type | Model |
|-----------|-------|
| architect, planning, ADR writing | `sonnet` |
| coding, implementation | `default` |
| review, audit, research | `haiku` |
| fix review issues | `sonnet` |
| no clear type | `default` |

**Agent override:** Agent's frontmatter `model` takes precedence over the table.

### Wait and write

3. Wait for user response. Set `selected_chain` accordingly.

**Output (writes to state):**
```json
{
  "status": "CHAINING",
  "chains": [
    { "name": "Custom", "description": "User-described chain",
      "steps": [
        { "type": "skill", "name": "architect", "model": "sonnet" },
        { "type": "agent", "name": "gitops-expert", "model": "haiku",
          "tools": ["Read", "Write", "Bash", "Grep", "WebSearch"],
          "skills": ["sre", "code-review"] },
        { "type": "node", "name": "coder", "model": "default" },
        { "type": "node", "name": "consolidator", "model": "default" }
      ]
    }
  ],
  "selected_chain": 0,
  "routing": { "last_node": "chain-planner", "next_node": "confirm", "reason": "chain resolved from description" }
}
```

**Agent step fields:** `type`, `name`, `model`, `tools` (mapped to subagent type at launch), `skills`.

**Routing:** Always -> `confirm`. If user aborts -> consolidator.

**Edge cases:**
- **Partial steps:** Build described steps + Fast-style defaults for the rest.
- **No skills or agents matched:** Build around generic nodes (coder, human_input, consolidator).
- **Unmatched step:** Leave as generic `coder`, note to user.
- **Agent with empty skills field:** Use agent without referencing a specific skill.
- **Multiple agents match:** Prefer the most specific description. If ambiguous, list as options.

---

### Node: `confirm`

**Trigger:** `state.routing.next_node == "confirm"`

**Mandatory approval gate.**

**Input:** `state.user_request`, `state.decomposition`, `state.chains`, `state.selected_chain`, `state.skill_index`, `state.agent_index`, `state.nodes`

**Behavior:**
1. Set `state.status = "CONFIRM"`.
2. Read the selected chain.
3. Activate nodes from chain steps (skill -> graph nodes ready, agent -> coder ready with agent context, node -> built-in node ready, fix -> coder with dependencies).
4. Present the plan. **See `skills/orchestrator/examples/confirm-gate.md` for the output format.**

**Routing:** "proceed" -> first ready node. "change chain" -> route to chain-planner. "modify tasks" / "add nodes" -> route to human_input. "abort" -> consolidator.

---

### Node: `coder`

**Trigger:** `state.nodes.coder.status == "ready"`

**Input:** `state.user_request`, relevant `decomposition.tasks`, `state.iteration_count`, `state.graph_errors`

**Behavior:** Execute tasks using referenced skill methodology. Write to `work/graph/output/coder/`.

**Routing:** If ready audit nodes exist -> route by priority (security-reviewer > test-auditor). Else -> consolidator.

---

### Node: `security-reviewer`

**Trigger:** `state.nodes["security-reviewer"].status == "ready"`

**Input:** relevant tasks, `coder.output_summary`, `state.graph_errors`

**Behavior:** Audit for OWASP issues, secrets, auth weaknesses. Write to `work/graph/output/security-review/`. Append errors to `graph_errors`.

**Routing:** If errors found AND `iter < max` -> back to coder (micro-loop). If maxed -> human_input. Else -> consolidator or next audit node.

---

### Node: `test-auditor`

Same structure as security-reviewer. Checks test coverage, edge cases. Identical routing.

---

### Node: `human_input`

**Trigger:** `state.routing.next_node == "human_input"`

**Pauses the graph** for error escalation, plan modification, or chain re-route.

**Behavior:** Present context, wait for response, write to `state.nodes.human_input`.

**Routing:** "continue" -> reset counter, route to coder. "skip"/"abort" -> consolidator. Plan modification -> re-run decomposer -> chain-planner. Chain re-route -> chain-planner.

---

### Node: `consolidator`

**Trigger:** `state.routing.next_node == "consolidator"`

**Input:** `state.nodes`, `state.graph_errors`, `state.iteration_count`, `state.decomposition`

**Behavior:** Read all output from `work/graph/output/*/`. Merge findings, note conflicts and unresolved errors. Set `state.status = "COMPLETE"`.

**Routing:** Terminal. Present results.

---

## 3. Router

The router is `f(state) -> next_node`. Called after every node completes.

```
function get_next_node(state):
    if state.status in ["COMPLETE", "ERROR"]: return None
    if state.nodes.human_input.status == "responded": return route_from_human(state)
    if state.routing.next_node: return state.routing.next_node
    for each name, node in state.nodes:
        if node.status == "ready": return name
    return "consolidator"
```

### Priority

1. `human_input` (highest)
2. `chain-planner`
3. `coder`
4. `security-reviewer`
5. `test-auditor`
6. `consolidator` (always last)

### Micro-loop rule

```
coder -> audit -> errors AND iter < max -> coder (inc iter)
                -> errors AND iter >= max -> human_input
                -> no errors -> consolidator
```

The router increments the counter, not the node.

---

## 4. Node Launch

The orchestrator launches every node as a sub-agent. The model is determined by the chain step.

### Model resolution

```
function resolve_model(state, node_name):
    chain = state.chains[state.selected_chain]
    for each step in chain.steps:
        if step.type == "node" AND step.name == node_name: return step.model
        if step.type == "skill" AND step.name == <skill whose graph contains this node>: return step.model
    return "default"
```

### Launch procedure

1. Read relevant state slice (only fields the node needs)
2. Resolve model via `resolve_model(state, node_name)`
3. Construct prompt with: role, input data, skill references, output path
4. Launch sub-agent with `inherit_context: false` and the resolved model
5. Read output, write to state, call router

### Agent steps vs skill steps

When `type: "agent"`:
- Read `agents/<name>.md`, use its full content as the sub-agent prompt
- Use the agent's `model` from frontmatter
- Use the agent's `tools` to determine subagent_type:

```
function resolve_subagent_type(tools):
    if not tools or tools is empty: return "general-purpose"
    if contains "WebSearch", "WebFetch", or anything beyond Read/Write/Bash/Grep:
        return "general-purpose"
    if tools subset of ["Read", "Write", "Bash", "Grep", "Edit", "LS", "Glob"]:
        return "Explore"
    return "general-purpose"
```

This is the only pi-specific mapping in the system. Agent frontmatter is agnostic.

When `type: "skill"`, use the standard prompt template.

### Prompt template (skill steps)

```
You are [ROLE]

Task: [specific task]

Input data:
[only the fields this node needs — never the full state]

Skills available:
- skills/<name>/SKILL.md — read before starting

Tools: Read, Write, Edit, Bash, Grep

Steps:
1. ...
2. Write output to [path]
3. Return one-line summary

Constraints:
- No conversation history from other agents
- Write output to path, return summary
```

---

## 5. Error Handling

| Situation | Action |
|-----------|--------|
| Sub-agent fails/times out | Re-launch once. Fail twice -> `ERROR`, route to `human_input`. |
| Node writes malformed output | Log to `graph_errors`, re-launch. |
| Node goes off-task | `steer_subagent` to redirect. Fails -> kill and re-launch. |
| State file missing | Re-initialize. Warn user. |
| Circular routing (same node 3x) | Force route to `human_input`. |
| No valid next node | Set `ERROR`, route to `human_input`. |

Recovery: write to `work/graph/errors.log`, set `status = "ERROR"`, route to `human_input`. User can reset, skip, or abort.

---

## 6. Output Structure

```
work/graph/
├── state.json              # Shared state
├── errors.log              # Graph-level errors
├── output/
│   ├── coder/
│   ├── security-review/
│   ├── test-audit/
│   └── consolidator/
```

---

## 7. Adding a New Built-in Node

To add a new node (e.g., `performance-auditor`):
1. Add its entry to the `nodes` object in `schema.json`
2. Define it in section 2: trigger, input, behavior, output fields, routing
3. Add it to the router's priority list
4. Add edges in the routing rules
