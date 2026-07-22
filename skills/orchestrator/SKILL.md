---
name: orchestrator
description: >
  Graph-engine orchestrator for the fleet-management project. Routes work
  through a data-driven state machine. No hardcoded node types — skills
  register their own graph nodes dynamically. Dynamic graph-planner node
  designs a custom topology per request: decomposes into parallel tasks,
  selects agents/skills, routes with verifiers and barriers.
---

# Orchestrator — Generic Graph Engine

## Overview

The orchestrator is a **state router**: it reads shared state, selects the next
node to execute based on routing rules, launches sub-agents for execution nodes,
and writes results back. It does not own the logic — it only follows transitions.

**What makes this generic (not code-specific):**
- No built-in "coder" or "security-reviewer" or "test-auditor" node types
- Graph skills register their own nodes dynamically — the orchestrator doesn't
  care what they do
- The graph-planner designs topologies by matching request to available
  skills/agents, not by hardcoded templates
- The router follows whatever nodes are registered, not a hardcoded priority list

**Announce at start:** "I'm using the graph engine to route this through the state machine."

### Flow

```
User request → decomposer → graph-planner (designs topology)
  → confirm (you approve) → execute nodes (parallel + sequential) → consolidate
```

The graph-planner is mandatory on every invocation. Even for a one-line fix,
you see the proposed topology and approve it before execution.

### Architecture

```
```
                    ┌─────────────────────────────┐
                    │       SHARED STATE          │
                    │  work/graph/state.json      │
                    │  status, topology, nodes{}  │
                    │  _dependencies, _barriers   │
                    └─────────────┬───────────────┘
                                  │
                      ┌───────────┴───────────┐
                      │        ROUTER         │
                      │  f(state) -> ready[]  │
                      └───────────┬───────────┘
                                  │
          ┌────────────┬──────────┼──────────┬─────────────┐
          ▼            ▼          ▼          ▼             ▼
   ┌────────────┐ ┌────────┐ ┌─────────┐ ┌────────┐ ┌──────────┐
   │ graph-     │ │confirm │ │ parallel│ │ graph  │ │human_    │
   │ planner    │ │(gate)  │ │ exec    │ │skill   │ │input     │
   └──────┬─────┘ └───┬────┘ │ nodes   │ │nodes   │ └────┬─────┘
          │            │      └─────────┘ └────────┘      │
          └────────────┴────────────┬─────────────────────┘
                                    ▼
                             ┌──────────────┐
                             │ consolidator │
                             └──────────────┘
```

"Exec nodes" now support parallel execution: multiple nodes whose dependencies
are satisfied fire concurrently as background sub-agents. The router returns a
*set* of ready nodes, not a single next node.
```

"Exec nodes" are dynamically registered per topology step — methodology skills,
agents, or generic executors.
"Graph skill nodes" are registered from a skill's `## Graph` section.

### Key properties

- **State router, not puppeteer.** The orchestrator never copies text between
  agents. Nodes write to shared state; the next node reads from it.
- **Graph planner before confirm gate.** The system designs a topology first,
  then you review and approve it. No execution happens without your go-ahead.
- **No hardcoded node types.** coder, security-reviewer, test-auditor do not
  exist. Every execution node is dynamically registered from topology nodes or
  skill graphs.
