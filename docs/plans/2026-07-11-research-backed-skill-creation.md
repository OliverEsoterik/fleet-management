# Research-Backed Skill Creation

**Date:** 2026-07-11
**Status:** Proposal

## Problem

The current `create-skill` skill is a thin methodology skill — it says "pick a type, name it, write it." It skips research entirely. Skills produced this way rely solely on the LLM's training weights, which means:

- No awareness of recent developments (papers, tools, standards)
- No citations or real sources
- No competitive analysis of existing implementations
- Shallow treatment of the topic with generic advice

## Proposal

Upgrade `skills/create-skill/SKILL.md` from a **methodology skill** to a **delegation skill** with a research-first workflow. The orchestrator follows 4 phases:

### Phase 1 — Research (parallel)

Launch 3-4 subagents concurrently to gather source material. Each searches a different domain:

| Agent | Sources | Output |
|---|---|---|
| Academic researcher | Semantic Scholar, arXiv | `work/<skill-name>/research/academic.md` |
| Web researcher | General web search, official docs, tutorials, best practices | `work/<skill-name>/research/web.md` |
| (Optional) GitHub researcher | GitHub search for existing tools, libraries, reference implementations | `work/<skill-name>/research/github.md` |
| (Optional) Historical researcher | Archive.org, Google Scholar for niche/older context | `work/<skill-name>/research/historical.md` |

Each agent returns a structured document with:
- Key concepts and definitions
- Recent developments and state-of-the-art
- Common pitfalls, anti-patterns, controversies
- Standards, specifications, or frameworks
- Curated links to high-quality sources

### Phase 2 — Synthesize (sequential, after Phase 1)

One subagent reads all research outputs and produces a consolidated reference document:

- Unified terminology and conceptual model
- Ranked list of most important findings
- Conflicts or contradictions between sources
- Recommendations for what the skill should cover
- Gaps where no good sources were found

**Output:** `work/<skill-name>/synthesis.md`

### Phase 3 — Plan (sequential, after Phase 2)

One subagent reads the synthesis + the current skill creation methodology. It designs the skill structure:

- Should this be a **delegation** skill (multi-agent workflow) or **methodology** skill (reference material)?
- What phases and agents does it need?
- What sources should it cite?
- How does it handle edge cases?

**Output:** `work/<skill-name>/plan.md`

### Phase 4 — Write (sequential, after Phase 3)

One subagent writes the final `skills/<name>/SKILL.md` file following the plan. The old methodology content about formatting is passed as reference.

**Output:** `skills/<name>/SKILL.md`

## Tradeoffs

| Factor | Before | After |
|---|---|---|
| Turn cost per skill | ~5-10 turns | ~20-40 turns |
| Source quality | None (LLM priors only) | Actual papers, docs, code |
| Recency ceiling | Training data cutoff | Whatever is findable today |
| Citation support | None | Full citations to real sources |
| Skill reliability | Generic advice | Grounded in current best practices |
| Execution time | ~5 minutes | ~15-30 minutes |

## Decisions

1. **GitHub search: optional.** Only included when the topic has clear software/tooling dimensions.
2. **Research artifacts: ephemeral.** Written to `work/<skill-name>/` and deleted after the skill is created. Not committed.
3. **Research phase can be skipped entirely.** For simple skills (e.g., a basic checklist, a rename, a single methodology reference), the orchestrator can choose a lightweight path: skip Phase 1 and 2, go straight to plan + write using the old methodology format as reference. This is a judgment call the orchestrator makes based on the complexity of the request.