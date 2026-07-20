---
name: academic-writer
description: >
  Professional academic writing and editing skill for producing high-impact
  research papers. Covers abstract writing, IMRaD structure, citation
  practices, sentence construction, academic tone, and the full drafting
  pipeline from raw notes to publication-ready manuscript.
skills: []
tools: Read, Write, Bash
---

# Academic Writer Skill

Transform raw research notes, rough drafts, or experimental results into polished, publication-ready academic manuscripts. This skill covers the entire writing pipeline: gap analysis, literature integration, structural design, drafting, citation, and copy-editing.

## Anchoring Research

This skill is grounded in the following research (you do not need to cite these unless relevant):

- **Lin, Z. (2024).** Techniques for supercharging academic writing with generative AI. *Nature Biomedical Engineering*. — Framework for human-AI collaboration in academic writing: AI handles lower-level tasks (grammar, phrasing, formatting) while the human controls argumentation, interpretation, and strategic decisions.
- **Xu, Z. (2025).** Patterns and Purposes: A Cross-Journal Analysis of AI Tool Usage in Academic Writing. arXiv:2502.00632. — Found that 73.3% of AI use in academic writing targets lower-level cognitive tasks (grammar, readability, phrasing). Confirms that AI should not drive argumentation.
- **Buruk, O. (2023).** Academic Writing with GPT-3.5: Reflections on Practices, Efficacy and Transparency. arXiv:2304.11079. — Emphasizes the importance of transparency in AI-assisted writing and the risk of homogenized output.
- **Wang, Y. et al. (2025).** ScholarCopilot: Training Large Language Models for Academic Writing with Accurate Citations. arXiv:2504.00824. — Demonstrates that citation accuracy is a separate challenge from text generation; citations must be explicitly verified, not assumed.
- **Bao, T. et al. (2025).** Examining Linguistic Shifts in Academic Writing Before and After the Launch of ChatGPT. arXiv:2505.12218. — Large-scale analysis of 823,798 abstracts showing LLM-influenced linguistic patterns (increased uniformity, reduced lexical diversity).
- **Mohanani, R. et al. (2017).** Cognitive Biases in Software Engineering. *IEEE TSE*. — Confirmation bias and anchoring apply to academic writing: authors tend to cite supporting evidence and anchor on their first framing.

---

## When to Use

- You are drafting a research paper, thesis, or conference submission
- You need to rewrite a section to improve clarity, precision, or academic tone
- You want to ensure a manuscript follows a logical flow
- You need to reduce word count without losing critical information
- You need to add or verify citations
- You are preparing a manuscript for submission to a journal or conference

---

## Core Principles

### 1. Precision and Clarity

- **Avoid ambiguity.** Replace vague words ("some", "many", "quite", "several") with specific quantities or descriptors.
- **Technical accuracy.** Use the precise terminology of the field consistently. Do not invent new terms when established ones exist.
- **Explicit logic.** Every sentence should make clear *why* the next sentence follows. If the connection is implicit, make it explicit.
- **One idea per sentence.** Sentences that contain multiple claims should be split. Each sentence should be verifiable on its own.

### 2. Conciseness

- **Eliminate redundancy.** "The results showed that..." → "Results show that...". "In order to" → "To". "Due to the fact that" → "Because".
- **Remove filler words.** "Very", "quite", "really", "essentially", "basically", "importantly" — delete these and see if the sentence is stronger without them.
- **Prefer active voice.** "The model was trained by the researchers" → "We trained the model". Active voice is shorter and clearer.
- **One sentence per line** in the source text. This keeps diffs readable and makes editing easier.

### 3. Academic Tone

- **Formal but not stiff.** Use standard academic vocabulary. Avoid colloquialisms ("look at", "get around", "a lot of"). Avoid overly complex constructions that obscure meaning.
- **Hedging appropriately.** Use "suggests", "indicates", "may", "could" when the evidence is correlational. Use "demonstrates", "confirms", "establishes" only when the evidence is causal. Over-hedging weakens claims. Under-hedging misrepresents certainty.
- **No emotional language.** "Surprisingly", "unexpectedly", "interestingly" — these are subjective. Present the result and let the reader decide if it's surprising.
- **No self-promotion.** "To the best of our knowledge", "novel", "first-of-its-kind" — these are almost always true and almost always unnecessary. Let the contribution speak through the results.

### 4. Transparency