- **Orchestration nodes are inline.** decomposer, graph-planner, confirm, and
  consolidator run in your (the orchestrator's) main context.
- **Execution nodes are sub-agents.** Any dynamically registered node that does
  real work runs as an isolated sub-agent for token separation.
- **Graph skill nodes are first-class.** When a topology step references a graph
  skill (e.g., create-skill, research), all its nodes are registered in the
  state machine and routed through like built-in nodes.
- **Micro-loops are graph-driven.** Review → fix → re-review is expressed as
  a cycle edge in the topology. The fix node re-runs with review feedback
  injected. The router tracks iteration counters per cycle edge, not per step.
- **Dynamic graph extension.** A node whose output contains an `_extensions`
  field can trigger the graph-planner to inject new nodes into the running
  graph mid-execution. This allows the topology to grow as work progresses.

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
| `PLANNING` | Designing graph topology (nodes, edges, parallel paths). |
| `CONFIRM` | Waiting for user approval on the proposed topology. |
| `EXECUTING` | One or more execution nodes active (may be parallel). |
| `EXTENDING` | A node signaled extension needs; graph-planner is adding nodes. |
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
| `graph-planner` | inline | Design graph topology, present for approval |
| `confirm` | inline | Activate selected topology, get user approval |
| `human_input` | inline | Pause for user escalation or modification |
| `consolidator` | inline | Read all output, present final results |

### Dynamically registered nodes (per topology step)

When the confirm node activates a topology, it registers nodes from the
selected topology's node list. These join the state machine alongside the
built-in nodes. Nodes with no dependencies on other topology nodes are set to
`"ready"` immediately. Nodes with dependencies wait for their inputs.

**Node types and their registration:**

| Node type | Registration |
|-----------|-------------|
| `skill` (methodology) | One node `<label>`. Sub-agent reads the skill's SKILL.md and executes it. |
| `skill` (graph) | All nodes from the skill's `## Graph` section, prefixed with `<label>.`. Each registered with its defined trigger, role, skills, output, and route. |
| `agent` | One node `<label>`. Sub-agent reads the agent's brain.md and runs with its configured model and tools. |
| `fix` | One node `<label>`. Sub-agent receives the preceding work node's output plus review feedback, re-does the work. |
| `plan` | One node `<label>`. Sub-agent reads the planning skill and produces a plan. |

**Node naming convention:** Nodes are named by their label in the topology
(e.g., `research-arxiv`, `synthesize-findings`, `verify-security`).
Graph-skill nodes are prefixed `<label>.` to prevent collisions.

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

**Routing:** Always -> `graph-planner`

---

### Node: `graph-planner` (inline)

**Trigger:** `state.routing.next_node == "graph-planner"`

**Mandatory.** Runs on every invocation. You see the proposed topology before
any work starts. Also runs **mid-execution** when a node signals a dynamic
extension (see Section 3 — Dynamic Extension).

**Input (`_extending: false` — initial planning):**
`state.user_request`, `state.decomposition.tasks`,
`state.skill_index`, `state.agent_index`

**Input (`_extending: true` — dynamic extension):**
`state._extend_context` (contains the node that signaled, its output,
and the current state), `state.skill_index`, `state.agent_index`

**Behavior:** Run this inline — do not launch a sub-agent.

1. Check if this is an initial planning call or a dynamic extension call.
2. Set `state.status = "PLANNING"` (or `"EXTENDING"` if re-entering mid-execution).

#### Initial planning (_extending: false, the default)

Design graph topologies directly, using graph engineering principles.

#### Step A: Check if the user already described a topology

Scan the user's request for graph language:
- Sequential connectors: "first... then", "next", "after that", "and then"
- Parallel indicators: "at the same time", "in parallel", "simultaneously",
  "both", "all of these"
- Ordered lists: "1." "2." "3.", "step 1" "step 2"
- Explicit skill or agent names (matched against both indices)
- Verifier language: "verify", "double-check", "validate", "confirm"
- Conditional language: "if... then", "depending on", "in case of"

**If structured language is detected:**
- Parse into a graph topology with nodes and edges:
  - Each sequential/parallel clause becomes a node
  - "And then" / "next" becomes a sequential edge
  - "At the same time" / "in parallel" marks nodes as parallel (no edge between them)
  - "If X then Y" becomes a router node with conditional edges
  - "Verify" / "validate" after a node becomes a verifier edge
- For each node, match against `agent_index` first, then `skill_index`:
  - **Agent match (highest priority):** Exact name match. Use the agent's
    `skills` list and `model`. Node type becomes `"agent"`.
  - **Skill match:** Name match, description keyword match, or task verb match.
  - **Agent fallback by skill:** If no agent matched by name, check if any
    agent lists the matched skill in its `skills` field. If yes, prefer the agent.
  - If no match: node type becomes `"work"` (generic executor, model: default).
- Build **exactly as described**. No collapsing or reordering. Add warnings
  as notes.
- Assign models per node — agent frontmatter model takes precedence.
- Show the topology directly — **no menu of alternatives.**

#### Step B: No topology language detected — design from scratch

Design 2-3 topology proposals using graph engineering principles.

**Design process:**

1. **Start from the output.** What is the user asking for? What shape does
   the final answer have? That's your merge/synthesize node.

2. **Decompose by data independence.** What independent pieces feed the
   final answer? Each independent piece is a fan-out node. If the request
   has multiple sources, lenses, or dimensions, each gets its own node.

3. **Add verifiers on critical edges.** If the output quality matters
   (code, financial analysis, security audit), add a verifier node between
   synthesis and output. For high-stakes work, use perspective-diverse
   verifiers (correctness, security, performance).

4. **Add routers where classification is needed.** If the request has
   conditional paths ("if the finding is severe, do X; if not, do Y"),
   add a router node that classifies and branches.

5. **Tier models per node.** Fan-out/research nodes get cheaper models.
   Synthesis/judgment nodes get expensive ones. Verifiers get cheap ones
   (multiple cheap verifiers > one expensive one).

6. **Estimate cost.** Approximate token count per node, multiply by
   model tier cost, sum. Write to state.

**Topology templates (adapt, don't copy):**

| Pattern | When | Structure |
|---------|------|-----------|
| **Diamond** | Research, data gathering, multi-source analysis | Fan-out N parallel researchers → reduce (code) → synthesize |
| **Diamond + Verifier** | Code review, security audit, financial analysis | Fan-out N reviewers → synthesize → verify (adversarial) → output |
| **Router** | Classification-dependent handling | Classify node → [heavy path | light path] → output |
| **Cycle** | Unknown-size discovery, bug sweep | Parallel finders → dedupe (code) → verify → loop until dry |
| **Pipeline** | Batch processing through stages | Stage-1 → stage-2 → stage-3 (each item independent) |
| **Composite** | Complex multi-phase work | Phase 1 diamond → phase 2 cycle → phase 3 verifier chain |

**Model assignment defaults:**

| Node role | Model |
|-----------|-------|
| planning, architecture, design | `sonnet` |
| synthesis, judgment, adjudication | `sonnet` |
| fan-out, research, data gathering | `haiku` |
| verification, review, audit | `haiku` |
| classification, extraction, routing | `haiku` |
| code generation, fix | `sonnet` |
| no clear type | `default` |

**Agent override:** Agent's frontmatter `model` takes precedence.

#### Step C: Present topologies to user

Show 2-3 topology proposals with enough detail to make a decision.
For each proposal:

```
Topology A: Diamond + Verifier (recommended)
Description: Fan-out 3 research agents → synthesize findings → verify with adversarial check

Nodes:
- research-arxiv (skill: research, model: haiku): Searches arXiv for papers
- research-web (skill: research, model: haiku): Searches web for recent posts
- research-github (skill: research, model: haiku): Searches GitHub for implementations
- synthesize (skill: writing-plans, model: sonnet): Merges findings into report
- verify (skill: code-review, model: haiku): Adversarially checks each claim
- consolidator: Presents final output

Edges:
- research-arxiv → synthesize (papers feed synthesis)
- research-web → synthesize (posts feed synthesis)
- research-github → synthesize (repos feed synthesis)
- synthesize → verify (draft gets verified)
- verify → consolidator (verified report presented)

Topology: diamond (fan-out 3, fan-in 1, verifier on merge)
Cost estimate: ~6K-10K tokens (3x haiku + 1x sonnet + 1x haiku)
```

**Ask the user to pick one, or describe modifications.** Do not proceed
without their choice.

#### Step D: Write selected topology to state

```json
{
  "status": "PLANNING",
  "graph_topologies": [
    {
      "name": "Diamond with Verifier",
      "description": "Fan-out 3 research sources → synthesize → verify",
      "nodes": [
        { "id": "research-arxiv", "type": "skill", "name": "research",
          "model": "haiku", "inputs": [], "outputs": ["findings-arxiv"] },
        { "id": "research-web", "type": "skill", "name": "research",
          "model": "haiku", "inputs": [], "outputs": ["findings-web"] },
        { "id": "research-github", "type": "skill", "name": "research",
          "model": "haiku", "inputs": [], "outputs": ["findings-github"] },
        { "id": "synthesize", "type": "skill", "name": "writing-plans",
          "model": "sonnet", "inputs": ["findings-arxiv", "findings-web",
            "findings-github"], "outputs": ["draft"] },
        { "id": "verify", "type": "skill", "name": "code-review",
          "model": "haiku", "inputs": ["draft"], "outputs": ["verdict"] },
        { "id": "consolidator", "type": "node", "role": "consolidator",
          "inputs": ["draft", "verdict"], "outputs": [] }
      ],
      "edges": [
        { "from": "research-arxiv", "to": "synthesize",
          "data": "findings-arxiv" },
        { "from": "research-web", "to": "synthesize",
          "data": "findings-web" },
        { "from": "research-github", "to": "synthesize",
          "data": "findings-github" },
        { "from": "synthesize", "to": "verify", "data": "draft" },
        { "from": "verify", "to": "consolidator", "data": "verdict" }
      ],
      "topology": "diamond",
      "cost_estimate": { "tokens": "6K-10K",
        "breakdown": "3x haiku research + 1x sonnet synthesis + 1x haiku verify" }
    }
  ],
  "selected_topology": 0,
  "routing": { "last_node": "graph-planner", "next_node": "confirm",
    "reason": "topology selected" }
}
```

**Node fields:** `id` (unique label), `type` (skill|agent|node), `name`
(skill/agent name), `model`, `inputs` (list of output IDs from upstream nodes),
`outputs` (list of output IDs this node produces), optional `role`, `tools`,
`skills`.

**Routing:**
- If `_extending: true` -> route to `router` (new nodes are injected into the
  running graph immediately; no confirm gate for extensions)
- If `_extending: false` -> always -> `confirm`
- If user aborts -> consolidator

#### Dynamic extension mode (_extending: true)

Called when a node's output contains an `_extensions` field. The graph-planner
receives context from `state._extend_context`:

```json
{
  "_extend_context": {
    "trigger_node": "research-arxiv",
    "trigger_output": {
      "_extensions": [
        {
          "description": "Found a promising sub-field that needs deeper investigation",
          "task": "search for papers on topological quantum error correction",
          "suggested_skill": "research",
          "suggested_model": "haiku",
          "depends_on_outputs": []
        }
      ],
      "items": [...]
    },
    "current_state": { ... }
  }
}
```

**Behavior:** For each extension in the `_extensions` array:

1. **Name the extension node** — generate a unique id by appending a counter
   to the trigger node's id (e.g., `research-arxiv-ext-1`).

2. **Match against skill/agent index** — same as Step A above: agent first,
   then skill. If no match, use `"work"` (generic executor).

3. **Assign model** — use `suggested_model` if provided, otherwise match from
   the standard model assignment table.

4. **Compute dependencies** — the extension node depends on the trigger node's
   output (the data that revealed the extension), plus any explicit
   `depends_on_outputs`. Add to `state._dependencies`.

5. **Register the node** — set its status to `"pending"` and add it to
   `state.nodes`.

6. **Present to user** — show the extension proposal:

```
[GRAPH ENGINE — DYNAMIC EXTENSION]
Node "research-arxiv" found new independent work:
  → Added node "research-arxiv-ext-1" (skill: research, model: haiku)
  → Task: search for papers on topological quantum error correction
  → Will run after "research-arxiv" completes

Proceed with this extension, modify, or skip?
```

   Wait for user input. Options:
   - "proceed" — inject the extension nodes and continue execution
   - "skip" — discard the extensions and continue execution
   - "modify" — route to `human_input` for manual adjustment, then return

7. **Write back to state** — update `state.nodes`, `state._dependencies`,
   and set `state.status = "EXECUTING"`.

**Key constraints:**
- Extension nodes are always downstream of their trigger node (they depend on
  its output). They cannot create dependencies on nodes that haven't run yet.
- An extension node can itself trigger further extensions (chain of discovery).
- Max 3 extension generations per root topology node. Tracked in
  `state._extension_generation[node_id]`. Beyond that, route to `human_input`.

**Edge cases:**
- **No skills or agents matched:** Build a single generic `work` node.
- **Unmatched node:** Leave as generic `work`, note to user.
- **Agent with empty skills field:** Use agent without referencing a specific skill.
- **Multiple agents match same skill:** List as options in the topology proposal.
- **User says "just do it":** Propose the simplest topology (diamond or single
  node) and ask for approval once. Do not skip the confirm gate.

---

### Node: `confirm` (inline)

**Trigger:** `state.routing.next_node == "confirm"`

**Mandatory approval gate.**

**Input:** `state.user_request`, `state.decomposition`, `state.graph_topologies`,
`state.selected_topology`, `state.skill_index`,
`state.agent_index`, `state.nodes`

**Behavior:** Run this inline — do not launch a sub-agent.

1. Set `state.status = "CONFIRM"`.
2. Read the selected topology (`state.graph_topologies[state.selected_topology]`).
3. Activate nodes from the topology's node list:

   For each node in the topology:

   **If node type is `"skill"` and the skill has a `## Graph` section:**
   - Read the skill's `## Graph` section
   - Register each of its nodes in state, prefixing names with
     `<topology-node-id>.`
   - Use each node's defined `trigger`, `role`, `skills`, `output`, `route`
   - Set the first node in the skill's graph to `"ready"`
   - Store the graph's internal routing rules

   **If node type is `"skill"` (methodology — no graph):**
   - Register one node named `<topology-node-id>`
   - Set its status to `"pending"` (will become ready when dependencies met)

   **If node type is `"agent"`:**
   - Register one node named `<topology-node-id>`
   - Set its status to `"pending"`

   **If node type is `"node"` (generic role like `fix` or `consolidator`):**
   - Register one node named `<topology-node-id>`
   - Set its status to `"pending"`

4. **Compute dependencies from topology edges.** For each node, find all
   upstream nodes whose outputs feed into it. Store as `_dependencies`:

   ```json
   {
     "_dependencies": {
       "synthesize": ["research-arxiv", "research-web", "research-github"],
       "verify": ["synthesize"],
       "consolidator": ["verify"]
     }
   }
   ```

   Nodes with no dependencies (`research-*` above) are immediately set to
   `"ready"`.

5. Present the topology to the user directly (not via sub-agent).
   Show:
   - The node list with their types, skills, and models
   - The edges showing data flow
   - The topology shape (diamond, pipeline, etc.)
   - The cost estimate
   - Which nodes will run in parallel (those with no dependencies)
   - Ask: "Proceed with this topology?"

**Routing:** "proceed" -> router (which finds all ready nodes).
"change topology" -> route to graph-planner.
"modify tasks" / "add nodes" -> route to human_input.
"abort" -> consolidator.

**Graph skill internal routing:**

When activating a graph skill's nodes as part of a topology node, create a
mapping entry so the router can resolve graph-internal routing:

```json
{
  "_graph_routes": {
    "<topology-node-id>": {
      "entry": "<first-node-name>",
      "routes": [
        { "from": "<node-a>", "condition": "always", "to": "<node-b>" }
      ],
      "sink": "<last-node-name>",
      "topology_exit": "<next-topology-node-id>"
    }
  }
}
```

When the last node of a graph skill completes, the router routes to the next
topology node that depends on its output.

---

### Node: `human_input` (inline)

**Trigger:** `state.routing.next_node == "human_input"`

**Pauses the graph** for error escalation, plan modification, or topology re-route.

**Behavior:** Present context, wait for response, write to
`state.nodes.human_input`.

**Routing:**
- "continue" -> reset counter, re-route to the node that triggered the pause
- "skip" / "abort" -> consolidator
- Plan modification -> re-run decomposer -> graph-planner
- Topology re-route -> graph-planner

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

The router is `f(state) -> ready_nodes[]`. Called after every node completes.
Unlike a linear router that returns one next node, this router returns a *set*
of nodes whose dependencies are satisfied. Multiple ready nodes fire in
parallel.

```
function get_ready_nodes(state):
    if state.status in ["COMPLETE", "ERROR"]: return []
    if state.nodes.human_input.status == "responded":
        return [route_from_human(state)]

    # 1. Check explicit routing override
    if state.routing.next_node:
        return [state.routing.next_node]

    ready = []

    # 2. Check topology dependencies
    # A node is ready when:
    #   a) Its status is "pending"
    #   b) All its dependencies are "complete" (outputs available)
    #   c) No other node with the same output target is still running
    deps = state.get("_dependencies", {})
    for each name, node in state.nodes:
        if name.startswith("_"): continue  # skip metadata
        if node.status != "pending": continue

        node_deps = deps.get(name, [])
        all_met = all(
            state.nodes[d].get("status") == "complete"
            for d in node_deps
        )
        if all_met:
            ready.append(name)

    # 3. Check graph skill internal routing
    active_graph = state.get("_graph_routes", {})
    for graph_key, graph_info in active_graph.items():
        current = graph_info.get("current_node")
        if current == graph_info.get("sink"):
            topology_exit = graph_info.get("topology_exit")
            if topology_exit and topology_exit not in ready:
                ready.append(topology_exit)

    # 4. Check for dynamic extensions from completed nodes
    # When a node completes, read its output file. If the output contains
    # an _extensions field, the node has signaled new independent work
    # that should be added to the graph dynamically.
    for each name, node in state.nodes:
        if name.startswith("_"): continue
        if node.status == "complete":
            output_path = f"work/graph/output/{name}/output.json"
            if os.path.exists(output_path):
                import json
                with open(output_path, "r") as f:
                    output = json.load(f)
                if "_extensions" in output and output["_extensions"]:
                    # Check extension generation limit
                    gen = state.get("_extension_generation", {}).get(name, 0)
                    if gen < 3:
                        # Signal to graph-planner for extension
                        state._extend_context = {
                            "trigger_node": name,
                            "trigger_output": output,
                            "current_state": state
                        }
                        state._extension_generation.setdefault(name, 0)
                        state._extension_generation[name] += 1
                        return ["graph-planner"]
                    else:
                        # Max generations reached — log and skip
                        state.graph_errors.append(
                            f"Max extension generations (3) reached for node {name}"
                        )

    # 5. Fall through to consolidator if nothing ready and nothing running
    running = [n for n in state.nodes.values()
               if n.get("status") == "running"]
    if not ready and not running:
        return ["consolidator"]

    return ready
```

### Execution model

```
function execute_round(state):
    ready = get_ready_nodes(state)

    if not ready:
        return  # nothing to do — wait for running nodes to finish

    if len(ready) == 1:
        # Single node — execute synchronously
        execute_node(ready[0], state)
        update_state(state)
        execute_round(state)  # re-check for newly ready nodes
    else:
        # Multiple nodes — no dependencies between them → launch in parallel
        for each node_name in ready:
            state.nodes[node_name].status = "running"
            launch_as_background_subagent(node_name, state)
        # Return to caller. Background agent completion triggers re-check.
        # (The pi harness notifies when background agents complete — on each
        #  notification, re-read state, call get_ready_nodes, and fire again.)
```

### Priority

1. `human_input` (highest — always checked first)
2. Topology dependency resolution (nodes whose inputs are all complete)
3. Graph skill internal routing (node-to-node within a skill's graph)
4. `consolidator` (always last, only when nothing is ready or running)

### Fan-in barriers

A fan-in node (one with multiple dependencies) only fires when ALL upstream
nodes complete. This is enforced by `_dependencies`:

```json
{
  "_dependencies": {
    "synthesize": ["research-arxiv", "research-web", "research-github"]
  }
}
```

`synthesize` stays `"pending"` until all three research nodes report
`"complete"`. The router checks the full dependency set every time.

### Micro-loop (graph-driven)

Micro-loops are expressed as cycle edges in the topology. When a topology
has a cycle (e.g., `verify -> fix -> verify`), the router tracks iteration
counters per edge:

1. When `verify` completes with findings, the `fix` node's dependencies are
   met -> `fix` becomes `"ready"`.
2. `fix` runs, then `verify` runs again on the fixed output.
3. If `verify` still has findings and iterations < max: loop again.
4. If `verify` passes or iterations >= max: break the cycle, route to the
   next downstream node or `consolidator`.

```
verify -> (has issues? -> fix -> verify)
       -> (passes?      -> consolidator)
```

The router increments an iteration counter per cycle edge. Max 5 iterations,
then escalates to `human_input`.

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
    topology = state.graph_topologies[state.selected_topology]
    for each graph_node in topology.nodes:
        if graph_node.id == node_name:
            return graph_node.model
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
| Graph skill node not found in state | Log error, treat graph step as complete, route to next topology node. |

Recovery: write to `work/graph/errors.log`, set `status = "ERROR"`, route
to `human_input`. User can reset, skip, or abort.

---

## 6. Output Structure

```
work/graph/
├── state.json              # Shared state
├── errors.log              # Graph-level errors
├── output/
│   ├── <topology-node-id>/         # One directory per execution node
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

These are registered dynamically when the skill is referenced in a topology.

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
