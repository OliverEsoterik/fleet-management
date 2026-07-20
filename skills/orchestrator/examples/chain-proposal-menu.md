# Chain Proposal — Menu Example

When the user's request has no sequential language, the chain-planner shows a menu of standard chains.

## Example

```
[GRAPH ENGINE — CHAIN PROPOSAL]
Request: implement feature X

Available chains:

1) Fast — Direct implementation, no audit
   Steps:
     a. feature-implementation [model: default]
     b. consolidator [model: default]

2) Safe — Implement + code review
   Steps:
     a. architect (analysis + ADR + plan) [model: sonnet]
     b. feature-implementation [model: default]
     c. code-review [model: haiku]
     d. Fix review issues [model: sonnet]
     e. consolidator [model: default]

3) Thorough — Full pipeline with audit
   Steps:
     a. architect (analysis + ADR + plan) [model: sonnet]
     b. feature-implementation [model: default]
     c. sre (security audit) [model: haiku]
     d. code-review [model: haiku]
     e. Fix issues from audits [model: sonnet]
     f. consolidator [model: default]

Choose a chain (1-3):
```

## Key rules

- Chains are built dynamically from the skill and agent indices
- If a skill or agent isn't registered, the chain drops that step
- If the request matches an agent (e.g., "audit GitOps"), the chain uses the agent instead of the raw skill
- No "Custom" option — if none of these fit, the user rephrases with "first... then..."