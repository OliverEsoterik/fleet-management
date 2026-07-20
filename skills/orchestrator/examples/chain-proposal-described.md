# Chain Proposal — Described Chain Example

When the user's request contains sequential language ("first... then..."),
the chain-planner shows a single resolved chain with no menu.

## Example 1: GitOps audit then fix

```
[GRAPH ENGINE — CHAIN PROPOSAL]
Request: audit our GitOps setup, then fix any issues found

Resolved chain from your description:

1. gitops-expert [haiku] — full GitOps audit (ArgoCD/Flux)
   > Agent: agents/gitops-expert.md (specializes in sre, code-review)
   > Produces: work/graph/output/1-gitops-expert/audit-report.md
2. fix [sonnet] — fix issues from audit report
   > Generic fix step, receives audit output as input
3. consolidator [default] — wrap up

Proceed with this chain, or describe modifications:
```

## Example 2: Research then architect

```
[GRAPH ENGINE — CHAIN PROPOSAL]
Request: check relevant code first, then do technical research, then options

Resolved chain from your description:

1. architect [sonnet] — analyze codebase, understand current logic
   > Graph skill: 3 nodes (analysis, adr-writer, planner)
   > Produces: work/graph/output/1-architect.*/
2. research [haiku] — state of the art, search arxiv + github + web
   > Graph skill: 10 nodes (source-validator, query-refiner, ...)
   > Produces: work/graph/output/2-research.*/
   > Note: architect already includes internal research — this step runs
   > the dedicated research skill for deeper coverage.
3. work [default] — produce implementation options from analysis + research
   > No matching skill found for "come up with options". Using generic
   > executor step with context from architect + research outputs.
4. consolidator [default] — wrap up

Proceed with this chain, or describe modifications:
```

## Key rules

- No menu, no Fast/Safe/Thorough/Custom options
- Each step is matched against `agent_index` first, then `skill_index`
- Graph skills show their node count in the chain display
- If multiple interpretations exist, list them numbered but keep it brief
- Always add `consolidator` as the final step if not already present