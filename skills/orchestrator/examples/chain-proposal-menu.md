# Chain Proposal — Menu Example

When the user's request has no sequential language, the chain-planner shows
a menu of standard chains. Step roles (work, review, plan) are resolved to
actual skills from the skill_index.

## Example: Research request

```
[GRAPH ENGINE — CHAIN PROPOSAL]
Request: research quantum computing error correction

Available chains:

1) Fast — Direct research, no audit
   Steps:
     a. research [haiku] — work
     b. consolidator [default]

2) Safe — Research + review
   Steps:
     a. research [haiku] — work
     b. code-review [haiku] — review (resolved from skill_index)
     c. fix [sonnet] — fix issues from review
     d. consolidator [default]

3) Thorough — Plan + research + review + fix
   Steps:
     a. architect [sonnet] — plan (resolved from skill_index)
     b. research [haiku] — work
     c. code-review [haiku] — review
     d. fix [sonnet] — fix
     e. consolidator [default]

Choose a chain (1-3):
```

## Example: Code feature request

```
[GRAPH ENGINE — CHAIN PROPOSAL]
Request: implement a rate limiter for the API

Available chains:

1) Fast — Direct implementation, no audit
   Steps:
     a. feature-implementation [default] — work
     b. consolidator [default]

2) Safe — Implement + code review
   Steps:
     a. feature-implementation [default] — work
     b. code-review [haiku] — review
     c. fix [sonnet] — fix
     d. consolidator [default]

3) Thorough — Plan + implement + sre + code review + fix
   Steps:
     a. architect [sonnet] — plan
     b. feature-implementation [default] — work
     c. sre [haiku] — review (security audit)
     d. code-review [haiku] — review
     e. fix [sonnet] — fix
     f. consolidator [default]

Choose a chain (1-3):
```

## Key rules

- Chains are built dynamically from the skill and agent indices
- Step roles (work, review, plan, fix) are resolved to actual skills
- If a role cannot be resolved (e.g., no review skill found), that step is dropped
- If an agent matches the request, the chain uses the agent for the `work` role
- No "Custom" option — if none of these fit, the user rephrases with
  "first... then..."