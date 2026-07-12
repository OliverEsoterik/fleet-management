---
name: create-skill
description: >
  Create a new skill in the project. Runs research (optional), synthesis,
  planning, and writing phases. Supports both research-backed creation for
  complex skills and lightweight creation for simple ones.
---

# Create Skill — Delegation

## Overview

This is a **delegation skill**. The orchestrator reads the `## Delegation` section below and executes it.

The workflow has two modes:

- **Full mode** (default for complex/novel topics): Phase 1 research (parallel), Phase 2 synthesis, Phase 3 plan, Phase 4 write
- **Lightweight mode** (simple skills like checklists, renames, single methodology): Skip Phases 1-2, go straight to Phase 3 plan + Phase 4 write

The orchestrator decides which mode based on the request. If the user says "create a quick skill for X" or the topic is trivially simple, use lightweight mode. Otherwise use full mode.

### Cleanup

Research artifacts in `work/<skill-name>/` are ephemeral. The orchestrator deletes them after the skill file is written.

---

## Delegation

**Orchestrator reads this section and executes it.**

### Mode Selection

Check the request:

- **Full mode:** Topic is complex, domain-specific, evolving, or has a body of research/practice behind it (e.g., "real-time bidding", "HIPAA compliance checklist", "DCF valuation")
- **Lightweight mode:** Topic is simple, well-known, a rename, a basic checklist, or the user explicitly says "quick" or "simple" (e.g., "review JSON files", "add a linter config", "rename a function")

If lightweight mode, skip to Phase 3.

---

### Phase 1 — Research (parallel, full mode only)

Launch all research agents with `run_in_background: true`. They write to `work/<skill-name>/research/`.

| Agent | Sources | Output |
|-------|---------|--------|
| Academic researcher | Semantic Scholar, arXiv | `work/<skill-name>/research/academic.md` |
| Web researcher | General web search, official docs, tutorials, best practices | `work/<skill-name>/research/web.md` |
| (Optional) GitHub researcher | GitHub search for tools, libraries, implementations | `work/<skill-name>/research/github.md` |
| (Optional) Historical researcher | Archive.org, Google Scholar for niche/older context | `work/<skill-name>/research/historical.md` |

Omit the optional researchers if the topic has no clear software/historical dimension.

- **Agent: academic-researcher**
  Role: You are an academic research specialist. Search Semantic Scholar and arXiv for the most relevant papers on this topic. Focus on: survey papers, recent developments (last 3 years), seminal papers, and any standards or specifications. For each paper, note: title, authors, year, key contributions, and why it matters for someone building a practical skill on this topic. Do NOT fabricate paper details — if a search returns nothing, say so.
  Skills: []
  Output: `work/<skill-name>/research/academic.md`

- **Agent: web-researcher**
  Role: You are a web research specialist. Search the web for the best practical resources on this topic. Look for: official documentation, tutorials, best practice guides, blog posts from recognized experts, community standards, and common pitfalls. Summarize each source with: title, URL, key takeaways, and relevance for skill creation. Prefer authoritative sources (docs, standards bodies, established practitioners) over random blogs.
  Skills: []
  Output: `work/<skill-name>/research/web.md`

- **Agent: github-researcher** (optional)
  Role: You are a GitHub research specialist. Search GitHub for the most relevant repositories, tools, libraries, and reference implementations on this topic. Look for: starred repos, active projects, well-documented implementations, and community standards. For each result, note: repo name, stars, description, language, and what makes it relevant. If no meaningful results, say so.
  Skills: []
  Output: `work/<skill-name>/research/github.md`

- **Agent: historical-researcher** (optional)
  Role: You are a historical research specialist. Search Archive.org, Google Scholar, and other sources for historical context, foundational work, or niche references on this topic. Focus on: origins of the field, classic papers, older but still-relevant standards, and perspectives that modern sources might miss. If the topic is too recent for historical context, say so.
  Skills: []
  Output: `work/<skill-name>/research/historical.md`

---

### Phase 2 — Synthesize (sequential, after Phase 1, full mode only)

- **Agent: synthesis-writer**
  Role: You are a research synthesis specialist. Read all research output files from `work/<skill-name>/research/`. Produce a consolidated reference document that includes: unified terminology and conceptual model, ranked list of most important findings (by relevance to someone building a practical skill), conflicts or contradictions between sources, recommendations for what the skill should cover, key citations the skill should reference, and gaps where no good sources were found. Be concise — this is not a dump, it's a curated briefing.
  Skills: []
  Output: `work/<skill-name>/synthesis.md`

---

### Phase 3 — Plan (sequential, after Phase 2)

- **Agent: skill-planner**
  Role: You are a skill architect. You will design the structure of a new skill file.
  
  **In full mode:** Read `work/<skill-name>/synthesis.md` for the research foundation.
  
  **In lightweight mode:** No research available — rely on general knowledge and the methodology reference below.
  
  Design the skill according to these rules:
  
  1. **Choose the type:** delegation skill (multi-agent workflow with phases) or methodology skill (reference material, step-by-step instructions)
  2. **Name it carefully** — the name is what the orchestrator matches against user requests. It should be something someone might naturally say: "review terraform", "dcf", "create skill"
  3. **If delegation:** design phases with agents, roles, skills references, and output paths
  4. **If methodology:** design clear step-by-step instructions a subagent can follow
  5. **Frontmatter format:**
     ```yaml
     ---
     name: ... (user-facing name, what the orchestrator matches)
     description: > ... (one-line summary)
     ---
     ```
  
  Write the plan to `work/<skill-name>/plan.md`.
  
  Skills: [create-skill]  (read this skill's SKILL.md for formatting rules)
  Output: `work/<skill-name>/plan.md`

---

### Phase 4 — Write (sequential, after Phase 3)

- **Agent: skill-writer**
  Role: You are a skill writer. Read `work/<skill-name>/plan.md` and write the final skill file at `skills/<name>/SKILL.md`.

  Follow the plan exactly. Use the formatting conventions from the create-skill methodology reference:
  
  - Delegation skills start with a `## Delegation` section with phases, agents, roles, skills, outputs
  - Methodology skills start with a `## Overview` and provide step-by-step instructions
  - Output paths use `work/<topic>/<file>.md` convention
  - Subagents use `Agent` tool with `subagent_type`, role, skills references
  
  Write the complete file. Return the path to the created file.
  
  Skills: [create-skill]  (read this skill's SKILL.md for formatting rules)
  Output: `skills/<name>/SKILL.md`
  
  After confirming the file was written successfully, clean up `work/<skill-name>/` by deleting it.

---

### After All Phases

1. Verify the skill file exists at `skills/<name>/SKILL.md`
2. Delete `work/<skill-name>/` directory (ephemeral research artifacts)
3. Report to user: what was created, what type it is, where it lives, and any notable decisions made during the process