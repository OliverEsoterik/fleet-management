# Market Research & GTM Strategy Methodology

## Purpose

Produce market research and go-to-market strategy that answers the investor's key questions:
1. **How big is the market?** (TAM, SAM, SOM)
2. **Who are the competitors?** (and why you'll win)
3. **How will you get customers?** (GTM, sales, marketing)
4. **What are the unit economics?** (LTV, CAC, payback)

## Process

### Step 1: Read the idea brief

Read `work/whitepaper/idea-brief.md`. Understand the industry, target customers, and stage.

### Step 2: TAM / SAM / SOM

**TAM (Total Addressable Market):** The total revenue opportunity if every potential customer bought your product. Use top-down (industry reports, analyst data) and bottom-up (number of potential customers × average revenue per customer).

**SAM (Serviceable Addressable Market):** The portion of TAM your product/service can actually reach given your business model, geography, and distribution channel.

**SOM (Serviceable Obtainable Market):** The portion of SAM you can realistically capture in the near term (3-5 years). Based on sales capacity, marketing budget, and competitive dynamics.

Format:
```
TAM: $X billion — [source, methodology]
SAM: $X million — [source, methodology]
SOM: $X million — [source, methodology]
```

### Step 3: Competitor landscape

Categorize competitors:

**Direct competitors:** Same problem, same solution approach
- What they do
- How they do it
- What they're missing (the gap you fill)
- Their funding, revenue, team size (if known)

**Indirect competitors:** Same problem, different solution approach
- How they solve the problem differently
- Why customers might choose them over you
- The switching cost for customers to move to you

**Future competitors:** Companies that could enter your space
- Adjacent companies with relevant capabilities
- Tech giants that could build a competing solution
- Startups in adjacent spaces that could pivot

### Step 4: Competitive positioning

For each differentiator, explain:
- **What it is** (specific capability)
- **Why it matters** (customer benefit)
- **How sustainable it is** (how long before competitors copy it)
- **Evidence** (customer feedback, technical validation, data)

Use a positioning matrix:
```
              | Us | Competitor A | Competitor B |
|-------------|----|--------------|--------------|
| Feature 1   | ✅ | ❌           | ✅           |
| Feature 2   | ✅ | ✅           | ❌           |
| Feature 3   | ✅ | ❌           | ❌           |
| Price       | $$ | $$$          | $            |
```

### Step 5: Customer persona

Create 1-2 detailed customer personas:
- Demographics (company size, industry, role, budget)
- Pain points (what keeps them up at night)
- Current solution (what they use now, why they hate it)
- Decision criteria (what matters most in choosing a solution)
- Buying process (who decides, what's the approval chain)
- Budget (what they're willing to pay, what they pay now)

### Step 6: Go-to-market strategy

**Channel strategy:**
- Direct sales (enterprise, high-touch, long cycle)
- Self-serve (product-led growth, low-touch)
- Channel partners (resellers, agencies, consultants)
- Marketplace (app store, platform distribution)
- Strategic partnerships (integrations, co-marketing)

**Why this channel?** What's the evidence it will work?

### Step 7: Customer acquisition

For each acquisition channel:
- **Channel** (content marketing, paid ads, sales outreach, referrals, partnerships)
- **CAC** (estimated cost per acquisition, with rationale)
- **Volume** (how many customers per month at maturity)
- **Scalability** (will CAC increase or decrease as you scale?)
- **Timeline** (how long from first touch to paying customer)

### Step 8: Pricing strategy

**Model:** Subscription / Usage-based / One-time / Freemium / Hybrid
**Why this model?** How does it align with customer value?
**Tiers:** What are the tiers, what's in each, what's the price?
**Benchmarks:** How does this compare to competitors?

### Step 9: Sales strategy

- Sales model (inbound, outbound, channel, enterprise)
- Sales cycle length (from first contact to closed deal)
- Deal size (average contract value)
- Sales team structure (how many reps, what comp)
- Key metrics (conversion rate, win rate, pipeline velocity)

### Step 10: Marketing plan

- Content marketing (blog, whitepapers, case studies, webinars)
- PR and thought leadership (conferences, awards, media)
- Demand generation (ads, SEO, email, events)
- Community building (user groups, forums, open source)

### Step 11: Key metrics

| Metric | Target | Benchmark | Rationale |
|--------|--------|-----------|-----------|
| LTV | $X | Industry avg $Y | [calculation] |
| CAC | $X | Industry avg $Y | [calculation] |
| LTV/CAC | 3:1 | Healthy >3:1 | [calculation] |
| Churn (monthly) | X% | Industry avg Y% | [rationale] |
| NPS | X | Industry avg Y | [rationale] |
| Conversion rate | X% | Industry avg Y% | [rationale] |

## Output Format

Write to `work/whitepaper/market.md`:

```markdown
# Market Research & GTM Strategy: [Business Name]

## Market Size
TAM: $X
SAM: $X
SOM: $X

## Competitor Landscape
[Direct, indirect, future competitors]

## Competitive Positioning
[Differentiation matrix + sustainability analysis]

## Customer Persona
[Persona details]

## Go-to-Market Strategy
[Channels, why, evidence]

## Customer Acquisition
[Channel breakdown with CAC, volume, scalability]

## Pricing Strategy
[Model, tiers, benchmarks]

## Sales Strategy
[Model, cycle, deal size, team]

## Marketing Plan
[Content, PR, demand gen, community]

## Key Metrics
[Table with targets and benchmarks]
```

## Quality Checks

- [ ] TAM/SAM/SOM have clear sources and methodology
- [ ] Competitor analysis is specific (not "they're all bad")
- [ ] Each differentiator has a sustainability assessment
- [ ] Customer persona is detailed enough to build a marketing plan
- [ ] GTM channel is justified (not "we'll do everything")
- [ ] CAC and LTV have explicit calculations, not just numbers
- [ ] Pricing is benchmarked against competitors