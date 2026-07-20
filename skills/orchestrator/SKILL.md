---
name: orchestrator
description: >
  Graph-engine orchestrator for the fleet-management project. Routes work
  through a data-driven state machine. No hardcoded node types — skills
  register their own graph nodes dynamically. Generic router, not a
  software-engineering pipeline.
---

# Orchestrator — Generic Graph Engine

## Overview

The orchestrator is a **state router**: it reads shared state, selects the next
node to execute based on routing rules, launches sub-agents for execution nodes,
and writes results back. It does not own the logic — it only follows transitions.

**What makes this generic (not code-specific):**
- No built-in "coder" or "security-reviewer" or "test-auditor" node types
- Chain templates use step *roles* (work, review, plan, fix) resolved to actual
  skills at build time
- Graph skills register their own nodes dynamically — the orchestrator doesn't
  care what they do
- The router follows whatever nodes are registered, not a hardcoded priority list

**Announce at start:** "I'm using the graph engine to route this through the state machine."

### Flow

```
User request → decomposer → chain-planner (user picks a chain)
  → confirm (user approves) → execute nodes (dynamically registered) → consolidate
```

The chain-planner is mandatory on every invocation. Even for a one-line fix,
you see available chain options and pick one.

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
   │ chain-   │  │confirm │ │exec  │ │ graph │ │human_    │
   │ planner  │  │(gate)  │ │nodes │ │skill  │ │input     │
   └─────┬────┘  └───┬────┘ │      │ │nodes  │ └────┬─────┘
         │           │      └──────┘ └───────┘      │
         └───────────┴────────────┬─────────────────┘
                                  ▼
                           ┌──────────────┐
                           │ consolidator │
                           └──────────────┘
```

"Exec nodes" are dynamically registered per chain step — methodology skills,
agents, or generic executors.
"Graph skill nodes" are registered from a skill's `## Graph` section.

### Key properties

- **State router, not puppeteer.** The orchestrator never copies text between
  agents. Nodes write to shared state; the next node reads from it.
- **Chain planner before confirm gate.** You pick a skill chain first, then
  confirm the detailed plan.
- **No hardcoded node types.** coder, security-reviewer, test-auditor do not
  exist. Every execution node is dynamically registered from chain steps or
  skill graphs.
