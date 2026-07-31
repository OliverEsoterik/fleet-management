# Confirm Gate Example

The confirm gate shows the execution plan for the selected chain. The user
approves, modifies, or aborts before any work starts.

## Example: Fast chain (methodology skill)

```
[GRAPH ENGINE — PLAN CONFIRMATION]
Request: implement feature X

Selected topology: Fast
Topology nodes:
  1. feature-implementation [default] — implement the feature
  2. consolidator [default] — wrap up

Registered nodes:
  - 1-feature-implementation: implement feature X [methodology skill]
  - consolidator: merge results

Options:
1) Proceed
2) Change topology
3) Modify tasks
4) Add nodes
5) Abort
```

## Example: Safe chain with graph skill

```
[GRAPH ENGINE — PLAN CONFIRMATION]
Request: research quantum computing

Selected topology: Safe
Topology nodes:
  1. research [haiku] — work (graph skill, 10 nodes)
  2. code-review [haiku] — review (methodology skill)
  3. fix [sonnet] — fix issues
  4. consolidator [default] — wrap up

Registered nodes:
  - 1-research.source-validator: validate sources
  - 1-research.query-refiner: refine queries
  - 1-research.arxiv-researcher: search arxiv
  - 1-research.github-researcher: search github
  - 1-research.pubmed-researcher: search pubmed
  - 1-research.archive-researcher: search archive
  - 1-research.web-researcher: search web
  - 1-research.synthesis-writer: synthesize findings
  - 1-research.report-writer: write report
  - 1-research.cleanup: clean up artifacts
  - 2-code-review: review research report
  - 3-fix: fix review issues
  - consolidator: merge results

Options:
1) Proceed
2) Change topology
3) Modify tasks
4) Add nodes
5) Abort
```

## Example: Chain with agent step

```
[GRAPH ENGINE — PLAN CONFIRMATION]
Request: audit our GitOps setup

Selected topology: Fast
Topology nodes:
  1. gitops-expert [haiku] — full GitOps audit
     > Agent: agents/gitops-expert.md (wraps sre, code-review)
  2. consolidator [default] — wrap up

Registered nodes:
  - 1-gitops-expert: run gitops-expert agent [haiku]
  - consolidator: merge results

Options:
1) Proceed
2) Change topology
3) Modify tasks
4) Add nodes
5) Abort
```

## Routing

- "proceed" -> first set of ready nodes
- "change chain" -> reset `selected_topology = -1`, route to `graph-planner`
- "modify tasks" / "add nodes" -> route to `human_input`
- "abort" -> consolidator