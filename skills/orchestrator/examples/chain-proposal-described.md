# Graph Topology Proposal — Described Request Example

When the user's request contains sequential or parallel language ("first... then...", "at the same time", "verify"), the graph-planner shows a single resolved topology with no menu.

## Example 1: GitOps audit then fix

```
[GRAPH ENGINE — TOPOLOGY PROPOSAL]
Request: audit our GitOps setup, then fix any issues found

Resolved topology from your description:

Nodes:
- gitops-audit (skill: sre, model: haiku): full GitOps audit (ArgoCD/Flux)
  > Agent: agents/gitops-expert.md
- fix-issues (role: fix, model: sonnet): fix issues from audit report
- consolidator: wrap up

Edges:
- gitops-audit -> fix-issues (audit findings)
- fix-issues -> consolidator (fixed output)

Topology: sequential (2 nodes, no fan-out)
Cost estimate: ~3K-5K tokens

Proceed with this topology, or describe modifications:
```

## Example 2: Research with parallel sources

```
[GRAPH ENGINE — TOPOLOGY PROPOSAL]
Request: research transformer architectures, looking at papers, code, and blog posts at the same time, then synthesize

Resolved topology from your description:

Nodes:
- research-arxiv (skill: research, model: haiku): search arXiv for papers
- research-github (skill: research, model: haiku): search GitHub for implementations
- research-web (skill: research, model: haiku): search web for blog posts
- synthesize (skill: writing-plans, model: sonnet): merge findings into report
- consolidator: wrap up

Edges:
- research-arxiv -> synthesize (papers)
- research-github -> synthesize (repos)
- research-web -> synthesize (posts)
- synthesize -> consolidator (report)

Topology: diamond (fan-out 3, fan-in 1)
Cost estimate: ~8K-12K tokens (3x haiku + 1x sonnet)

Proceed with this topology, or describe modifications:
```

## Key rules

- No menu — parsed directly from request language
- Parallel indicators ("at the same time", "both", "in parallel") create fan-out nodes
- Connectors ("then", "next") create sequential edges
- Verifier language ("verify", "double-check") adds verifier nodes
- Each node is matched against `agent_index` first, then `skill_index`
- Graph skills show their node count
- Always add `consolidator` as the final step if not already present
