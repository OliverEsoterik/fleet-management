---
name: peer-review
description: >
  Structured methodology for evaluating scientific manuscripts and grant
  proposals. Systematic multi-phase assessment covering research design,
  methodological rigor, statistical validity, reporting standards compliance,
  and constructive feedback. For code review, use the code-review skill.
skills: []
tools: Read, Write, Bash, Grep
---

# Peer Review

## Overview

Peer review is a structured evaluation of a scientific manuscript or grant
proposal. This skill provides a systematic framework for assessing research
quality, identifying strengths and weaknesses, and producing actionable
feedback that helps editors make decisions and authors improve their work.

The process is organized into six sequential phases, each with a distinct
evaluation lens. Complete them in order — later phases depend on judgments
formed in earlier ones.

**What this skill is not:** It does not evaluate software code (use the
code-review skill for that), perform statistical computations, or replace
domain expertise. It structures what you already know about evaluating
research into a repeatable process.

**Announce at start:** "I'm using the peer-review skill to evaluate this
manuscript."

## Review Phases

### Phase 1: First Pass — Scope and Signal

Goal: determine whether the manuscript warrants a full review or has fatal
flaws that make detailed review unnecessary.

Read the abstract, introduction (last paragraph), figures, and discussion
(first and last paragraphs). Do not read the full paper yet.

**Assess:**
- Is the research question clearly stated and worth answering?
- Are the conclusions supported by the data shown in the figures?
- Is there a fundamental fatal flaw that precludes publication (obvious
  confound, sample of 1, no controls, data not matching the conclusions)?
- Is the work appropriate for the venue (journal fit)?

**Decision gate:** If there is an unambiguous fatal flaw, summarize it in
one paragraph with the severity labeled "Fatal" and skip to Phase 6 (report
writing). Otherwise proceed through all phases.

**Output for this phase:** One sentence stating the research question and
one sentence stating initial impression. Keep it in working notes, not in
the final report.

### Phase 2: Structural Integrity

Goal: evaluate whether the manuscript is coherently structured and whether
each section does its job.

**Title and abstract:**
- Does the title accurately reflect the study without over-claiming?
- Does the abstract cover: background, objective, methods, key results,
  and conclusion — in that order?
- Is the abstract comprehensible to someone outside the immediate subfield?

**Introduction:**
- Does it establish why the research question matters (gap in knowledge,
  unresolved controversy, practical need)?
- Does it cite the relevant prior work without omitting opposing views?
- Does the last paragraph clearly state the hypothesis or objective?

**Methods:**
- Can you trace what was done from description alone? If not, what is missing?
- Are the key methodological choices justified (why this model, this sample
  size, this statistical test)?

**Results:**
- Do the results follow the order established in the methods?
- Are negative or null results reported alongside positive ones?

**Discussion:**
- Does the first paragraph restate the main finding without introducing new
  results?
- Are limitations discussed in their own section, not buried in the middle?
- Are the conclusions bounded by what the data actually show?

**References:**
- Are recent (last 3-5 years) relevant papers cited?
- Is there balanced citation of competing viewpoints?
- Is self-citation proportionate?

### Phase 3: Methodological Rigor

Goal: assess whether the research design can support the conclusions drawn.

**Study design:**
- Is the design appropriate for the research question (randomized trial vs
  observational, case-control vs cohort, in vitro vs in vivo)?
- Are the primary and secondary endpoints clearly defined?
- Is there evidence of pre-registration (clinical trials, registered reports)?

**Sample and power:**
- Is the sample size justified (power analysis, prior studies, resource
  constraints)?
- Are inclusion and exclusion criteria specified?
- Is there evidence of selection bias?

**Controls:**
- Are positive and negative controls present and appropriate?
- Are there unaccounted confounders?
- Are batch effects, technical variation, or known artifacts addressed?

**Replication:**
- Are there biological replicates (independent samples) vs technical
  replicates (same sample measured multiple times)?
- Have key findings been replicated independently, or is this a single
  experiment?

**Blinding and randomization:**
- Were assessors blinded to treatment group?
- Was randomization used, and is the method described?
- If blinding was not possible, is this acknowledged as a limitation?

### Phase 4: Statistical Validity

Goal: evaluate whether the statistical analysis is appropriate and correctly
interpreted. This phase assumes reviewer competence in basic statistics.
If you lack this, state it explicitly rather than guessing.

**Analysis choices:**
- Is the statistical test appropriate for the data type (continuous vs
  categorical, paired vs unpaired, parametric assumptions met)?
- Are multiple comparisons corrected for, and is the method stated
  (Bonferroni, FDR, Tukey)?
- Are effect sizes and confidence intervals reported, not just p-values?

**Common problems to flag:**
- P-values without effect sizes — significance without magnitude
- Confidence intervals that don't match the reported test
- Post-hoc power calculations (circular — power should be pre-specified)
- "Marginally significant" (p = 0.06) treated as meaningful
- Cherry-picking significant results from a battery of tests
- Misuse of correlation to imply causation
- Overlooking non-independence (repeated measures, clustering)

**Data presentation:**
- Are error bars defined in every figure legend (SD, SEM, CI)?
- Are individual data points shown alongside bar plots (especially for n < 10)?
- Are axes scaled appropriately (not truncated to exaggerate differences)?