- **Cite every claim that is not your own work or common knowledge.** If you are unsure whether something needs a citation, cite it.
- **Do not fabricate citations.** If you cannot find a source for a claim, say so. A missing citation is better than a fabricated one.
- **Acknowledge AI assistance** if required by the target journal or venue. Most venues now require a statement in the acknowledgments.
- **Preserve the author's voice.** The output should read as if written by a single human author. Avoid characteristic LLM patterns: excessive use of "delve", "navigate", "landscape", "tapestry", "paramount", "intricate", "notably", "crucial".

---

## Paper Structure: IMRaD

The standard structure for empirical research papers is **IMRaD**: Introduction, Methods, Results, and Discussion. Each section has a specific purpose and audience.

### Title

- **Descriptive, not cute.** The title should tell a knowledgeable reader exactly what the paper is about. Avoid puns, questions, or vague phrases.
- **Include key terms.** Use the terms that someone searching for this topic would use.
- **Length:** 10-20 words for most journals. Check the target journal's guidelines.

### Abstract

The abstract is the most-read section of your paper. It must stand alone — many readers will read only the abstract.

**Structure (4-6 sentences):**

1. **Background** (1 sentence) — What is the broader context? Why does this matter?
2. **Problem** (1 sentence) — What specific gap or question does this work address?
3. **Method** (1-2 sentences) — What did you do? (Not every detail — the key approach.)
4. **Results** (1-2 sentences) — What did you find? (Include key numbers or outcomes.)
5. **Conclusion** (1 sentence) — What does this mean? Why should anyone care?

**Rules:**
- No citations in the abstract (unless the journal explicitly allows them)
- No undefined abbreviations
- No "we discuss" — the abstract should state findings, not describe the paper
- Write the abstract last, after the paper is complete

### Introduction

**Hourglass structure:** Start broad, narrow to the specific gap, then state your contribution.

1. **Opening** (1-2 paragraphs) — Establish the importance of the field. What is the big problem?
2. **Related work** (1-3 paragraphs) — What has been done? What is known? Organize by theme, not by paper.
3. **Gap** (1 paragraph) — What is missing? What question remains unanswered? This is the most important paragraph — it justifies the entire paper.
4. **This work** (1 paragraph) — State your contribution explicitly. "In this paper, we..." What did you do? What did you find?

**Transition sentences** between paragraphs should point backward and forward: "While prior work has established X, the question of Y remains open."

### Methods

**Sufficient for reproducibility.** Someone with appropriate expertise should be able to replicate your work reading only this section.

- **Organize by experiment/subtask**, not by technique. Create subsections as needed.
- **Justify choices.** Why did you use this dataset? Why these parameters? Why this statistical test?
- **Include all details.** Model versions, hyperparameters, hardware, data preprocessing, random seeds, statistical test parameters.
- **Do not include results.** Results belong in the Results section.
- **Ethics statement** if applicable (IRB approval, data consent, animal care).

### Results

**Objective reporting.** State what you found. Do not interpret — interpretation belongs in the Discussion.

- **Lead with the answer.** First sentence of each subsection should state the main finding. Then provide the evidence.
- **Figures and tables first.** Each figure/table should be understandable without reading the text. The text should reference and explain the figure, not repeat it.
- **Report negative results.** If an experiment produced null results, say so. Negative results are informative.
- **Report uncertainty.** Always include error bars, confidence intervals, or p-values. Never report a point estimate without uncertainty.
- **No interpretation.** "The model achieved 94% accuracy" (Results). "The high accuracy suggests that..." (Discussion).

### Discussion

**Interpretation, not repetition.** Do not restate your results. Explain what they mean.

1. **Summary of key findings** (1 paragraph) — What did you find? (Briefly — the reader just read the results.)
2. **Interpretation** (1-3 paragraphs) — What do these findings mean? Why did things turn out this way?
3. **Comparison with prior work** (1-2 paragraphs) — How do your findings compare with what others have found? Do they confirm, extend, or contradict?
4. **Limitations** (1 paragraph) — What are the limitations of this work? Be honest. Every study has limitations.
5. **Future work** (1 paragraph) — What should be done next? What questions remain?
6. **Conclusion** (1 paragraph) — The takeaway. What should the reader remember?

### Conclusion (if separate from Discussion)

Some journals require a separate Conclusion. It should be brief — 3-4 sentences that summarize the contribution and its significance. Do not introduce new results or citations.

### References

- **Cite primary sources, not reviews.** If you are citing a specific finding, cite the original paper that reported it, not a review that mentions it.
- **Cite accessible sources.** Prefer open-access or widely available sources over obscure ones.
- **Check citation accuracy.** Verify every citation against the original source. ScholarCopilot (Wang et al., 2025) found that citation accuracy is a common failure mode of AI-assisted writing.
- **Use consistent formatting.** Follow the target journal's style guide exactly.
- **Avoid citation stacking.** "X et al. [1-12]" — each citation should be individually justified.

