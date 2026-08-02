# Quality Checker Methodology

## Purpose

Apply the 10 documentation quality dimensions (Treude et al., 2020) to both the whitepaper and pitch deck before final compilation. Catch issues that would undermine investor confidence.

## Process

### Step 1: Read both documents

Read these files:
- `work/whitepaper/whitepaper.tex`
- `work/whitepaper/pitch-deck.tex`

### Step 2: Score each document on 10 dimensions

For each dimension, read the relevant sections of the document and score:

| # | Dimension | What to check | PASS | FLAG | FAIL |
|---|-----------|---------------|------|------|------|
| 1 | **Accuracy** | Are claims factually supported by the analysis? Cross-reference every claim against the analysis files. | All claims supported | 1-2 unsupported claims | 3+ unsupported claims |
| 2 | **Completeness** | Are all required sections present? Check against the idea brief's industry classification for the required template sections. | All sections present | 1 section missing | 2+ sections missing |
| 3 | **Consistency** | Do sections agree with each other? Cross-reference key numbers across sections. | All numbers match | 1-2 minor discrepancies | 3+ discrepancies |
| 4 | **Correctness** | Does the LaTeX compile? Check for syntax errors. | Compiles clean | Minor warnings | Errors |
| 5 | **Currency** | Are data and projections current? | All data is current | 1-2 stale references | 3+ stale references |
| 6 | **Readability** | Is the text clear? Check: sentence length (>25 words = flag), jargon density (>2 undefined terms per section = flag), passive voice (>20% of sentences = flag). | All clear | Minor readability issues | Hard to follow |
| 7 | **Relevance** | Does every section serve the investor audience? | All sections relevant | 1 section off-topic | 2+ sections off-topic |
| 8 | **Structure** | Is the document well-organized? Check: TOC, section ordering, logical flow, cross-references. | Well-organized | Minor structural issues | Poor organization |
| 9 | **Style** | Is the tone professional? Check for: marketing fluff ("game-changing", "revolutionary"), overclaims ("best", "only"), emotional language, typos. | Professional tone | Minor style issues | Unprofessional tone |
| 10 | **Timeliness** | Can the document be produced in reasonable time? Check for blocking issues. | No blocking issues | Minor issues | Blocking issues |
| 11 | **Citations** | Does every factual claim have a `\cite{}` or named source? Scan the `.tex` for uncited numbers, percentages, dollar figures, and comparative statements. Cross-reference every `\cite{key}` against `references.bib` to ensure the entry exists. **Check that every entry in `references.bib` has a `howpublished = {\url{...}}` field.** Any entry without a public URL is unverifiable and must be removed. | Every claim cited, all keys match, all entries have URLs | 1-2 missing URLs or uncited claims | 3+ missing URLs or uncited claims |

### Step 3: Write the quality report

For each FAIL or FLAG, provide:
- **Location:** Section name and line number from the `.tex` file
- **Issue:** What's wrong
- **Why it matters:** Why an investor would care
- **Fix:** A concrete, specific fix (not "rewrite this section" — show the replacement text)

### Step 4: Determine the verdict

**PASS:** No blocking issues, all dimensions pass. The documents are ready for compilation.

**FIX MINOR:** Non-blocking issues flagged. The documents can be compiled but the flagged issues should be addressed before distribution.

**BLOCKING ISSUES:** One or more critical issues that must be fixed before compilation. The documents are NOT ready. List the blocking issues and their fixes.

## Output Format

Write to `work/whitepaper/quality-report.md`:

```markdown
# Quality Report: [Business Name]

## Verdict
[PASS / FIX MINOR / BLOCKING ISSUES]

## Whitepaper Scorecard

| Dimension | Score | Notes |
|-----------|-------|-------|
| Accuracy | PASS/FLAG/FAIL | ... |
| Completeness | PASS/FLAG/FAIL | ... |
| Consistency | PASS/FLAG/FAIL | ... |
| Correctness | PASS/FLAG/FAIL | ... |
| Currency | PASS/FLAG/FAIL | ... |
| Readability | PASS/FLAG/FAIL | ... |
| Relevance | PASS/FLAG/FAIL | ... |
| Structure | PASS/FLAG/FAIL | ... |
| Style | PASS/FLAG/FAIL | ... |
| Timeliness | PASS/FLAG/FAIL | ... |

## Whitepaper Issues

### FAIL/FLAG Issues
| Dimension | Location | Issue | Why it matters | Fix |
|-----------|----------|-------|----------------|-----|
| ... | ... | ... | ... | ... |

## Pitch Deck Scorecard
[Same format as above]

## Pitch Deck Issues
[Same format as above]

## Summary
[1-2 sentence verdict with rationale]
```

## Quality Checks

- [ ] Every FLAG or FAIL has a specific location (section:line)
- [ ] Every issue has a concrete fix
- [ ] The verdict is clear and actionable
- [ ] Both documents are scored (whitepaper AND pitch deck)
- [ ] The report distinguishes between the two documents