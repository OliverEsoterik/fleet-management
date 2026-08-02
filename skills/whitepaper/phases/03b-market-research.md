# Market Data Research Methodology

## Purpose

Search the web for real market data, competitor intelligence, and industry reports to ground the market analysis in real-world information rather than assumptions. The goal is to find actual TAM/SAM/SOM figures, identify real competitors with their pricing and positioning, and gather industry benchmarks that investors will recognize.

**Output:** `work/whitepaper/market-research.md` — a curated reference document with market data, competitor profiles, and industry sources.

## Process

### Step 1: Read the idea brief

Read `work/whitepaper/idea-brief.md`. Understand:
- The industry/sector classification (SaaS, deep tech, biotech, finance, hardware, other)
- The target customer segments
- The proposed solution and its value proposition
- Key constraints (regulatory, competitive, timeline)

### Step 2: Generate search queries

From the idea brief, derive search queries for each area. Use the web search capability available in your environment.

**Market size queries:**
- "[industry] market size 2024 2025" or "[industry] TAM SAM"
- "[industry] market report" or "[industry] industry analysis"
- "[industry] growth rate CAGR"
- Better to search for specific analyst reports, e.g., "Gartner [industry] market forecast"

**Competitor queries:**
- "[industry] competitors" or "[industry] landscape"
- "[competitor name] pricing" or "[competitor name] funding"
- "top [industry] companies 2024"
- "Crunchbase [industry] startups"

**Industry benchmarks:**
- "[industry] SaaS benchmarks" or "[industry] gross margin"
- "[industry] customer acquisition cost" or "[industry] LTV"
- "[industry] churn rate benchmarks"

**Customer and market validation:**
- "[problem domain] survey" or "[problem domain] statistics"
- "[industry] customer pain points"
- "[industry] trends 2024 2025"

### Step 3: Search for market data

For each query, search the web. Select results that are:
- **Recent** (preferably 2023+; markets change fast)
- **Authoritative** (analyst firms, government statistics, reputable industry publications)
- **Specific** (actual numbers with methodology, not vague estimates)

**What to look for:**
- TAM/SAM/SOM figures with sources (Gartner, IDC, Forrester, Statista, PitchBook, CB Insights, government data)
- Market growth rates (CAGR projections)
- Number of potential customers (enterprises, SMBs, consumers)
- Average revenue per customer benchmarks
- Geographic market breakdowns

### Step 4: Research competitors

For each competitor found, search for:
- **Company details:** name, location, founding year, funding rounds, total funding
- **Product:** what they do, key features, target customers
- **Pricing:** pricing model (subscription, usage-based, enterprise), price points
- **Positioning:** how they describe themselves, their key differentiators
- **Market share:** estimated market share, revenue (if available)

**Format each competitor:**
```markdown
### [Competitor Name]
- **Website:** [URL]
- **Funding:** [Total funding, latest round, investors]
- **Description:** [What they do, 1-2 sentences]
- **Target customers:** [Enterprise/SMB/SME]
- **Pricing:** [Model and price range]
- **Differentiation:** [What they claim as their advantage]
- **Relevance:** [Why this competitor matters for the analysis]
```

### Step 5: Gather industry benchmarks

Search for industry-specific metrics:
- Typical gross margins for the industry
- Median CAC and LTV/CAC ratios
- Average contract values (ACV)
- Churn rates (monthly and annual)
- Sales efficiency metrics (magic number, payback period)
- Engineering salary benchmarks (for cost structure)

### Step 6: Write the research output

Write to `work/whitepaper/market-research.md`:

```markdown
# Market Research: [Business Name]

## Research Queries
- Market size: [list of queries]
- Competitors: [list of queries]
- Benchmarks: [list of queries]

## Summary
[3-5 sentence summary of key findings]

## Market Size
### TAM
- **Figure:** $X [billion/million]
- **Source:** [Source name, URL, date]
- **Methodology:** [How the source arrived at this figure]
- **Confidence:** [High/Medium/Low — and why]

### SAM
- **Figure:** $X [billion/million]
- **Source:** [Source name, URL, date]
- **Rationale:** [Why this portion of TAM is addressable]

### SOM
- **Figure:** $X [million]
- **Rationale:** [Realistic capture based on sales capacity, competition, timeline]

## Competitor Landscape
[Competitor profiles in the format from Step 4]

## Industry Benchmarks
| Metric | Industry Median | Source |
|--------|----------------|--------|
| Gross margin | X% | [Source] |
| CAC | $X | [Source] |
| LTV/CAC | Xx | [Source] |
| Monthly churn | X% | [Source] |
| ACV | $X | [Source] |

## Key Insights
[What the research means for the whitepaper — 3-5 bullet points]
```

### Step 7: Quality checks

Before finishing:
- [ ] Every market size figure has a named source (not "industry reports say")
- [ ] Competitor profiles include at least 3 real competitors with specific info
- [ ] Industry benchmarks are cited with sources
- [ ] The summary tells the reader what the research means for the whitepaper
- [ ] Queries are documented (for reproducibility)
- [ ] Confidence levels are honest (don't overclaim weak data)