# Documentation Quality Dimensions

Based on: Treude, C., Middleton, J., & Atapattu, T. (2020). "Beyond Accuracy: Assessing Software Documentation Quality."

## The 10 Dimensions

### 1. Accuracy

**Definition:** The extent to which documentation correctly reflects the system it describes.

**PASS:** Every claim is supported by the analysis files. Numbers match across sections. Technical claims are accurate.
**FAIL:** Claims without evidence. Numbers that don't match. Technical descriptions that are wrong.

**How to fix:** Cross-reference every claim against the analysis files. If a claim isn't supported, remove it or add the evidence.

### 2. Completeness

**Definition:** The extent to which documentation covers all aspects of the system.

**PASS:** All required sections are present. No obvious gaps. Every question an investor would ask is addressed.
**FAIL:** Missing sections. Unanswered questions. Gaps in the narrative.

**How to fix:** Check against the template section list. For the industry classification, verify that all relevant sections are included. If a section is missing, add it.

### 3. Consistency

**Definition:** The extent to which documentation is internally consistent and free of contradictions.

**PASS:** Numbers match across sections. Terminology is consistent. No contradictions.
**FAIL:** Contradictory numbers, conflicting claims, inconsistent terminology.

**How to fix:** Cross-reference key numbers across all sections. Revenue in the financial section must match revenue in the market section. Timeline in the technical section must match timeline in the GTM section.

### 4. Correctness

**Definition:** The extent to which documentation is syntactically and structurally correct.

**PASS:** LaTeX compiles without errors. No syntax issues. Well-formed documents.
**FAIL:** LaTeX compilation errors. Broken references. Missing `\end{document}`.

**How to fix:** Run `pdflatex` and fix all errors. Check for unescaped special characters, missing brackets, and broken references.

### 5. Currency

**Definition:** The extent to which documentation reflects the current state of the system.

**PASS:** All data is current. Projections are clearly labeled as forward-looking. Market data is from the last 2 years.
**FAIL:** Stale data. Outdated market references. Projections that don't account for recent changes.

**How to fix:** Check the date of every data point. Market data should be from the last 2 years. If the idea brief was written in 2025, don't cite 2020 market reports.

### 6. Readability

**Definition:** The extent to which documentation is easy to read and understand.

**PASS:** Clear sentences, defined jargon, appropriate level of detail. Active voice preferred.
**FAIL:** Run-on sentences (>25 words). Undefined jargon. Passive voice >20% of sentences. Dense paragraphs.

**How to fix:**
- Break long sentences into shorter ones
- Define jargon on first use: "We use a transformer model (a type of neural network designed for sequential data)..."
- Replace passive voice with active: "The system processes data" not "Data is processed by the system"
- Use bullet points for lists, not dense paragraphs

### 7. Relevance

**Definition:** The extent to which documentation serves its intended audience and purpose.

**PASS:** Every section serves the investor audience. No irrelevant content. Focused on the investment thesis.
**FAIL:** Off-topic sections. Too much detail on irrelevant topics. Missing the forest for the trees.

**How to fix:** For each section, ask: "Does this help an investor decide whether to invest?" If no, cut it or move it to the appendix.

### 8. Structure

**Definition:** The extent to which documentation is organized and navigable.

**PASS:** Clear section hierarchy, logical flow, table of contents, cross-references.
**FAIL:** Poor organization, missing TOC, no logical flow, hard to navigate.

**How to fix:** Follow the template section order. Use `\label{sec:name}` and `\ref{sec:name}` for cross-references. Ensure the TOC is generated.

### 9. Style

**Definition:** The extent to which documentation follows conventions of professional writing.

**PASS:** Professional tone. No marketing fluff. No overclaims. No typos or grammatical errors.
**FAIL:** "Game-changing", "revolutionary", "disruptive". "Best", "only", "first". Exclamation marks. Typos.

**How to fix:**
- Replace "game-changing" with specific facts
- Replace "we're the best" with "our approach improves X by Y% over Z"
- Proofread for typos and grammar
- Use a professional, understated tone. Let the facts speak.

### 10. Timeliness

**Definition:** The extent to which documentation can be produced and updated in reasonable time.

**PASS:** No blocking issues. Can be compiled and distributed today.
**FAIL:** Blocking issues that prevent compilation or distribution.

**How to fix:** Address all blocking issues before compilation. Run the full pipeline and verify the output.

## Applying the Dimensions

### For the Whitepaper

Score each dimension on the whitepaper.tex file. Focus on the content, structure, and style.

### For the Pitch Deck

Score each dimension on the pitch-deck.tex file. Focus on the slide structure, design consistency, and alignment with the whitepaper.

### Verdicts

| Verdict | Meaning | Action |
|---------|---------|--------|
| PASS | All dimensions pass. No blocking issues. | Compile and distribute. |
| FIX MINOR | Non-blocking issues flagged. | Compile, but fix flagged issues before distribution. |
| BLOCKING | One or more critical issues. | Fix before compilation. Re-run quality check. |