- **Orchestration nodes are inline.** decomposer, chain-planner, confirm, and
  consolidator run in your (the orchestrator's) main context.
- **Execution nodes are sub-agents.** Any dynamically registered node that does
  real work runs as an isolated sub-agent for token separation.
- **Graph skill nodes are first-class.** When a chain step references a graph
  skill (e.g., create-skill, research), all its nodes are registered in the
  state machine and routed through like built-in nodes.
- **Micro-loops are chain-driven.** Review → fix → re-review is encoded in
  chain step types, not in hardcoded node names. The fix step is a re-run of
  the work step with review feedback injected.

---

## 1. Shared State

The shared state lives at `work/graph/state.json` and is the single source of
truth. The orchestrator creates it on first invocation.

**Schema:** See `skills/orchestrator/schema.json` for the full JSON structure.

### Status values

| Status | Meaning |
|--------|---------|
| `START` | Initial state. |
| `DECOMPOSING` | Breaking request into tasks. |
| `CHAINING` | Building chain proposals. |
| `CONFIRM` | Waiting for user approval. |
| `EXECUTING` | One or more execution nodes active. |
| `HUMAN_REVIEW` | Waiting for user input (paused). |
| `ERROR` | Unrecoverable error. |
| `COMPLETE` | Work finished. |

---

## 2. Nodes

Nodes are either **inline** or **sub-agent**. The orchestrator handles both.

### Built-in nodes (always present)

| Node | Type | Purpose |
|------|------|---------|
| `decomposer` | inline | Index skills/agents, decompose user request |
| `chain-planner` | inline | Build chain proposals, get user choice |
| `confirm` | inline | Activate selected chain, get user approval |
| `human_input` | inline | Pause for user escalation or modification |
| `consolidator` | inline | Read all output, present final results |

### Dynamically registered nodes (per chain step)

When the confirm node activates a chain, it registers nodes based on each
step's type. These join the state machine alongside the built-in nodes.

**Step types and their node registration:**

| Step type | Registration |
|-----------|-------------|
| `skill` (methodology) | One node named `<step-index>-<skill-name>`. Sub-agent reads the skill's SKILL.md and executes it. |
| `skill` (graph) | All nodes from the skill's `## Graph` section, prefixed with `<step-index>-<skill-name>.`. Each is registered with its defined trigger, role, skills, output, and route. |
| `agent` | One node named `<step-index>-<agent-name>`. Sub-agent reads the agent's brain.md and runs with its configured model and tools. |
| `fix` | One node named `<step-index>-fix`. Sub-agent receives the preceding work step's output plus review feedback, re-does the work. |
| `plan` | One node named `<step-index>-plan`. Sub-agent reads the planning skill and produces a plan. |

**Node naming convention:** Dynamic nodes are named `<step-index>-<label>`
(e.g., `1-research`, `2-code-review`, `3-create-skill.source-validator`).
This prevents collisions when multiple skills are in the same chain.

**Rule of thumb for inline vs sub-agent:**
- If the node produces user-facing output or makes routing decisions — inline
- If the node does isolated work with its own methodology — sub-agent

---

### Node: `decomposer` (inline)

**Trigger:** `state.status == "START"` OR `state.routing.next_node == "decomposer"`

**Input:** `state.user_request`

**Behavior:** Run this inline — do not launch a sub-agent.

1. Scan `skills/*/SKILL.md` — read frontmatter (`name`, `description`). For
   graph skills, also read their `## Graph` nodes list.
2. Build a `skill_index`: each entry has `name`, `description`,
   `type` (graph|methodology), `nodes` (list of node names if graph), and
   `produces` (what outputs the skill generates, inferred from its graph
   output paths).
3. Scan `agents/*.md` — read frontmatter (`name`, `description`, `skills`,
   `model`, `tools`).
4. Build an `agent_index`: each entry has `name`, `description`, `skills`,
   `model`, and `tools`.
5. Match the user request against skill names/descriptions and agent
   names/descriptions.
6. Decompose the request into tasks, assign each task to a node.

**Output (writes to state):** See `skills/orchestrator/examples/decomposer-output.md`
for the full format.

**Routing:** Always -> `chain-planner`

---

### Node: `chain-planner` (inline)

**Trigger:** `state.routing.next_node == "chain-planner"`

**Mandatory.** Runs on every invocation. You see chain options before any
work starts.

**Input:** `state.user_request`, `state.decomposition.tasks`,
`state.skill_index`, `state.agent_index`

**Behavior:** Run this inline — do not launch a sub-agent.

1. Set `state.status = "CHAINING"`.
2. Build chain proposals directly.

#### Step A: Check if the user already described a chain

Scan the user's request for chain language:
- Sequential connectors: "first... then", "next", "after that", "and then"
- Ordered lists: "1." "2." "3.", "step 1" "step 2"
- Explicit skill or agent names (matched against both indices)

**If chain language is detected:**
- Parse into individual steps. Each connector-separated clause is one step.
- For each step, match against `agent_index` first, then `skill_index`:
  - **Agent match (highest priority):** Exact name match. Use the agent's
    `skills` list and `model`. Step type becomes `"agent"`.
  - **Skill match:** Name match, description keyword match, or task verb match.
  - **Agent fallback by skill:** If no agent matched by name, check if any
    agent lists the matched skill in its `skills` field. If yes, prefer the agent.
  - If no match: step type becomes `"work"` (generic executor, model: default).
- Build **exactly as described**. No collapsing, dedup, or reordering.
  Add warnings as notes.
- Add a `consolidator` step at the end if not already present.
- Assign models per step — agent frontmatter model takes precedence.
- Show as a single resolved chain — **no menu.**

**See `skills/orchestrator/examples/chain-proposal-described.md` for output format.**

#### Step B: No chain language detected — show menu

Show standard chains built dynamically from the indices. The templates use
step *roles* resolved to actual skills at build time:

**Step roles and resolution:**

| Role | Resolution |
|------|-----------|
| `work` | The primary skill(s) matched to the user's request |
| `review` | Scan skill_index for skills whose name/description matches "review", "audit", "sre", "inspect", "check". Prefer the best description match relative to `work`. If none found, skip with a note. |
| `plan` | Scan skill_index for skills whose name/description matches "architect", "strategy", "plan", "design". If none found, skip with a note. |
| `fix` | Special step type. Re-runs the `work` step with review feedback injected. Always paired with a preceding `review` step. |

**Template chains:**

- **Fast** — `work` -> consolidator
- **Safe** — `work` -> `review` -> `fix` -> consolidator
- **Thorough** — `plan` -> `work` -> `review` -> `fix` -> consolidator

If `plan` or `review` roles cannot be resolved to a real skill, those steps
are dropped with a note to the user.

If an agent matches the request, use it instead of the raw skill for the
`work` role.

**See `skills/orchestrator/examples/chain-proposal-menu.md` for output format.**

#### Model assignment per step

| Step role | Model |
|-----------|-------|
| plan, architecture | `sonnet` |
| work, execution (code-adjacent) | `default` |
| work, execution (research, analysis) | `haiku` |
| review, audit | `haiku` |
| fix | `sonnet` |
| no clear type | `default` |

**Agent override:** Agent's frontmatter `model` takes precedence over the table.

#### Wait and write

3. Present the chain options to the user directly (not via sub-agent).
   Wait for their choice.
4. Write the selected chain to state.json.

**Output (writes to state):**
```json
{
  "status": "CHAINING",
  "chains": [
    {
      "name": "Safe",
      "description": "Work + review + fix",
      "steps": [
        { "type": "skill", "name": "research", "model": "haiku",
          "role": "work" },
        { "type": "skill", "name": "code-review", "model": "haiku",
          "role": "review", "note": "Resolved from skill_index" },
        { "type": "node", "name": "fix", "model": "sonnet",
          "role": "fix" },
        { "type": "node", "name": "consolidator", "model": "default" }
      ]
    }
  ],
  "selected_chain": 0,
  "routing": { "last_node": "chain-planner", "next_node": "confirm",
    "reason": "chain selected" }
}
```

**Step fields:** `type` (skill|agent|node), `name` (skill/agent name or
generic role), `model`, `role` (work|review|fix|plan), optional `tools`,
`skills`, `note`.

**Routing:** Always -> `confirm`. If user aborts -> consolidator.

**Edge cases:**
- **Partial steps:** Build described steps + Fast-style defaults for the rest.
- **No skills or agents matched:** Build a single generic `work` step (executor).
- **Unmatched step:** Leave as generic `work`, note to user.
- **Agent with empty skills field:** Use agent without referencing a specific skill.
- **Multiple agents match:** Prefer the most specific description. If ambiguous,
  list as options.
- **Review step but no review skill found:** Drop the review and fix steps,
  note to user.

---

### Node: `confirm` (inline)

**Trigger:** `state.routing.next_node == "confirm"`

**Mandatory approval gate.**

**Input:** `state.user_request`, `state.decomposition`, `state.chains`,
`state.selected_chain`, `state.selected_chain_steps`, `state.skill_index`,
`state.agent_index`, `state.nodes`

**Behavior:** Run this inline — do not launch a sub-agent.

1. Set `state.status = "CONFIRM"`.
2. Read the selected chain (`state.chains[state.selected_chain]`).
3. Activate nodes from chain steps. For each step in order:

   **If step type is `"skill"` and the skill has a `## Graph` section:**
   - Read the skill's `## Graph` section
   - Register each of its nodes in state, prefixing names with
     `<step-index>-<skill-name>.`
   - Use each node's defined `trigger`, `role`, `skills`, `output`, `route`
   - Set the first node in the graph to `"ready"`
   - Store the graph's internal routing rules so the router can follow them

   **If step type is `"skill"` (methodology — no graph):**
   - Register one node named `<step-index>-<skill-name>`
   - Set its status to `"ready"`
   - Store its route: after completion, route to the next chain step

   **If step type is `"agent"`:**
   - Register one node named `<step-index>-<agent-name>`
   - Set its status to `"ready"`

   **If step type is `"node"` (generic role like `fix` or `consolidator`):**
   - Register one node named `<step-index>-<role>`
   - If role is `"fix"`: set status to `"pending"` (activated when preceding
     review step completes)
   - If role is `"consolidator"`: set status to `"pending"` (always last)
   - Otherwise: set status to `"ready"`

4. Present the plan to the user directly (not via sub-agent).
   **See `skills/orchestrator/examples/confirm-gate.md` for output format.**

**Routing:** "proceed" -> first ready node. "change chain" -> route to
chain-planner. "modify tasks" / "add nodes" -> route to human_input.
"abort" -> consolidator.

**Node activation detail for graph skills:**

When activating a graph skill's nodes, create a mapping entry so the router
can resolve graph-internal routing:

```json
{
  "_graph_routes": {
    "<step-index>-<skill-name>": {
      "entry": "<first-node-name>",
      "routes": [
        { "from": "<node-a>", "condition": "always", "to": "<node-b>" }
      ],
      "sink": "<last-node-name>",
      "chain_exit": "<next-step-index>"
    }
  }
}
```

When the last node of a graph skill completes, the router routes to the next
step in the chain (the `chain_exit` target).

---

### Node: `human_input` (inline)

**Trigger:** `state.routing.next_node == "human_input"`

**Pauses the graph** for error escalation, plan modification, or chain re-route.

**Behavior:** Present context, wait for response, write to
`state.nodes.human_input`.

**Routing:**
- "continue" -> reset counter, re-route to the node that triggered the pause
- "skip" / "abort" -> consolidator
- Plan modification -> re-run decomposer -> chain-planner
- Chain re-route -> chain-planner

---

### Node: `consolidator` (inline)

**Trigger:** `state.routing.next_node == "consolidator"`

**Input:** `state.nodes`, `state.graph_errors`, `state.iteration_count`,
`state.decomposition`

**Behavior:** Run this inline — do not launch a sub-agent.

Read all output from `work/graph/output/*/`. Merge findings, note any
conflicts or unresolved errors. Set `state.status = "COMPLETE"`. Present
the final results to the user directly.

**Routing:** Terminal. No further routing.

---

## 3. Router

The router is `f(state) -> next_node`. Called after every node completes.

```
function get_next_node(state):
    if state.status in ["COMPLETE", "ERROR"]: return None
    if state.nodes.human_input.status == "responded": return route_from_human(state)
    if state.routing.next_node: return state.routing.next_node

    # 1. Check dynamically registered nodes (execution nodes)
    for each name, node in state.nodes:
        if name starts with "_": continue  # skip metadata keys
        if node.status == "ready": return name

    # 2. Check if a graph skill's last node just completed
    active_graph = state._graph_routes
    if active_graph:
        for graph_key, graph_info in active_graph.items():
            if graph_info.get("current_node") == graph_info.get("sink"):
                chain_exit = graph_info.get("chain_exit")
                if chain_exit:
                    return chain_exit
                break

    # 3. Fall through to consolidator
    return "consolidator"
```

### Priority

1. `human_input` (highest — always checked first)
2. Dynamically registered execution nodes (any status == "ready")
3. Graph skill internal routing (node-to-node within a graph)
4. Chain step progression (graph finished -> next step in chain)
5. `consolidator` (always last)

### Micro-loop (chain-driven)

Micro-loops are encoded in the chain structure, not in hardcoded node names.
A chain step with `role: "fix"` is a re-run of the preceding work step with
review feedback injected. The router handles this by:

1. When a review step completes with findings, the `fix` step is set to
   `"ready"`
2. The `fix` step receives: the original work output + the review findings
3. When the `fix` step completes, the review step is re-set to `"ready"`
   (up to `max_iterations` times)
4. After `max_iterations` or when review finds no issues, the chain proceeds

```
work -> review -> (has issues? -> fix -> re-run review)
               -> (no issues?  -> consolidator)
```

The router increments an iteration counter per work/review pair, not
globally. Max 5 iterations per pair, then escalates to `human_input`.

---

## 4. Node Execution

Nodes execute in one of two ways depending on their type.

### Inline nodes (built-in orchestration)

You execute these directly in your main context. No `Agent` tool call.
Steps:
1. Read the relevant state slice from `work/graph/state.json`
2. Execute the behavior described in the node definition
3. Write any output to the specified path in `work/graph/`
4. Set `state.routing` to route to the next node
5. Update `state` by writing back to `work/graph/state.json`

### Sub-agent nodes (dynamically registered execution nodes)

These are launched as sub-agents for token isolation.

### Model resolution

```
function resolve_model(state, node_name):
    chain = state.chains[state.selected_chain]
    for each step in chain.steps:
        if step.type == "skill" AND step.name matches node_name:
            return step.model
        if step.type == "agent" AND step.name matches node_name:
            return step.model
        if step.type == "node" AND step.role matches node_name:
            return step.model
    return "default"
```

### Launch procedure (sub-agent nodes only)

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
    if contains "WebSearch", "WebFetch", or anything beyond
        Read/Write/Bash/Grep:
        return "general-purpose"
    if tools subset of ["Read", "Write", "Bash", "Grep", "Edit", "LS",
        "Glob"]:
        return "Explore"
    return "general-purpose"
```

This is the only pi-specific mapping in the system. Agent frontmatter is
agnostic.

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
| Sub-agent writes malformed output | Log to `graph_errors`, re-launch sub-agent. |
| Sub-agent goes off-task | `steer_subagent` to redirect. Fails -> kill and re-launch. |
| Inline node encounters an error | Log to `graph_errors`, set `status = "ERROR"`, route to `human_input`. |
| State file missing | Re-initialize. Warn user. |
| Circular routing (same node 3x) | Force route to `human_input`. |
| No valid next node | Set `ERROR`, route to `human_input`. |
| Graph skill node not found in state | Log error, treat graph step as complete, route to next chain step. |

Recovery: write to `work/graph/errors.log`, set `status = "ERROR"`, route
to `human_input`. User can reset, skip, or abort.

---

## 6. Output Structure

```
work/graph/
├── state.json              # Shared state
├── errors.log              # Graph-level errors
├── output/
│   ├── <step-index>-<node-name>/   # One directory per execution node
│   └── consolidator/               # Final results
```

---

## 7. Adding a New Skill (Graph Nodes)

Skills define their own graph nodes in the `## Graph` section of their
SKILL.md. The orchestrator auto-discovers them. No orchestrator changes
needed.

Each skill graph node must define:

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Unique node identifier within the skill | `source-validator` |
| `trigger` | When the node activates | `route("query-refiner")` |
| `input` | State fields it needs | `[user_request]` |
| `role` | Sub-agent role prompt | `You are a research specialist...` |
| `skills` | Skills the sub-agent can reference | `[]` |
| `output` | Where it writes results | `work/research/sources/arxiv.md` |
| `route` | Where to route next | `always -> synthesis-writer` |

These are registered dynamically when the skill is referenced in a chain.

---

## 8. Adding a New Built-in Node (rare)

Only needed if you want a new node that is always present in every graph
run (e.g., a new orchestration step). Most new nodes should be added as
skill graph nodes, not built-in nodes.

1. Decide if it should be inline or sub-agent:
   - **Inline:** if it makes routing decisions, presents output to the user,
     or does trivial state transitions
   - **Sub-agent:** if it executes an isolated methodology
2. Add its entry to the `nodes` object in `schema.json`
3. Define it in section 2: trigger, input, behavior, output fields, routing
4. The router will find it automatically (it scans all nodes for `"ready"`
   status)
