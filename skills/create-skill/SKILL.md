---
name: create-skill
description: >
  Create a new skill in the project. Runs research (optional), synthesis,
  planning, and writing phases. Supports both research-backed creation for
  complex skills and lightweight creation for simple ones.
---

# Create Skill — Graph

## Overview

This is a **graph skill**. The orchestrator reads the `## Graph` section below,
registers the nodes, and routes through them.

The workflow has two modes:

- **Full mode** (default for complex/novel topics): Phase 1 research (parallel),
  Phase 2 synthesis, Phase 3 plan, Phase 4 write
- **Lightweight mode** (simple skills like checklists, renames, single
  methodology): Skip Phases 1-2, go straight to Phase 3 plan + Phase 4 write

The orchestrator decides which mode based on the request. If the user says
"create a quick skill for X" or the topic is trivially simple, use lightweight
mode. Otherwise use full mode.

---

## Graph

### Mode Selection (Decomposer Decision)

The decomposer checks the request:

- **Full mode:** Topic is complex, domain-specific, evolving, or has a body of
  research/practice behind it (e.g., "real-time bidding", "HIPAA compliance
  checklist", "DCF valuation"). Sets the Phase 1 research nodes and
  `research-gate` status to `"ready"`.
- **Lightweight mode:** Topic is simple, well-known, a rename, a basic
  checklist, or the user explicitly says "quick" or "simple" (e.g., "review
  JSON files", "add a linter config", "rename a function"). Sets
  `skill-planner` status to `"ready"` directly.

### Nodes

Nodes:
  - name: academic-researcher
    trigger: nodes.academic-researcher.status == "ready"
    input: [user_request, decomposition]
    role: >
      You are an academic research specialist. Search Semantic Scholar and
      arXiv for the most relevant papers on this topic. Focus on: survey
      papers, recent developments (last 3 years), seminal papers, and any
      standards or specifications. For each paper, note: title, authors, year,
      key contributions, and why it matters for someone building a practical
      skill on this topic. Do NOT fabricate paper details — if a search
      returns nothing, say so.
    skills: []
    output: work/<skill-name>/research/academic.md
    route: always -> research-gate

  - name: web-researcher
    trigger: nodes.web-researcher.status == "ready"
    input: [user_request, decomposition]
    role: >
      You are a web research specialist. Search the web for the best practical
      resources on this topic. Look for: official documentation, tutorials,
      best practice guides, blog posts from recognized experts, community
      standards, and common pitfalls. Summarize each source with: title, URL,
      key takeaways, and relevance for skill creation. Prefer authoritative
      sources (docs, standards bodies, established practitioners) over random
      blogs.
    skills: []
    output: work/<skill-name>/research/web.md
    route: always -> research-gate

  - name: github-researcher
    trigger: nodes.github-researcher.status == "ready"
    input: [user_request, decomposition]
    role: >
      You are a GitHub research specialist. Search GitHub for the most relevant
      repositories, tools, libraries, and reference implementations on this
      topic. Look for: starred repos, active projects, well-documented
      implementations, and community standards. For each result, note: repo
      name, stars, description, language, and what makes it relevant. If no
      meaningful results, say so.
    skills: []
    output: work/<skill-name>/research/github.md
    route: always -> research-gate

  - name: historical-researcher
    trigger: nodes.historical-researcher.status == "ready"
    input: [user_request, decomposition]
    role: >
      You are a historical research specialist. Search Archive.org, Google
      Scholar, and other sources for historical context, foundational work, or
      niche references on this topic. Focus on: origins of the field, classic
      papers, older but still-relevant standards, and perspectives that modern
      sources might miss. If the topic is too recent for historical context,
      say so.
    skills: []
    output: work/<skill-name>/research/historical.md
    route: always -> research-gate

  - name: research-gate
    trigger: nodes.research-gate.status == "ready"
    input: []
    role: >
      No-op gate node. Set to "ready" by the decomposer after all Phase 1
      research nodes have been dispatched. When the last research node
      completes, its route points here — the orchestrator checks that all
      research nodes are done before launching synthesis-writer. If no
      research nodes were launched (all skipped), routes directly to
      synthesis-writer. The orchestrator handles this — no sub-agent is
      launched.
    skills: []
    output: work/graph/output/research-gate/done.txt
    route: always -> synthesis-writer

  - name: synthesis-writer
    trigger: route("research-gate")
    input: [user_request]
    role: >
      You are a research synthesis specialist. Read all research output files
      from `work/<skill-name>/research/`. Produce a consolidated reference
      document that includes: unified terminology and conceptual model, ranked
      list of most important findings (by relevance to someone building a
      practical skill), conflicts or contradictions between sources,
      recommendations for what the skill should cover, key citations the skill
      should reference, and gaps where no good sources were found. Be concise
      — this is not a dump, it's a curated briefing.
    skills: []
    output: work/<skill-name>/synthesis.md
    route: always -> skill-planner

  - name: skill-planner
    trigger: nodes.skill-planner.status == "ready"
    input: [user_request]
    role: >
      You are a skill architect. You will design the structure of a new skill
      file.

      If a synthesis document exists at `work/<skill-name>/synthesis.md`,
      read it for the research foundation. If it doesn't exist (lightweight
      mode), no research available — rely on general knowledge.

      Design the skill according to these rules:

      1. Choose the type: graph skill (multi-node workflow with triggers,
         routes, and roles) or methodology skill (reference material,
         step-by-step instructions) or data provider (bash scripts)
      2. Name it carefully — the name is what the orchestrator matches against
         user requests. It should be something someone might naturally say:
         "review terraform", "dcf", "create skill"
      3. If graph: design nodes with name, trigger, input, role, skills,
         output, and route fields. See `skills/orchestrator/SKILL.md`
         section 2 for the node format.
      4. If methodology: design clear step-by-step instructions a subagent
         can follow
      5. Frontmatter format:
         ```yaml
         ---
         name: ... (user-facing name, what the orchestrator matches)
         description: > ... (one-line summary)
         skills: []  # optional — skills this one wraps or depends on
         tools: Read, Write, Bash  # optional — tools the sub-agent needs
         ---
         ```
         Note: `model` is NOT a skill field. Model pinning is done via
         agents (`agents/<name>.md`), not skills.

      6. If the skill is a methodology that produces a specific type of
         output, document it in the `produces` field of the orchestrator's
         skill_index (e.g., `produces: [analysis, adr, plan]`). This is
         used by the chain-planner for dependency resolution.
    skills: [create-skill]
    output: work/<skill-name>/plan.md
    route: always -> skill-writer

  - name: skill-writer
    trigger: route("skill-planner")
    input: [user_request]
    role: >
      You are a skill writer. Read `work/<skill-name>/plan.md` and write the
      final skill file at the path specified in the plan.

      Follow the plan exactly. Use the formatting conventions from the
      create-skill methodology reference:

      - Graph skills start with a `## Graph` section with nodes (name,
        trigger, input, role, skills, output, route). See
        `skills/orchestrator/SKILL.md` section 2 for the canonical format.
      - Methodology skills start with a `## Overview` and provide step-by-step
        instructions
      - Output paths use `work/<topic>/<file.md>` convention
      - Frontmatter: `name`, `description`, optional `skills` and `tools`.
        Do NOT add `model` — that belongs in agent frontmatter.
      - If user also wants an agent wrapper for model pinning, create
        `agents/<name>.md` with frontmatter: `name`, `description`,
        `skills: [<skill-name>]`, `model`, `tools`. See
        `agents/gitops-expert.md` for an example.
      - Subagents use `Agent` tool with `subagent_type`, role, skills references

      Write the complete file. Return the path to the created file.

      After confirming the file was written successfully, clean up
      `work/<skill-name>/` by deleting it.
    skills: [create-skill]
    output: <from-plan>  # resolved at runtime from plan.md
    route: always -> cleanup

  - name: cleanup
    trigger: route("skill-writer")
    input: []
    role: >
      Delete the `work/<skill-name>/` directory (ephemeral research artifacts).
      Verify the skill file exists at the path specified in the plan. Report
      to user: what was created, what type it is, where it lives, and any
      notable decisions made during the process.
    skills: []
    output: work/graph/output/cleanup/done.txt
    route: always -> consolidator

### Routing Summary

```
research-gate (set ready by decomposer in full mode, launches parallel:
               academic-researcher, web-researcher,
               github-researcher*, historical-researcher*)
  |              * optional — decomposer may omit these nodes
  v
synthesis-writer (reads research/*.md, writes synthesis.md)
  |
  v
skill-planner (reads synthesis.md if exists, writes plan.md)
  |
  v
skill-writer (reads plan.md, writes SKILL.md)
  |
  v
cleanup (deletes work/<skill-name>/, reports results)
  |
  v
consolidator (built-in terminal node)
```

In lightweight mode, the decomposer sets `skill-planner` to `"ready"` directly,
skipping all Phase 1-2 nodes. The routing goes from `skill-planner` through
`skill-writer` to `cleanup` as normal.

### Research Node Selection (Decomposer Decision)

The optional researchers (github-researcher, historical-researcher) are omitted
if the topic has no clear software or historical dimension. The decomposer
simply does not set those nodes to `"ready"` in the shared state.

### Cleanup

Research artifacts in `work/<skill-name>/` are ephemeral. The `cleanup` node
deletes them after the skill file is written.
