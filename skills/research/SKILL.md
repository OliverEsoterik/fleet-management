---
name: research
description: >
  Multi-source research skill. Scans specified sources (arxiv, github, pubmed,
  archive, web) in parallel using dedicated search tools, then produces a
  consolidated research report. Sources are opt-in — specify which to scan.
---

# Research — Multi-Source Parallel Search & Synthesis

## Overview

This skill lets you scan multiple research sources in parallel for a given
query and produce a consolidated report. You specify which sources to search;
each source is handled by a dedicated tool call.

**Designed for extensibility:** adding a new source means creating one tool
script in `skills/research/tools/search-<source>.sh` and adding one entry to
the source table below. No other code changes needed.

---

## Source Table

| Source | Tool | Requires | Notes |
|--------|------|----------|-------|
| `arxiv` | `search-arxiv.sh` | `curl`, `python3` | Free XML API, no auth. Broad academic coverage (CS, math, physics, stats, etc.) |
| `github` | `search-github.sh` | `gh` CLI (authenticated) | GitHub repos. Requires `gh auth login`. |
| `pubmed` | `search-pubmed.sh` | `curl`, `python3` | Free NCBI EUtils API, no auth. Life sciences, medicine, genomics. |
| `archive` | `search-archive.sh` | `curl`, `python3` | Archive.org. Good for historical/primary sources, not academic papers. |
| `web` | *(subagent uses WebSearch tool)* | Agent-level `WebSearch` | General web search. Only available as an agent tool, not a bash script. |

**Sources not implemented yet** (blocking issues noted):

| Source | Reason Skipped |
|--------|---------------|
| semantic-scholar | 429 rate-limited without API key |
| ssrn | 403 — blocks programmatic access |
| google-scholar | Aggressively blocks scraping |
| google-books | Requires API key for reliable access |

---

## Graph

**The orchestrator reads this section and executes it.**

### Usage

```
/skill:research "linux kernel schedulers" --sources=arxiv,github
/skill:research "CRISPR gene editing ethics" --sources=pubmed,web
/skill:research "19th century telegraph systems" --sources=archive,web,arxiv
```

If `--sources` is omitted, default to `arxiv,github,pubmed,web`.