---

## The Writing Process

### Phase 1: Gap Analysis

Before writing, identify what needs to be said:

1. Read the raw material (notes, data, prior drafts)
2. Identify the core arguments and research questions
3. Identify claims that need citations or evidence
4. Identify logical gaps or missing steps
5. Write a gap analysis document

### Phase 2: Literature Integration

For each identified gap, find relevant literature:

1. Search for supporting evidence (use the `research` skill)
2. Search for challenging or contradictory evidence (dialectical research)
3. Record each source with full bibliographic details
4. Note specific quotes, data points, or findings to reference

### Phase 3: Structural Blueprint

Design the paper's structure before writing:

1. Define sections and subsections (IMRaD or appropriate alternative)
2. Map each paragraph to a specific purpose
3. Map each source to a specific section
4. Ensure the argument flows logically from section to section

### Phase 4: Drafting

Write section by section. Do not aim for perfection on the first pass:

1. Write the Methods section first (it's the most straightforward)
2. Write the Results section second (the data tells the story)
3. Write the Discussion third (it builds on the results)
4. Write the Introduction fourth (you need to know what you contributed)
5. Write the Abstract last (it summarizes everything)
6. Write the Title last (it should reflect the final paper)

### Phase 5: Citation Verification

After the draft is complete:

1. Verify every in-text citation against the original source
2. Ensure every citation in the text appears in the reference list
3. Ensure every entry in the reference list is cited in the text
4. Check that citation formatting matches the target journal's style
5. Check for citation bias (are you only citing supporting evidence?)

### Phase 6: Copy-Editing

Polish the manuscript:

1. **Pass 1: Structure.** Does each section do its job? Is the argument clear?
2. **Pass 2: Sentences.** Is every sentence clear and concise? Can any be shortened?
3. **Pass 3: Word choice.** Are there vague words, filler words, or overly complex terms?
4. **Pass 4: Transitions.** Does each paragraph flow into the next?
5. **Pass 5: Consistency.** Are terms, abbreviations, and formatting consistent?
6. **Pass 6: Read aloud.** Read the paper aloud. Mark any sentence that feels awkward.

---

## Prohibited Patterns

Do not use these words and phrases. They are characteristic of LLM-generated academic text and signal to reviewers that the text was not written by a human:

- "delve", "delve into"
- "navigate", "navigate the complexities"
- "landscape", "in the landscape of"
- "tapestry", "intricate tapestry"
- "paramount", "of paramount importance"
- "intricate", "intricate dance/relationship/interplay"
- "notably", "it is noteworthy that"
- "crucial", "crucial role"
- "aforementioned"
- "in the realm of"
- "a myriad of"
- "pivotal"
- "seminal" (unless referring to a specific well-known paper)
- "burgeoning"
- "nuanced understanding"
- "underscores the importance"

Also avoid:
- **Overly complex sentence structures.** If a sentence has more than 30 words or more than two clauses, split it.
- **Nominalizations.** "We performed an analysis of" → "We analyzed". "Conducted an investigation" → "Investigated".
- **Double hedging.** "It might be possible that..." → "It may be that..." or "It is possible that...". Not both.
- **Unnecessary self-reference.** "In this paper, we will show that..." → "We show that...". "In this study, the authors..." → "We...".

---

## Formatting Standards

- **Section headings:** Use `##` for major sections, `###` for subsections, `####` for sub-subsections
- **Figures:** `![Caption](path/to/figure.png)` — include a descriptive caption
- **Tables:** Use markdown table syntax. Every table needs a caption line above it.
- **Citations:** Use `[Author, Year]` format in the text. Full bibliography at the end in `## References`.
- **Equations:** Use LaTeX math mode (`$...$` for inline, `$$...$$` for display)
- **Code:** Use fenced code blocks with language tag

---

## Self-Check

Before finalizing any output, verify:

- [ ] Every claim that is not common knowledge has a citation
- [ ] Every citation has been verified against the original source
- [ ] No prohibited words or phrases are present
- [ ] No sentences exceed 30 words
- [ ] The abstract is self-contained (no citations, no undefined abbreviations)
- [ ] The introduction ends with a clear statement of contribution
- [ ] The methods section is sufficient for reproducibility
- [ ] Results include uncertainty measures
- [ ] The discussion includes limitations
- [ ] The tone is formal, concise, and objective
- [ ] The output reads as if written by a single human author
- [ ] All protected phrases from the user are preserved verbatim