**Computational methods (if applicable):**
- Are software versions and parameters documented?
- Is the analysis code available and runnable?
- Are random seeds set for reproducibility?

### Phase 5: Integrity and Ethics

Goal: identify concerns about research conduct, data integrity, and ethical
compliance.

**Data availability:**
- Are raw data deposited in a public repository?
- Are accession or DOI numbers provided?
- If data cannot be shared (e.g., patient data), is this justified and are
  summary statistics sufficient?

**Ethics:**
- Are ethics committee or IRB approvals documented (human subjects, animal
  research)?
- Was informed consent obtained (human studies)?
- Are the 3Rs addressed (animal research: replacement, reduction, refinement)?

**Figure integrity:**
- Are there signs of image manipulation (duplicate regions, spliced lanes
  in blots, inconsistent backgrounds)?
- Are microscopy images representative, not selectively chosen?
- Are flow cytometry gating strategies shown?

**Research integrity:**
- Is there evidence of duplicate publication (same data in multiple papers)?
- Are all authors' contributions specified?
- Are competing interests declared?
- Is the funding source disclosed?

### Phase 6: Writing and Clarity

Goal: assess whether the manuscript communicates effectively. This is the
lowest-priority phase — defer to it after all scientific concerns are
documented.

- Is the language clear and precise? Can you understand each sentence on
  first reading?
- Is the narrative logical? Does each section lead naturally to the next?
- Are acronyms defined on first use and kept to a minimum?
- Are figures legible (font size, color contrast, axis labels)?
- Can each figure be understood from its legend alone?
- Is the manuscript length appropriate for the content?

## Writing the Review Report

Organize the report in three sections: summary, major concerns, minor
concerns.

### Summary Section

One or two paragraphs covering:
1. What the manuscript reports (one-sentence summary)
2. Your overall assessment (how novel, how rigorous, how significant)
3. Your recommendation: Accept, Minor Revision, Major Revision, Reject
4. The 2-3 strongest aspects of the work
5. The 2-3 weakest aspects of the work

### Major Concerns

These are issues that must be addressed before the manuscript can be accepted.
Number them sequentially.

For each major concern, include:
- **What the issue is** (specific and localizable: "Section 3.2, the
  regression model uses..." not "the analysis is wrong")
- **Why it matters** (what conclusion or interpretation it affects)
- **What to do about it** (actionable suggestion: re-analysis with X,
  add control Y, clarify Z)

Examples of major concerns: fatal confound, wrong control, missing power
analysis, conclusions unsupported by data, data integrity concerns.

### Minor Concerns

These are issues that would improve the manuscript but are not blockers.
Number them separately.

Examples of minor concerns: unclear phrasing, missing reference, figure
label typo, additional analysis that would strengthen but is not required,
suggestion for better data visualization.

### Tone Rules

- Frame everything about the work, not the authors: "This experiment lacks
  a positive control" not "You forgot a control."
- When you find something good, say so explicitly. "The longitudinal design
  and 5-year follow-up are a significant strength."
- When uncertain, say so: "I may be misunderstanding, but line 237 states X
  while the method on line 115 says Y — can you clarify?"
- Do not request experiments that are infeasible, irrelevant to the research
  question, or beyond the scope of the work.
- Never speculate about author identity, motivation, or competence.

## Discipline-Specific Adaptations

The framework above applies broadly. Adapt emphasis based on field:

**Clinical research:** Prioritize Phase 3 (design, randomization, blinding)
and Phase 4 (statistical validity). Check CONSORT checklist for trials.

**Basic biomedical:** Prioritize Phase 3 (controls, replicates) and Phase 5
(figure integrity, data availability).

**Computational / bioinformatics:** Prioritize Phase 4 (code availability,
software versions, random seeds, cross-validation) and Phase 3 (training/
test separation, overfitting).

**Social sciences:** Prioritize Phase 3 (pre-registration, measurement
validity, sampling) and Phase 4 (effect sizes, confidence intervals).

**Review articles / meta-analyses:** Prioritize search strategy, inclusion/
exclusion criteria, assessment of bias in included studies, and heterogeneity
analysis. Check PRISMA checklist.

## Output Format

Write findings to `work/graph/output/peer-review/review.md`. Structure:

```markdown
# Peer Review Report

**Manuscript:** <title>
**Review completed:** <date>
**Phases completed:** 1-6 (list which)
**Recommendation:** Accept / Minor Revision / Major Revision / Reject

## Summary

<2-3 paragraphs>

## Major Concerns

### 1. <concern title>

- **Location:** Section/paragraph/line
- **Issue:** What is wrong or unclear
- **Why it matters:** How this affects interpretation or validity
- **Recommendation:** What to change or add

### 2. <concern title>
...

## Minor Concerns

### 1. <concern title>

- **Location:** Section/paragraph/line
- **Issue:** What is unclear or could be improved
- **Suggestion:** How to address it

### 2. <concern title>
...
```

## Verification

Before reporting "done":
1. Were all six review phases completed in order?
2. Are major and minor concerns clearly distinguished?
3. Does each major concern include a specific, actionable recommendation?
4. Is the tone constructive throughout (framed about the work, not the author)?
5. Is the output written to the correct path?
6. If a fatal flaw was found in Phase 1, was it clearly labeled as such?