### Nodes

  - name: source-validator
    trigger: nodes.source-validator.status == "ready"
    input: [user_request]
    role: >
      Validate the requested sources against the source table and set up the
      output directory structure. Parse `--sources` from the user request
      (comma-separated). Default to `arxiv,github,pubmed,web` if omitted.

      For each source: check it exists in the source table above. If an
      unknown source is specified, warn and skip it.

      Create `work/research/` directory structure:
      ```
      work/research/
      ├── sources/     ← individual source outputs
      └── report/      ← final report
      ```

      Announce the plan to the user with a numbered list of sources and
      estimated phases, then wait for confirmation (y/n). Write the validated
      source list and confirmation result to the output path.
    skills: []
    output: work/research/sources-validated.md
    route: always -> query-refiner

  - name: query-refiner
    trigger: route("source-validator")
    input: [user_request]
    role: >
      You are a research query strategist. Your job is to take the user's
      research topic and produce one refined query per requested source.
      Different sources optimize for different query styles. Write the result
      to the output path.

      Rules for query refinement:
      - **arxiv:** Use simple keywords. arXiv's API searches titles, abstracts,
        and authors. Example: "transformer attention mechanism" not "What is
        the attention mechanism in transformers?"
      - **github:** Use repo-describing keywords. GitHub search works best
        with project names, topics, and descriptive terms.
      - **pubmed:** PubMed uses MeSH-aware search. Technical/medical
        terminology works well. Example: "machine learning genomics" not "how
        is ML used in genomics"
      - **archive:** General keywords — Archive.org's search is broad.
      - **web:** Natural language questions or full sentences work well with
        WebSearch.

      Output format (markdown):
      ```markdown
      # Refined Queries for: <original query>

      ## arxiv
      <refined query>

      ## github
      <refined query>

      ## pubmed
      <refined query>
      ```
    skills: []
    output: work/research/queries.md
    route: always -> query-refiner-done  # signals completion; 5 researcher nodes trigger on route("query-refiner")

  - name: arxiv-researcher
    trigger: route("query-refiner")
    input: [user_request]
    role: >
      You are an arXiv research specialist. Read `work/research/queries.md`
      and find the query for the `arxiv` source. Run the search tool and save
      the results.

      Tool: `bash skills/research/tools/search-arxiv.sh "<query>" <max_results>`
      Where `<max_results>` defaults to 10. Pipe stdout to a markdown file.
    skills: []
    output: work/research/sources/arxiv.md
    route: always -> synthesis-writer

  - name: github-researcher
    trigger: route("query-refiner")
    input: [user_request]
    role: >
      You are a GitHub research specialist. Read `work/research/queries.md`
      and find the query for the `github` source. Run the search tool and
      save the results.

      Tool: `bash skills/research/tools/search-github.sh "<query>" <max_results>`
      Where `<max_results>` defaults to 10.
    skills: []
    output: work/research/sources/github.md
    route: always -> synthesis-writer

  - name: pubmed-researcher
    trigger: route("query-refiner")
    input: [user_request]
    role: >
      You are a PubMed research specialist. Read `work/research/queries.md`
      and find the query for the `pubmed` source. Run the search tool and
      save the results.

      Tool: `bash skills/research/tools/search-pubmed.sh "<query>" <max_results>`
      Where `<max_results>` defaults to 10.
    skills: []
    output: work/research/sources/pubmed.md
    route: always -> synthesis-writer

  - name: archive-researcher
    trigger: route("query-refiner")
    input: [user_request]
    role: >
      You are an Archive.org research specialist. Note: Archive.org is best
      for historical documents, primary sources, books, and media — not
      academic papers. Search terms should be broad.

      Read `work/research/queries.md` and find the query for the `archive`
      source. Run the search tool and save the results.

      Tool: `bash skills/research/tools/search-archive.sh "<query>" <max_results>`
      Where `<max_results>` defaults to 10.
    skills: []
    output: work/research/sources/archive.md
    route: always -> synthesis-writer

  - name: web-researcher
    trigger: route("query-refiner")
    input: [user_request]
    role: >
      You are a web research specialist. Read `work/research/queries.md` and
      find the query for the `web` source. Since web search is only available
      via agent-level tools, use the WebSearch tool directly. Search for the
      refined query, read the most relevant results, and synthesize them.

      Tool: _not a bash script_ — use the built-in `WebSearch` tool in your
      agent toolkit. You can also use `WebFetch` to read pages.

      Constraints: Do NOT exceed 15 web requests total. Focus on quality over
      quantity: find the 3-5 best sources and summarize them well.
    skills: []
    output: work/research/sources/web.md
    route: always -> synthesis-writer

  - name: synthesis-writer
    trigger: route("arxiv-researcher") AND route("github-researcher") AND
      route("pubmed-researcher") AND route("archive-researcher") AND
      route("web-researcher")
    input: [user_request]
    role: >
      You are a research synthesis specialist. Read all source output files
      from `work/research/sources/`. Produce a consolidated markdown reference
      that includes:

      1. **Unified summary** — what the research found, organized by theme,
         not by source
      2. **Key findings** — the most important discoveries, patterns, or
         disagreements across sources (ranked by relevance)
      3. **Gaps** — what was NOT found that would be useful
      4. **Source-by-source notes** — brief notes on what each source
         contributed and any limitations (e.g., "GitHub search was noisy due
         to many forks")

      Be concise. This is a curated briefing, not a dump.
    skills: []
    output: work/research/synthesis.md
    route: always -> report-writer

  - name: report-writer
    trigger: route("synthesis-writer")
    input: [user_request]
    role: >
      You are a research report writer. Read `work/research/synthesis.md`
      and write a polished final report to the output path.

      The report should be:
      - Well-structured with sections and sub-sections
      - Written for a technical audience (the person who requested this
        research)
      - Actionable — include recommendations for next steps, further reading,
        or areas that need more investigation
      - Include source attribution (where each finding came from)

      Optional: If any source tool output raw markdown in
      `work/research/sources/` that contains paper abstracts or detailed
      metadata, reference it rather than duplicating.
    skills: []
    output: work/research/report/report.md
    route: always -> cleanup

  - name: cleanup
    trigger: route("report-writer")
    input: [user_request]
    role: >
      Delete the `work/research/sources/` and `work/research/queries.md`
      files (intermediate artifacts). Keep `work/research/synthesis.md` and
      `work/research/report/report.md`.

      Report final status to the user: what sources were searched, what was
      produced, and where the report lives.
    skills: []
    output: work/research/cleanup-done.md
    route: always -> consolidator

---

## Adding a New Source

1. Create `skills/research/tools/search-<name>.sh`
   - Accepts query as first argument, max results as optional second argument
   - Outputs markdown to stdout
   - Fails gracefully on error (exit code 1, error message to stdout)
   - Dependencies: only `curl`, `python3`, and optionally one CLI tool

2. Add one row to the **Source Table** in this SKILL.md

3. Add one entry in the `## Graph` section with a researcher node for that
   source, with `trigger: route("query-refiner")` and
   `route: always -> synthesis-writer`

That's it. Neither the orchestration logic nor the other tools need changes.

---

## Design Decisions

- **Tools are standalone bash scripts** — no dependencies on other files in
  this repo. Each can be copied elsewhere and used independently.
- **Sources are opt-in** — the user specifies which sources to search. This
  avoids expensive/wasteful searches (e.g., you probably don't want
  Archive.org for a compilers research question).
- **Web search uses agent tools, not bash** — because `WebSearch` is only
  available as an agent-level tool. The subagent handles it inline.
- **PubMed as bonus source** — not in the original request, but it's a free,
  high-quality API with no auth. Worth including given the academic research
  context.