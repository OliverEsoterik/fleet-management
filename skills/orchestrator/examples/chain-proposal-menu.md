# Graph Topology Proposal — Menu Example

When the user's request has no sequential/parallel language, the graph-planner designs 2-3 topology proposals. Each proposal shows nodes, edges, topology shape, and cost estimate.

## Example: Research request

```
[GRAPH ENGINE — TOPOLOGY PROPOSALS]
Request: research quantum computing error correction

Topology A: Diamond (recommended)
Description: Fan-out 3 research sources -> synthesize
Nodes:
  - research-arxiv [haiku]: search arXiv
  - research-github [haiku]: search GitHub
  - research-web [haiku]: search web
  - synthesize [sonnet]: merge findings
Edges: 3 parallel -> 1 merge
Cost: ~8K-12K tokens

Topology B: Diamond + Verifier
Description: Same as A, but with adversarial verify before output
Nodes:
  - research-arxiv [haiku], research-github [haiku], research-web [haiku]
  - synthesize [sonnet]
  - verify [haiku]: check each claim
  - consolidator
Edges: 3 parallel -> merge -> verify -> output
Cost: ~10K-15K tokens

Topology C: Sequential
Description: Single research pass, simpler but slower
Nodes:
  - research [haiku]: search all sources sequentially
  - consolidator
Edges: research -> output
Cost: ~3K-5K tokens

Choose topology (A/B/C) or describe modifications:
```

## Example: Code feature request

```
[GRAPH ENGINE — TOPOLOGY PROPOSALS]
Request: implement a rate limiter for the API

Topology A: Sequential (recommended)
Description: Plan -> implement -> review -> fix
Nodes:
  - plan [sonnet]: design architecture
  - implement [default]: write code
  - code-review [haiku]: review implementation
  - fix [sonnet]: fix review issues
  - consolidator
Edges: sequential chain
Cost: ~15K-25K tokens

Topology B: Diamond + Verifier
Description: Implement + parallel security audit -> fix -> verify
Nodes:
  - plan [sonnet]: design architecture
  - implement [default]: write code
  - security-audit [haiku]: parallel security review
  - fix [sonnet]: fix issues
  - verify [haiku]: verify fixes
  - consolidator
Edges: plan -> (implement, audit) -> fix -> verify -> output
Topology: diamond with verifier chain
Cost: ~20K-35K tokens

Topology C: Fast
Description: Direct implementation, no review
Nodes:
  - implement [default]: write code
  - consolidator
Cost: ~5K-10K tokens

Choose topology (A/B/C) or describe modifications:
```

## Key rules

- Topologies are built dynamically from the skill and agent indices
- Each topology shows: nodes, edges, topology shape, and cost estimate
- The recommended topology is marked (usually diamond or diamond+verifier)
- Model tiering is applied per node (fan-out gets cheap, synthesis gets expensive)
- No "Custom" option — if none fit, user describes what they want
