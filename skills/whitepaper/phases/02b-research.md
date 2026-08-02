# Technical Research Methodology

## Purpose

Search arXiv and GitHub for relevant academic papers and open-source implementations to support the technical analysis. The goal is to ground the whitepaper's technical claims in real research and existing work — not to inflate the reference count, but to show investors that the approach is grounded in established science and engineering practice.

**Output:** `work/whitepaper/research.md` — a curated reference document with full citation data, including BibTeX entries ready for the whitepaper's bibliography.

## Process

### Step 1: Read the idea brief

Read `work/whitepaper/idea-brief.md`. Understand:
- The problem domain and proposed solution
- The industry/sector classification (SaaS, deep tech, biotech, etc.)
- The core technical innovation areas
- Key technologies mentioned or implied

### Step 2: Generate search queries

From the idea brief, derive 3-5 search queries for arXiv and 2-3 for GitHub.

**Query design rules:**

| Source | Style | Example |
|--------|-------|---------|
| arXiv | Simple keywords, technical terms. Search titles + abstracts. | "transformer attention mechanism protein folding" not "how does AI help fold proteins" |
| GitHub | Repo-describing terms. Focus on project/topic names. | "distributed kv store go" not "write a key value store in go" |

**Query areas to cover:**
- Core technology (e.g., "transformer architecture", "federated learning", "homomorphic encryption")
- Problem domain (e.g., "medical image segmentation", "real-time bidding algorithm")
- Related implementations (e.g., "RAG pipeline", "vector database", "LLM fine-tuning")
- Evaluation benchmarks (e.g., "GLUE benchmark", "MLPerf inference")

### Step 3: Search arXiv

For each arXiv query, run:

```bash
bash skills/research/tools/search-arxiv.sh "<query>" 10
```

The tool outputs markdown to stdout with:
- Paper title, authors, publication date, categories
- arXiv URL and DOI (if available)
- Abstract (first 500 characters)

Save the output of each query to a temporary file. Collect all results.

**Selection criteria — keep a paper if:**
- It directly addresses the core technology or problem domain
- It provides a foundation for the proposed solution
- It establishes the state of the art that the startup improves upon
- It validates the feasibility of the approach

**Discard if:**
- It's tangentially related (same buzzwords, different problem)
- It's clearly outdated (>5 years old for fast-moving fields like ML)
- The abstract doesn't actually support the technical narrative

### Step 4: Search GitHub

For each GitHub query, run:

```bash
bash skills/research/tools/search-github.sh "<query>" 10
```

The tool outputs markdown to stdout with:
- Repository name, description, stars, forks, language
- Created/updated dates, license
- URL

**Selection criteria — keep a repo if:**
- It's a relevant implementation or framework in the same domain
- It has meaningful stars (>50) or is from a recognized organization
- It demonstrates that the approach is feasible (existing work proves it)
- It shows the competitive landscape (what exists, what's missing)

**Discard if:**
- It's a tutorial or course project (not production-quality)
- It's a fork with no meaningful changes
- It's unrelated to the technical approach

### Step 5: Deduplicate and organize

Merge results from all queries. Remove duplicates (same paper or repo appearing in multiple queries). Organize by theme:

1. **Foundational research** — papers that establish the scientific basis
2. **State of the art** — recent work that the startup improves upon or extends
3. **Existing implementations** — open-source repos that demonstrate feasibility
4. **Competitive landscape** — existing solutions the startup differentiates from

### Step 6: Write the research output

Write to `work/whitepaper/research.md`:

```markdown
# Technical Research: [Business Name]

## Research Queries
- arXiv: [query 1], [query 2], ...
- GitHub: [query 1], [query 2], ...

## Summary
[3-5 sentence summary of what the research found and how it supports the technical analysis]

## Foundational Research

### [Paper Title]
- **Authors:** [Author list]
- **Year:** [Year]
- **Venue:** [arXiv / conference / journal]
- **arXiv ID:** [ID, e.g., 2301.12345]
- **URL:** [Link]
- **Relevance:** [Why this paper matters for the proposed solution — 1-2 sentences]
- **Key insight:** [The specific finding that supports the technical approach]

**BibTeX:**
```bibtex
@misc{key,
  author = {Last, First and Last, First},
  title = {Paper Title},
  year = {2023},
  eprint = {2301.12345},
  archivePrefix = {arXiv},
}
```

---

### [Paper Title]
...

## State of the Art

[Same format as above — papers showing current best practices]

## Existing Implementations

### [owner/repo]
- **Description:** [What it does]
- **Stars:** [N]  **Language:** [Lang]
- **URL:** [Link]
- **Relevance:** [Why this implementation matters — 1-2 sentences]
- **Key takeaway:** [What the startup can learn from or build upon]

**BibTeX:**
```bibtex
@misc{owner-repo,
  author = {Owner or Organization},
  title = {Repository Name},
  year = {2023},
  howpublished = {\url{https://github.com/owner/repo}},
}
```

---

### [owner/repo]
...

## Competitive Landscape
[Existing solutions and how they relate to the proposed approach]
```

### Step 7: Quality checks

Before finishing:
- [ ] Every paper has a complete BibTeX entry (author, title, year, arXiv ID)
- [ ] Every GitHub repo has a complete BibTeX entry (author, title, URL)
- [ ] Every entry has a "Relevance" field explaining why it matters
- [ ] The research is organized by theme, not by query
- [ ] No duplicate entries
- [ ] The summary tells the reader what the research means for the whitepaper