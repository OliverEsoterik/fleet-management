# Confirm Gate Example

The confirm gate shows the execution plan for the selected chain. The user approves, modifies, or aborts before any work starts.

## Example: Fast chain

```
[GRAPH ENGINE — PLAN CONFIRMATION]
Request: implement feature X

Selected chain: Fast
Chain steps:
  1. feature-implementation [default] — implement the feature
  2. consolidator [default] — wrap up

Nodes to execute:
  - coder: implement feature X [skills: feature-implementation]
  - consolidator: merge results

Options:
1) Proceed
2) Change chain
3) Modify tasks
4) Add nodes
5) Abort
```

## Example: Chain with agent step

```
[GRAPH ENGINE — PLAN CONFIRMATION]
Request: audit our GitOps setup

Selected chain: Fast
Chain steps:
  1. gitops-expert [haiku] — full GitOps audit
     > Agent: agents/gitops-expert.md (wraps sre, code-review)
  2. consolidator [default] — wrap up

Nodes to execute:
  - coder: run gitops-expert agent [haiku]
  - consolidator: merge results

Options:
1) Proceed
2) Change chain
3) Modify tasks
4) Add nodes
5) Abort
```

## Routing

- "proceed" -> first ready node
- "change chain" -> reset `selected_chain = -1`, route to `chain-planner`
- "modify tasks" / "add nodes" -> route to `human_input`
- "abort" -> consolidator